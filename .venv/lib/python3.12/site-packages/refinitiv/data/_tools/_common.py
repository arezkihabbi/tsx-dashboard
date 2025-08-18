import threading
from collections import defaultdict
from enum import Enum
from typing import Any, Callable, List, Optional, TYPE_CHECKING, Union, Iterable

import simplejson as json

from ._lazy_loader import load as lazy_load

np = lazy_load("numpy")
pd = lazy_load("pandas")

if TYPE_CHECKING:
    from pandas import DataFrame

forbidden_symbols = ':/|\\?*<>"'


class OrEvent(threading.Event):
    @staticmethod
    def orify(event, changed_callback):
        def or_clear(self):
            self._clear()
            self.changed()

        def or_set(self):
            self._set()
            self.changed()

        event._set = event.set
        event._clear = event.clear
        event.changed = changed_callback
        event.set = lambda: or_set(event)
        event.clear = lambda: or_clear(event)

    def __init__(self, *events) -> None:
        super().__init__()

        def changed():
            bools = [ev.is_set() for ev in events]
            if any(bools):
                self.set()
            else:
                self.clear()

        for event in events:
            OrEvent.orify(event, changed)

        # initialize
        changed()


class RepeatedTimer(threading.Timer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True

    def not_finished(self) -> bool:
        return not self.finished.is_set()

    def run(self):
        while self.not_finished():
            self.finished.wait(self.interval)
            if not self.finished.is_set():
                self.function(*self.args, **self.kwargs)


class CallbackHandler:
    def __init__(self):
        self._lock = threading.Lock()
        self._callbacks = defaultdict(list)

    def on(self, event: str, callback: Callable) -> None:
        with self._lock:
            self._callbacks[event].append(callback)

    def is_on(self, event: str) -> bool:
        return event in self._callbacks

    def has_callback(self, event: str, callback: Callable) -> bool:
        return event in self._callbacks and callback in self._callbacks[event]

    def has_no_callback(self, event: str, callback: Callable) -> bool:
        return not self.has_callback(event, callback)

    def remove_callback(self, event: str, callback: Callable) -> None:
        with self._lock:
            callbacks = self._callbacks[event]
            callback in callbacks and callbacks.remove(callback)
            not callbacks and self._callbacks.pop(event, None)

    def emit(self, event: str, *args, **kwargs) -> None:
        # .copy() makes sure that underlying list will not change during iteration
        for callback in self._callbacks.get(event, []).copy():
            callback(*args, **kwargs)

    def remove_all_callbacks(self, event: Optional[str] = None) -> None:
        with self._lock:
            if event is not None:
                self._callbacks.pop(event, None)
            else:
                self._callbacks = defaultdict(list)


def ohlc(self, interval: str = "1min", *args, **kwargs) -> "DataFrame":
    call_from_recorder = kwargs.pop("call_from_recorder", False)
    df = self.fillna(method="ffill")
    df.fillna(method="bfill", inplace=True)
    df = df.astype("float")

    df = df.resample(interval, *args, **kwargs).ohlc()

    if call_from_recorder:
        df.fillna(pd.NA, inplace=True)
    return df


def get_from_path(obj, path, delim="."):
    if isinstance(path, list):
        splitted = path

    else:
        splitted = path.split(delim)

    for k in splitted:
        if hasattr(obj, "get"):
            obj = obj.get(k)

        elif iterable(obj) and is_int(k):
            try:
                obj = obj[int(k)]
            except (IndexError, KeyError):
                return None

    return obj


def is_int(obj):
    if isinstance(obj, str):
        try:
            int(obj)
        except Exception:
            return False
        else:
            return True
    return isinstance(obj, int)


def iterable(obj):
    if isinstance(obj, str):
        return False
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def bool_or_none_to_str(value: Any) -> Union[str, Any]:
    """
    Coerce a bool type or None type into a string value.

    Note that we prefer JSON-style 'true'/'false' for boolean values here.
    """
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return ""

    return value


def urljoin(*pieces):
    # first piece have a leading slash
    if all(piece is None for piece in pieces):
        return ""

    if pieces and len(pieces[0]) > 1 and pieces[0][0] == "/":
        pieces = ("/",) + pieces
    # last piece have a trailing slash
    if pieces and len(pieces[-1]) > 1 and pieces[-1][-1] == "/":
        pieces = pieces + ("/",)

    return "/".join(s.strip("/") for s in pieces)


def is_all_same_type(item_type, items):
    return all(isinstance(item, item_type) for item in items)


def make_counter():
    i = 0

    def counter():
        nonlocal i
        i += 1
        return i

    return counter


def get_response_reason(response):
    if hasattr(response, "reason_phrase"):
        return response.reason_phrase
    elif hasattr(response, "reason"):
        return response.reason
    return "unknown reason"


class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        result = instance.__dict__[self.func.__name__] = self.func(instance)
        return result


def is_all_str(input_list: list) -> bool:
    return all([isinstance(i, str) for i in input_list])


def validate_bool_value(value: bool) -> bool:
    if isinstance(value, bool):
        return value
    else:
        raise ValueError(f"Please provide boolean value ('True' or 'False'), current value is '{value}'")


class ArgsParser:
    def __init__(self, parse) -> None:
        self.parse = parse

    def get_str(self, *args, delim=None) -> str:
        if delim is not None:
            retval = delim.join(str(item) for item in self.get_list(*args))
        else:
            retval = self.parse(*args)
            if not isinstance(retval, str):
                retval = str(retval)
        return retval

    def get_list(self, *args) -> list:
        retval = self.parse(*args)
        if not isinstance(retval, list):
            retval = [retval]
        return retval

    def get_float(self, *args) -> float:
        retval = self.parse(*args)
        if isinstance(retval, np.datetime64):
            retval = retval.astype(float)
        else:
            retval = float(retval)
        return retval

    def get_bool(self, *args) -> bool:
        retval = self.parse(*args)
        if not isinstance(retval, bool):
            retval = bool(retval)
        return retval

    def get_unique(self, *args) -> list:
        return list(dict.fromkeys(self.get_list(*args)))


class EnumArgsParser(ArgsParser):
    def __init__(self, parse, parse_to_enum) -> None:
        super().__init__(parse)
        self.parse_to_enum = parse_to_enum

    def get_enum(self, *args) -> Enum:
        return self.parse_to_enum(*args)


def parse_list_of_str(param: Union[str, list]) -> list:
    if isinstance(param, str):
        return [param]

    if isinstance(param, list):
        if is_all_same_type(str, param):
            return param
        else:
            raise ValueError(f"Not all elements are strings in {param}")

    raise TypeError(f"Invalid type, expected str or list, {type(param).__name__} is given")


def parse_iterable_of_str(param: Union[str, Iterable[str]]) -> list:
    if isinstance(param, str):
        return [param]

    if isinstance(param, Iterable):
        if not isinstance(param, list):
            param = list(param)
        if is_all_same_type(str, param):
            return param
        else:
            raise ValueError(f"Not all elements are strings in {param}")

    raise TypeError(f"Invalid type, expected str or list, {type(param).__name__} is given")


def make_parse_enum(enum_class: iterable, can_be_lower: bool = True) -> callable:
    enum_values = [k.value for k in enum_class]

    def parse_enum(param: Union[str, list, Enum]) -> Union[str, list]:
        if isinstance(param, list):
            return [parse_enum(p) for p in param]

        if isinstance(param, enum_class):
            return param.value

        if param in enum_values:
            return param

        if can_be_lower and hasattr(param, "upper"):
            param_upper = param.upper()
            upper_enum_values = {value.value.upper(): value for value in enum_class}

            if param_upper in upper_enum_values:
                return upper_enum_values[param_upper].value

        raise AttributeError(f"Value '{param}' must be in {enum_values}")

    return parse_enum


def make_convert_to_enum(enum_class: iterable) -> callable:
    lower_values = {item.value.lower(): item for item in enum_class}

    def convert_to_enum(param: Union[str, List[str], Enum, List[Enum]]) -> Union[Enum, List[Enum]]:
        if isinstance(param, str) and param.lower() in lower_values:
            return lower_values[param.lower()]

        if isinstance(param, list):
            return [convert_to_enum(p) for p in param]

        if isinstance(param, enum_class):
            return param

        if isinstance(param, str) and param.upper() in enum_class.__members__.keys():
            param = enum_class.__members__[param.upper()]
            return param

        raise ValueError(f"Cannot convert param '{param}'")

    return convert_to_enum


def parse_hp_universe(universe: Union[str, list]) -> list:
    universe = parse_list_of_str(universe)
    universe = [i for i in universe if i not in {"", " "}]
    if universe:
        return universe
    raise ValueError("List of universes is empty, nothing to process")


def validate_types(val: Any, types: Union[list, tuple], val_name: str = "") -> None:
    t_names = [tp.__name__ for tp in types if tp if tp.__name__ != "NoneType"]

    if None in types:
        raise TypeError("Use 'type(None)' instead 'None', in 'types'")

    if type(val) not in types:
        raise TypeError(
            f"Parameter '{val_name}' of invalid type provided: '{type(val).__name__}', expected types: {t_names}"
        )


fields_arg_parser = ArgsParser(parse_list_of_str)
universe_arg_parser = fields_arg_parser
hp_universe_parser = ArgsParser(parse_hp_universe)
custom_insts_historical_universe_parser = ArgsParser(parse_hp_universe)
iterator_str_arg_parser = ArgsParser(parse_iterable_of_str)
attributes_arg_parser = fields_arg_parser


def make_enum_arg_parser(*args, **kwargs):
    return ArgsParser(make_parse_enum(*args, **kwargs))


def make_convert_to_enum_arg_parser(*args, **kwargs):
    return ArgsParser(make_convert_to_enum(*args, **kwargs))


def make_enum_arg_parser_by_members(enum_class, can_be_lower=True):
    parser = make_parse_enum(enum_class, can_be_lower)

    def _parser(value):
        lower_values = {name.lower(): item for name, item in enum_class.__members__.items()}
        if isinstance(value, str) and value.lower() in lower_values:
            value = lower_values[value.lower()]
        return parser(value)

    return ArgsParser(_parser)


def merge_dict_to_dict(dest: dict, source: dict) -> dict:
    for source_key, source_value in source.items():
        dest_value = dest.get(source_key)

        if source_key in dest and isinstance(source_value, dict) and isinstance(dest_value, dict):
            merge_dict_to_dict(dest_value, source_value)

        else:
            dest[source_key] = source_value

    return dest


def extend_params(params, extended_params):
    if extended_params:
        # params -> [("param1", "val1"), ]
        params = dict(params)
        # result -> {"param1": "val1"}
        params.update(extended_params)
        # result -> {"param1": "val1", "extended_param": "value"}
        # return [("param1", "val1"), ("extended_param", "value")]
        return list(params.items())
    return params


def get_correct_filename(filename, replace_with=""):
    result = filename
    for symbol in forbidden_symbols:
        result = result.replace(symbol, replace_with)
    return result


class lazy_dump:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return json.dumps(self.value)


class lazy_formatting:
    def __init__(self, text, *args):
        self.text = text
        self.args = args

    def __str__(self):
        return self.text % self.args

    def __repr__(self):
        return self.text % self.args


class NotNoneList(list):
    def __init__(self, *args):
        super().__init__()
        for arg in args:
            self.append(arg)

    def append(self, item) -> None:
        super().append(item if item is not None else pd.NA)

    def extend(self, iterable) -> None:
        for item in iterable:
            self.append(item)

    def __setitem__(self, key, value):
        if value is None:
            value = pd.NA
        super().__setitem__(key, value)

    def insert(self, index, item) -> None:
        if item is None:
            item = pd.NA
        super().insert(index, item)


def get_warning_message_if_parameter_no_used_in_request(param_name, not_applicable=None, applicable=None):
    message = []
    if not_applicable:
        not_applicable = " and ".join(not_applicable)
        not_applicable = f"is not applicable for {not_applicable}"
        message.append(not_applicable)
    if applicable:
        applicable = " and ".join(applicable)
        applicable = f"is applicable only to {applicable}"
        message.append(applicable)

    return f"'{param_name}' {' and '.join(message)}"
