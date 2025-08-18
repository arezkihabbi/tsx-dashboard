from typing import Callable, List, Optional, Any


def is_date_true(param: Any) -> bool:
    return param is not None


class ParamItem:
    def __init__(
        self,
        arg_name: str,
        query_param_name: Optional[str] = None,
        function: Optional[Callable] = None,
        is_true: Callable = None,
    ):
        self.arg_name = arg_name
        self.query_param_name = query_param_name or arg_name
        self.function = function
        self.is_true = lambda param: is_true(param) if is_true else bool(param)


class ValueParamItem(ParamItem):
    def __init__(
        self,
        arg_name: str,
        query_param_name: Optional[str] = None,
        function: Optional[Callable] = None,
        is_true: Callable = None,
    ):
        super().__init__(arg_name, query_param_name, function, is_true)
        self.function = lambda value, *args, **kwargs: function(value)


class SerParamItem(ParamItem):
    def __init__(
        self,
        arg_name: str,
        query_param_name: Optional[str] = None,
        function: Optional[Callable] = None,
        is_true: Callable = None,
    ):
        super().__init__(arg_name, query_param_name, function, is_true)
        self.function = lambda v, *args, **kwargs: v if not hasattr(v, "get_dict") else v.get_dict()


def get_params(params_config: List[ParamItem], *args, **kwargs):
    retval = []
    for item in params_config:
        param = kwargs.get(item.arg_name)
        if not item.is_true(param):
            continue

        if item.function:
            _kwargs = {k: v for k, v in kwargs.items() if k != item.arg_name}
            param = item.function(param, *args, **_kwargs)
        retval.append((item.query_param_name, param))
    return retval
