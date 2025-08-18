from typing import Union, List, Dict, TYPE_CHECKING

from ._dictionary_type import DictionaryType
from ._enum_type_entry import EnumTypeEntry, create_enum_entry
from ._field_description import FieldDescription, create_field_description
from ._validator import validator
from .._stream_factory import create_dictionary_stream
from .._validator_exceptions import ValidationException
from ...._content_type import ContentType
from ...._core.log_reporter import PrvLogReporterMixin
from ...._core.session import get_default
from ...._tools import version_to_tuple

if TYPE_CHECKING:
    from .._dictionary_stream import PrvDictionaryStream
    from ...._core.session import Session


class Dictionary(PrvLogReporterMixin):
    """
    Examples
    --------
    If user create a session and pass it to Dictionary, then load method will use passed session
    >>> import refinitiv.data as rd
    >>> session = rd.session.Definition().get_session()
    >>> dictionary = rd.delivery._dictionary.Dictionary(session=session)
    >>> dictionary.load()

    If user create a session and set it default, then load method will use default session
    >>> import refinitiv.data as rd
    >>> sess_definition = rd.session.Definition()
    >>> dictionary = rd.delivery._dictionary.Dictionary()
    >>> session_A = sess_definition.get_session()
    >>> rd.session.set_default(session_A)
    >>> dictionary.load() # will use session_A
    >>> session_B = sess_definition.get_session()
    >>> rd.session.set_default(session_B)
    >>> dictionary.load() # will use session_B

    If user create a session and pass it to Dictionary,
    then load method will use passed session even if exists default session
    >>> import refinitiv.data as rd
    >>> sess_definition = rd.session.Definition()
    >>> session_A = sess_definition.get_session()
    >>> dictionary = rd.delivery._dictionary.Dictionary(session=session_A)
    >>> session_B = sess_definition.get_session()
    >>> rd.session.set_default(session_B)
    >>> dictionary.load() # will use session_A
    """

    def __init__(self, session: "Session" = None, service: str = None) -> None:
        from . import check_websocket_version

        check_websocket_version()

        self._session = session
        self._session_from_ctor = bool(session)
        self._session and self._init_logger(self._session.logger())

        self._service = service
        self._fid_to_field_desc: Dict[int, FieldDescription] = {}
        self._acronym_to_field_desc: Dict[str, FieldDescription] = {}
        self._fid_to_enum_type: Dict[int, EnumTypeEntry] = {}
        self._dict_type_to_version: Dict[DictionaryType, tuple] = {}
        self._rippled_fields = set()

    @property
    def is_field_dict_available(self) -> bool:
        return bool(self._fid_to_field_desc)

    @property
    def is_enum_dict_available(self) -> bool:
        return bool(self._fid_to_enum_type)

    @property
    def versions(self) -> dict:
        """
        retrieve the field and enum type metadata version. e.g: {"RWFFld": (4,20,30), "RWFEnum": (17, 91)}

        Returns
        -------
        dict {"RWFFld": fld_version, "RWFEnum": enum_version}
            The first item is field dictionary version and the second item is enum type dictionary version

        Examples
        --------
        >>> from refinitiv.data.delivery._dictionary import Dictionary, DictionaryType
        >>> dictionary = Dictionary()
        >>> dictionary.load()
        >>> dictionary.versions
            {"RWFFld": (4,20,30), "RWFEnum": (17, 91)}
        >>> dictionary.versions['RWFEnum']
            (17, 91)
        """
        return self._dict_type_to_version

    def get_field(self, key: Union[int, str]) -> Union[FieldDescription, None]:
        """
        To retrieve the field's information by name or fid,
        including "name", "long_name", "fid", "ripple_to", "field_type", "length", "rwf_type", "rwf_len"

        Parameters
        ----------
        key : str | int
            If it is string, it is parsed as name; if it is int, it is parsed as fid.

        Returns
        ----------
        FieldDescription | None
            Return all information for one field defined in metadata or None if all acronyms cannot be found in metadata

        Examples
        ----------
        >>> from refinitiv.data.delivery._dictionary import Dictionary
        >>> dictionary = Dictionary()
        >>> dictionary.load()
        >>> keys = ['BID', 4]  # 4 stands for RDN_EXCHID
        >>> for key in keys:
        ...     field = dictionary.get_field(key)
        ...     print(field)
        """
        field_desc = None

        # key is a "name"
        if isinstance(key, str) and key in self._acronym_to_field_desc:
            field_desc = self._acronym_to_field_desc[key]

        # key is a "fid"
        elif isinstance(key, int) and key in self._fid_to_field_desc:
            field_desc = self._fid_to_field_desc[key]

        return field_desc

    def get_enum_display(self, key: Union[int, str], value: int) -> Union[str, None]:
        """
        To retrieve enumerated field's value by enum id.
        For example, one of the enumerated type for field RDN_EXCHID "ASE" and its value is 1, it will return the str value "ASE".

        Parameters
        ----------
        key : str | int
            To identify the field. If it is a string, it is parsed as a name; if it is an int, it is parsed as a fid.
        value : int
            The value of the enumerated field.

        Returns
        ----------
        int | None
            Field's value for specified display or None if the field is not enum type or the field is not defined in metadata.

        Examples
        ----------
        >>> from refinitiv.data.delivery._dictionary import Dictionary
        >>> dictionary = Dictionary()
        >>> dictionary.load()
        >>> dictionary.get_enum_display("RDN_EXCHID", 1)
            "ASE"
        >>> dictionary.get_enum_display(4, 1)
            "ASE"
        """
        field_desc = self.get_field(key)

        if field_desc is None:
            return None

        enum_display = None

        if field_desc.enum_length > 0:
            enum_type = self._fid_to_enum_type.get(field_desc.fid)

            if enum_type and value in enum_type.values:
                index = enum_type.values.index(value)

                if len(enum_type.displays) > index:
                    enum_display = enum_type.displays[index]

        return enum_display

    def get_enum_value(self, key: Union[int, str], display: str) -> Union[int, None]:
        """
        To retrieve enumerated field's value by display.
        For example, one of the enumerated type for field RDN_EXCHID "ASE" and its value is 1, it will return the int value 1.

        Parameters
        ----------
        key : str | int
            To identify the field. If it is a string, it is parsed as a name; if it is an int, it is parsed as a fid.
        display: str
            The value of the enumerated field.

        Returns
        ----------
        int | None
            Field's value for specified display or None, if the field is not enum type or the field is not defined in metadata.

        Examples
        ----------
        >>> from refinitiv.data.delivery._dictionary import Dictionary
        >>> dictionary = Dictionary()
        >>> dictionary.load()
        >>> dictionary.get_enum_value("RDN_EXCHID", "ASE")
            1
        >>> dictionary.get_enum_value(4, "ASE")
            1
        """
        field_desc = self.get_field(key)

        if field_desc is None:
            return None

        value = None

        if field_desc.enum_length > 0:
            enum_type = self._fid_to_enum_type.get(field_desc.fid)

            if enum_type and display in enum_type.displays:
                index = enum_type.displays.index(display)

                if len(enum_type.displays) > index:
                    value = enum_type.values[index]

        return value

    def is_valid_enum_field(self, key: Union[str, int], value: Union[str, int]) -> bool:
        is_valid = True

        try:
            validator.check_enum_field_value(key, value)
        except ValidationException:
            is_valid = False

        return is_valid

    def validate(self, fields: dict, **kwargs) -> dict:
        """
        To check whether several fields' key and value are compliance with the dictionary definition.
        If any field is invalid, it will be returned with the error message, also it will be stored in the log.

        Parameters
        ----------
        fields: dict
             Which key is field name or fid, its value is the value of the field.

        kwargs: key1=value1, key2=value2, ......

        Returns
        ----------
        dict
            The dict of invalid fields and the error message. The key is field name or fid according to the passed
            in argument, its value is detailed error message for this field.

        Examples
        ----------
        >>> from refinitiv.data.delivery._dictionary import Dictionary
        >>> dictionary = Dictionary()
        >>> dictionary.load()
        >>> dictionary.validate({"ASK":1.1, "BID": 1.2}, ASKSIZE=100, BIDSIZE=110)
        {
            'ASK': 'Field ASK cannot be found in metadata',
            'ASKSIZE': 'Field ASKSIZE cannot be found in metadata',
            'BID': 'Field BID cannot be found in metadata',
            'BIDSIZE': 110
        }
        """
        if not self.is_field_dict_available:
            raise ValidationException("Metadata not available")

        fields.update(kwargs)
        return validator.get_validated_fields_values(self, fields)

    def is_ripple_to_field(self, field_id: Union[int, str]) -> bool:
        if isinstance(field_id, str) and field_id in self._acronym_to_field_desc:
            field_id = self._acronym_to_field_desc[field_id]

        if isinstance(field_id, int) and field_id in self._fid_to_field_desc:
            return field_id in self._rippled_fields

        return False

    def load(self, dictionary_type: Union[str, DictionaryType] = None, api: str = None) -> None:
        """
        Parameters
        ----------
        dictionary_type: DictionaryType, optional
        api: str, optional
            Specifies the data source. It can be updated/added using config file

        Returns
        -------
        None

        Examples
        ----------
        >>> from refinitiv.data.delivery._dictionary import Dictionary, DictionaryType
        >>> dictionary = Dictionary()
        >>> dictionary.load() # will load all types

        >>> dictionary = Dictionary()
        >>> dictionary.load(DictionaryType.RWF_FLD) # will load only field data
        """
        if not self._session_from_ctor:
            self._session = get_default()
            self._init_logger(self._session.logger())

        load = False

        if dictionary_type == DictionaryType.RWF_FLD or not dictionary_type:
            load = True
            field_stream = create_dictionary_stream(
                ContentType.STREAMING_DICTIONARY,
                domain="Dictionary",
                name=DictionaryType.RWF_FLD,
                api=api,
                session=self._session,
                service=self._service,
            )
            field_stream.on_refresh(self._on_refresh)
            field_stream.open(with_updates=False)
            field_stream.close()

        if dictionary_type == DictionaryType.RWF_ENUM or not dictionary_type:
            load = True
            enum_stream = create_dictionary_stream(
                ContentType.STREAMING_DICTIONARY,
                domain="Dictionary",
                name=DictionaryType.RWF_ENUM,
                api=api,
                session=self._session,
                service=self._service,
            )
            enum_stream.on_refresh(self._on_refresh)
            enum_stream.open(with_updates=False)
            enum_stream.close()

        if not load:
            raise ValueError(f"Nothing to load for {dictionary_type}")

    def _on_refresh(self, stream: "PrvDictionaryStream", message: dict):
        domain = message.get("Domain")
        if domain != "Dictionary":
            return

        message_state = message.get("State", {})
        if message_state.get("Data") != "Ok":
            return

        key = message.get("Key", {})
        if not key or key.get("Name") != stream.name:
            return

        self._fill_dictionary(stream.name, message.get("Series"))

    def _fill_dictionary(self, dictionary_type: Union[str, DictionaryType], series: dict) -> bool:
        if not series:
            return False

        version = series.get("Summary", {}).get("Elements", {}).get("Version")
        if not version:
            return False

        curr_version = self._dict_type_to_version.get(dictionary_type)
        if curr_version is None:
            self._dict_type_to_version[dictionary_type] = version_to_tuple(version)

        else:
            # check if version is newer
            if version_to_tuple(version) <= curr_version:
                return False

        entries = series.get("Entries")
        if not entries:
            return False

        if dictionary_type == DictionaryType.RWF_FLD:
            self._fill_field_dictionary(entries)

        elif dictionary_type == DictionaryType.RWF_ENUM:
            self._fill_enum_type_dictionary(entries)

        return True

    def _fill_field_dictionary(self, entries: List[dict]):
        for elements in entries:
            if not elements:
                continue

            try:
                field_desc = create_field_description(elements["Elements"])
            except KeyError:
                continue

            fid = field_desc.fid
            name = field_desc.name

            if fid not in self._fid_to_field_desc:
                self._fid_to_field_desc[fid] = field_desc
                self._acronym_to_field_desc[name] = field_desc

                if field_desc.ripple_to != 0:
                    self._rippled_fields.add(fid)

    def _fill_enum_type_dictionary(self, entries: List[dict]):
        for elements in entries:
            if not elements:
                continue

            try:
                elements = elements["Elements"]
                fids = elements["FIDS"]["Data"]["Data"]
                enum_type_entry = create_enum_entry(elements["VALUE"]["Data"], elements["DISPLAY"]["Data"])
            except KeyError:
                continue

            for fid in fids:
                self._fid_to_enum_type[fid] = enum_type_entry
