import asyncio
import time
import warnings
from enum import unique
from typing import Callable, List, Union, TYPE_CHECKING, Optional, Any

from ._data_grid_type import DataGridType, determine_content_type_and_flag, use_field_names_in_headers_arg_parser
from .._content_data import Data
from .._content_provider_layer import ContentUsageLoggerMixin
from .._df_build_type import DFBuildType
from ..._base_enum import StrEnum
from ..._content_type import ContentType
from ..._core.session import get_valid_session
from ..._tools import (
    ArgsParser,
    make_convert_to_enum_arg_parser,
    try_copy_to_list,
    fields_arg_parser,
    universe_arg_parser,
)
from ..._tools import create_repr
from ...delivery._data._data_provider import DataProviderLayer, Response
from ...errors import RDError

if TYPE_CHECKING:
    from ..._types import ExtendedParams, OptDict, StrStrings
    from ..._core.session import Session

MIN_TICKET_DURATION_MS = 15000


@unique
class RowHeaders(StrEnum):
    """Possible values for row headers."""

    DATE = "date"


OptRowHeaders = Optional[Union[str, List[str], RowHeaders, List[RowHeaders]]]

row_headers_enum_arg_parser = make_convert_to_enum_arg_parser(RowHeaders)


def parse_row_headers(value) -> Union[RowHeaders, List[RowHeaders]]:
    if value is None:
        return []

    value = row_headers_enum_arg_parser.parse(value)

    return value


row_headers_arg_parser = ArgsParser(parse_row_headers)


def get_layout(row_headers: List[RowHeaders], content_type: ContentType) -> dict:
    layout = None

    is_rdp = content_type is ContentType.DATA_GRID_RDP
    is_udf = content_type is ContentType.DATA_GRID_UDF

    if is_udf:
        layout = {
            "layout": {
                "columns": [{"item": "dataitem"}],
                "rows": [{"item": "instrument"}],
            }
        }
    elif is_rdp:
        layout = {"output": "Col,T|Va,Row,In|"}

    if RowHeaders.DATE in row_headers:
        if is_udf:
            layout["layout"]["rows"].append({"item": "date"})

        elif is_rdp:
            output = layout["output"]
            output = output[:-1]  # delete forward slash "|"
            output = f"{output},date|"
            layout["output"] = output

    else:
        layout = ""

    if layout is None:
        raise ValueError(f"Layout is None, row_headers={row_headers}, content_type={content_type}")

    return layout


def get_dfbuild_type(row_headers: List[RowHeaders]) -> DFBuildType:
    dfbuild_type = DFBuildType.INDEX

    if RowHeaders.DATE in row_headers:
        dfbuild_type = DFBuildType.DATE_AS_INDEX

    return dfbuild_type


class Definition(ContentUsageLoggerMixin[Response[Data]], DataProviderLayer[Response[Data]]):
    """
    Defines the Fundamental and Reference data to retrieve.

    Parameters:
    ----------
    universe : str or list of str
        Single instrument or list of instruments.
    fields : str or list of str
        Single field or list of fields.
    parameters : dict, optional
        Fields global parameters.
    row_headers : str, list of str, list of RowHeaders enum
        Output/layout parameters to add to the underlying request. Put headers to rows in the response.
    use_field_names_in_headers : bool, optional
        Boolean that indicates whether or not to add field names in the headers.
    extended_params : dict, optional
        Specifies the parameters that will be merged with the request.

    Examples
    --------
    >>> from refinitiv.data.content import fundamental_and_reference
    >>> definition = fundamental_and_reference.Definition(["IBM"], ["TR.Volume"])
    >>> definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    _USAGE_CLS_NAME = "FundamentalAndReference.Definition"

    def __init__(
        self,
        universe: "StrStrings",
        fields: "StrStrings",
        parameters: "OptDict" = None,
        row_headers: OptRowHeaders = None,
        use_field_names_in_headers: bool = None,
        extended_params: "ExtendedParams" = None,
    ):
        if use_field_names_in_headers is None:
            use_field_names_in_headers = False

        else:
            warnings.warn(
                "Parameter 'use_field_names_in_headers' is deprecated and will be removed in future library version v2.0.",
                FutureWarning,
            )

        extended_params = extended_params or {}
        universe = extended_params.get("universe") or try_copy_to_list(universe)
        universe = universe_arg_parser.get_list(universe)
        universe = [value.upper() if value.islower() else value for value in universe]
        self.universe = universe
        self.fields = fields_arg_parser.get_list(try_copy_to_list(fields))

        if parameters is not None and not isinstance(parameters, dict):
            raise ValueError(f"Arg parameters must be a dictionary")

        self.parameters = parameters
        self.use_field_names_in_headers = use_field_names_in_headers_arg_parser.get_bool(use_field_names_in_headers)
        self.extended_params = extended_params
        self.row_headers = try_copy_to_list(row_headers)
        super().__init__(
            data_type=ContentType.DEFAULT,
            universe=self.universe,
            fields=self.fields,
            parameters=self.parameters,
            row_headers=self.row_headers,
            use_field_names_in_headers=self.use_field_names_in_headers,
            extended_params=self.extended_params,
        )

    def _update_content_type(self, session: "Session"):
        content_type, changed = determine_content_type_and_flag(session)
        session._is_debug() and changed and session.debug(
            f"UDF DataGrid service cannot be used with platform sessions, RDP DataGrid will be used instead. "
            f"The \"/apis/data/datagrid/underlying-platform = '{DataGridType.UDF}'\" "
            f"parameter will be discarded, meaning that the regular RDP DataGrid "
            f"service will be used for Fundamental and Reference data requests."
        )
        self._initialize(content_type, **self._kwargs)
        row_headers = self._kwargs.get("row_headers")
        row_headers = row_headers_arg_parser.get_list(row_headers)
        layout = get_layout(row_headers, content_type)
        dfbuild_type = get_dfbuild_type(row_headers)
        self._kwargs["layout"] = layout
        self._kwargs["__dfbuild_type__"] = dfbuild_type

    @staticmethod
    def make_on_response(callback: Callable) -> Callable:
        def on_response(response, data_provider, session):
            if response and response.data and response.data.raw.get("ticket"):
                return
            callback(response, data_provider, session)

        return on_response

    @staticmethod
    def _get_duration(raw: dict) -> int:
        """
        Compute the duration to sleep before next retry to request ticket status

        Parameters
        ----------
        raw : dict
            e.g. {"estimatedDuration": 44000, "ticket": "78BF26B24A9D416E"}

        Raises
        ------
        RDError
            If raw does not contain "estimatedDuration"

        Returns
        -------
        int
            Duration in seconds
        """
        estimated_duration_ms = raw.get("estimatedDuration")
        if estimated_duration_ms:
            duration_sec = min(estimated_duration_ms, MIN_TICKET_DURATION_MS) // 1000
            return duration_sec

        raise RDError(-1, "Received a ticket response from DataGrid without estimatedDuration")

    def get_data(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
    ):
        """
        Sends a request to the Refinitiv Data Platform to retrieve the data.

        Parameters
        ----------
        session : Session, optional
            Session object. If it's not passed the default session will be used.
        on_response : Callable, optional
            User-defined callback function to process received response.

        Returns
        -------
        Response

        Raises
        ------
        AttributeError
            If user didn't set default session.
        """
        session = get_valid_session(session)
        self._update_content_type(session)

        if self._content_type == ContentType.DATA_GRID_UDF:
            on_response_filter = on_response and self.make_on_response(on_response)
            response = super().get_data(session, on_response_filter)
            raw = response.data.raw
            ticket = raw.get("ticket")

            while ticket:
                time.sleep(self._get_duration(raw))
                self._kwargs["ticket"] = ticket
                response = super().get_data(session, on_response_filter)
                raw = response.data.raw
                ticket = raw.get("ticket")

        else:
            response = super().get_data(session, on_response)

        return response

    async def get_data_async(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
        closure: Optional[Any] = None,
    ):
        """
        Sends an asynchronous request to the Refinitiv Data Platform to retrieve the data.

        Parameters
        ----------
        session : Session, optional
            Session object. If it's not passed the default session will be used.
        on_response : Callable, optional
            User-defined callback function to process received response.
        closure : any, optional
            Optional closure that will be passed to the headers and returned

        Returns
        -------
        Response

        Raises
        ------
        AttributeError
            If user didn't set default session.

        """
        session = get_valid_session(session)
        self._update_content_type(session)

        if self._content_type == ContentType.DATA_GRID_UDF:
            on_response_filter = on_response and self.make_on_response(on_response)
            response = await super().get_data_async(session, on_response_filter, closure)
            raw = response.data.raw
            ticket = raw.get("ticket")

            while ticket:
                await asyncio.sleep(self._get_duration(raw))
                self._kwargs["ticket"] = ticket
                response = await super().get_data_async(session, on_response_filter, closure)
                raw = response.data.raw
                ticket = raw.get("ticket")

        else:
            response = await super().get_data_async(session, on_response, closure)

        return response

    def __repr__(self):
        return create_repr(
            self,
            content=f"{{"
            f"universe='{self.universe}', "
            f"fields='{self.fields}', "
            f"parameters='{self.parameters}', "
            f"row_headers='{self.row_headers}'"
            f"}}",
        )
