import asyncio
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor, wait
from functools import partial
from typing import List, TYPE_CHECKING, Any, Callable, Dict

from ._content_data_factory import ContentDataFactory
from ._content_data_provider import ContentDataProvider
from ._entire_data_provider import get_entire_data_provider
from ._intervals import DayIntervalType, get_day_interval_type
from .._errors import RDError
from .._tools import fields_arg_parser
from ..delivery._data._data_provider import Response
from ..delivery._data._response import create_response

if TYPE_CHECKING:
    import pandas as pd
    from ._content_data import Data
    from ._historical_df_builder import HistoricalBuilder


def copy_fields(fields: List[str]) -> List[str]:
    if fields is None:
        return []

    if not isinstance(fields, (list, str)):
        raise AttributeError(f"fields not support type {type(fields)}")
    fields = fields_arg_parser.get_list(fields)

    return fields[:]


def get_first_success_response(responses: List[Response]) -> Response:
    successful = (response for response in responses if response.is_success)
    first_successful = next(successful, None)
    return first_successful


def validate_responses(responses: List[Response]):
    response = get_first_success_response(responses)

    if response is None:
        error_message = "ERROR: No successful response.\n"

        error_codes = set()

        for response in responses:
            if response.errors:
                error = response.errors[0]

                if error.code not in error_codes:
                    error_codes.add(error.code)
                    sub_error_message = error.message

                    if "." in error.message:
                        sub_error_message, _ = error.message.split(".", maxsplit=1)

                    error_message += f"({error.code}, {sub_error_message}), "

        error_message = error_message[:-2]
        error = RDError(1, f"No data to return, please check errors: {error_message}")
        error.response = responses
        raise error


class HistoricalDataFactoryMultiResponse(ContentDataFactory):
    def get_dfbuilder(
        self, responses: List[Response] = None, **kwargs
    ) -> Callable[[Any, Dict[str, Any]], "pd.DataFrame"]:
        df_builder: "HistoricalBuilder" = super().get_dfbuilder(**kwargs)

        if len(responses) == 1:
            return df_builder.build_one

        else:
            return df_builder.build

    def create_data_success(self, raw: Any, **kwargs) -> "Data":
        responses: List[Response] = kwargs.get("responses")

        if responses is None:
            raise ValueError("Cannot get df_builder, responses in None.")

        if len(responses) == 1:
            raw = raw[0]

        return self.data_class(raw=raw, _dfbuilder=self.get_dfbuilder(**kwargs), _kwargs=kwargs)


class HistoricalDataProvider(ContentDataProvider):
    data_factory_multi_response = HistoricalDataFactoryMultiResponse()

    @abstractmethod
    def _get_axis_name(self, interval, **kwargs) -> str:
        # for override
        pass

    def get_data(self, *args, **kwargs) -> Response:
        universe: List[str] = kwargs.pop("universe", [])
        entire_data_provider = get_entire_data_provider(kwargs.get("__content_type__"))

        with ThreadPoolExecutor(thread_name_prefix="HistoricalRequestThread") as ex:
            futures = []
            for inst_name in universe:
                fut = ex.submit(
                    entire_data_provider.get_data,
                    partial(super().get_data, *args),
                    universe=inst_name,
                    **kwargs,
                )
                futures.append(fut)

            wait(futures)

            responses = []
            for fut in futures:
                exception = fut.exception()

                if exception:
                    raise exception

                response = fut.result()
                responses.append(response)

        validate_responses(responses)

        kwargs["responses"] = responses
        kwargs["universe"] = universe
        kwargs["fields"] = copy_fields(kwargs.get("fields"))
        kwargs["axis_name"] = self._get_axis_name(kwargs.get("interval"))
        return create_response(responses, self.data_factory_multi_response, kwargs)

    async def get_data_async(self, *args, **kwargs) -> Response:
        universe: List[str] = kwargs.pop("universe", [])
        entire_data_provider = get_entire_data_provider(kwargs.get("__content_type__"))

        tasks = []
        for inst_name in universe:
            tasks.append(
                entire_data_provider.get_data_async(
                    partial(super().get_data_async, *args), universe=inst_name, **kwargs
                )
            )

        responses = await asyncio.gather(*tasks)

        kwargs["responses"] = responses
        kwargs["universe"] = universe
        kwargs["fields"] = copy_fields(kwargs.get("fields"))
        kwargs["axis_name"] = self._get_axis_name(kwargs.get("interval"))
        return create_response(responses, self.data_factory_multi_response, kwargs)


field_timestamp_by_day_interval_type = {
    DayIntervalType.INTER: "DATE",
    DayIntervalType.INTRA: "DATE_TIME",
}

axis_by_day_interval_type = {
    DayIntervalType.INTRA: "Timestamp",
    DayIntervalType.INTER: "Date",
}


def get_fields_events(fields, **kwargs):
    fields = fields_arg_parser.get_list(fields)
    result = copy_fields(fields)
    field_timestamp = "DATE_TIME"

    if field_timestamp not in result:
        result.append(field_timestamp)
    return ",".join(result)


def get_fields_summaries(fields, **kwargs):
    fields = fields_arg_parser.get_list(fields)
    result = copy_fields(fields)
    interval = kwargs.get("interval")
    field_timestamp = field_timestamp_by_day_interval_type.get(get_day_interval_type(interval or DayIntervalType.INTER))
    if field_timestamp not in result:
        result.append(field_timestamp)
    return ",".join(result)


class SummariesDataProvider(HistoricalDataProvider):
    def _get_axis_name(self, interval, **kwargs):
        axis_name = axis_by_day_interval_type.get(get_day_interval_type(interval or DayIntervalType.INTER))
        return axis_name


class EventsDataProvider(HistoricalDataProvider):
    def _get_axis_name(self, interval, **kwargs):
        return "Timestamp"
