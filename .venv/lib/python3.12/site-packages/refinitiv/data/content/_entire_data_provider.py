import abc
from datetime import timedelta
from typing import Callable, List, Any, Optional, TYPE_CHECKING

from ._content_data_factory import ContentDataFactory
from ._df_builder import build_empty_df
from .._content_type import ContentType
from .._tools import hp_datetime_adapter
from ..content._intervals import (
    interval_arg_parser,
    get_day_interval_type,
    DayIntervalType,
    Intervals,
)
from ..delivery._data._data_provider import Response

if TYPE_CHECKING:
    from ..delivery._data._response import Response

INTERVALS_BY_SECONDS = {
    Intervals.ONE_MINUTE: 59,
    Intervals.FIVE_MINUTES: 299,
    Intervals.TEN_MINUTES: 599,
    Intervals.THIRTY_MINUTES: 1799,
    Intervals.SIXTY_MINUTES: 3599,
    Intervals.HOURLY: 3599,
}

EVENTS_MAX_LIMIT = 10000


def remove_last_date_elements(data: List[List[Any]]) -> List[List[Any]]:
    end_date = data[-1][0]
    for index, item in enumerate(data[::-1]):
        if item[0] != end_date:
            data = data[:-index]
            return data

    return data


class EntireDataProvider(abc.ABC):
    @abc.abstractmethod
    def request_with_dates(self, *args) -> Response:
        pass

    @abc.abstractmethod
    def request_with_count(self, *args) -> Response:
        pass

    @abc.abstractmethod
    def get_request_function(self, **kwargs) -> Optional[Callable]:
        pass

    @abc.abstractmethod
    def get_request_function_async(self, **kwargs) -> Optional[Callable]:
        pass

    def get_data(self, provide_data: Callable, **kwargs) -> Response:
        request_function = self.get_request_function(**kwargs)

        if request_function:
            response = request_function(provide_data, **kwargs)

        else:
            response = provide_data(**kwargs)

        return response

    async def get_data_async(self, provide_data: Callable, **kwargs) -> Response:
        request_function = self.get_request_function_async(**kwargs)

        if request_function:
            response = await request_function(provide_data, **kwargs)

        else:
            response = await provide_data(**kwargs)

        return response


class SummariesEntireDataProvider(EntireDataProvider):
    def request_with_dates(
        self,
        provide_data: Callable,
        interval,
        start: str,
        end: str,
        count: Optional[int] = None,
        **kwargs,
    ) -> Response:
        interval_sec = INTERVALS_BY_SECONDS[interval_arg_parser.get_str(interval)]

        entire_data = []
        responses = []
        unique_data_count = set()
        last_raw = {}

        finished_date = hp_datetime_adapter.get_localize(start)
        # need do ... while
        end_date = finished_date + timedelta(microseconds=1)

        while end_date > finished_date and len(unique_data_count) <= 1:
            response = provide_data(
                interval=interval,
                count=count,
                start=start,
                end=end,
                **kwargs,
            )
            responses.append(response)

            if not response.is_success:
                break

            raw = response.data.raw
            last_raw = raw
            if len(raw) == 0 or not raw.get("data"):
                break

            data = list(raw["data"])
            entire_data.extend(data)

            if count is not None and len(entire_data) >= count:
                entire_data = entire_data[:count]
                break

            unique_data_count.add(len(data))

            end_date = data[-1][0]
            end = end_date
            end_date = hp_datetime_adapter.get_localize(end_date)

            if (end_date - finished_date).seconds < interval_sec:
                break

        return entire_create_response(
            responses,
            last_raw,
            entire_data,
            kwargs,
        )

    async def request_with_dates_async(
        self,
        provide_data: Callable,
        interval,
        start: str,
        end: str,
        count: Optional[int] = None,
        **kwargs,
    ) -> Response:
        interval_sec = INTERVALS_BY_SECONDS[interval_arg_parser.get_str(interval)]

        entire_data = []
        responses = []
        unique_data_count = set()
        last_raw = {}

        finished_date = hp_datetime_adapter.get_localize(start)
        # need do ... while
        end_date = finished_date + timedelta(microseconds=1)

        while end_date > finished_date and len(unique_data_count) <= 1:
            response = await provide_data(
                interval=interval,
                count=count,
                start=start,
                end=end,
                **kwargs,
            )
            responses.append(response)

            if not response.is_success:
                break

            raw = response.data.raw
            last_raw = raw
            if len(raw) == 0 or not raw.get("data"):
                break

            data = list(raw["data"])
            entire_data.extend(data)

            if count is not None and len(entire_data) >= count:
                entire_data = entire_data[:count]
                break

            unique_data_count.add(len(data))

            end_date = data[-1][0]
            end = end_date
            end_date = hp_datetime_adapter.get_localize(end_date)

            if (end_date - finished_date).seconds < interval_sec:
                break

        return entire_create_response(
            responses,
            last_raw,
            entire_data,
            kwargs,
        )

    def request_with_count(
        self,
        provide_data: Callable,
        interval,
        count: int,
        end: str,
        start: Optional[str] = None,
        **kwargs,
    ) -> Response:
        interval_sec = INTERVALS_BY_SECONDS[interval_arg_parser.get_str(interval)]

        c = count
        entire_data = []
        responses = []
        unique_data_count = set()
        last_raw = {}

        finished_date = None
        if start:
            finished_date = hp_datetime_adapter.get_localize(start)

        while c > 0 and len(unique_data_count) <= 1:
            response = provide_data(
                interval=interval,
                count=count,
                start=start,
                end=end,
                **kwargs,
            )
            responses.append(response)

            if not response.is_success:
                break

            raw = response.data.raw
            last_raw = raw
            if len(raw) == 0 or not raw.get("data"):
                break

            data = list(raw["data"])
            entire_data.extend(data)

            unique_data_count.add(len(data))

            c -= len(data)
            count = c
            end_date = data[-1][0]
            end = end_date

            if finished_date:
                end_date = hp_datetime_adapter.get_localize(end_date)

                if (end_date - finished_date).seconds < interval_sec:
                    break

        return entire_create_response(
            responses,
            last_raw,
            entire_data,
            kwargs,
        )

    async def request_with_count_async(
        self,
        provide_data: Callable,
        interval,
        count: int,
        end: str,
        start: Optional[str] = None,
        **kwargs,
    ) -> Response:
        interval_sec = INTERVALS_BY_SECONDS[interval_arg_parser.get_str(interval)]

        c = count
        entire_data = []
        responses = []
        unique_data_count = set()
        last_raw = {}

        finished_date = None
        if start:
            finished_date = hp_datetime_adapter.get_localize(start)

        while c > 0 and len(unique_data_count) <= 1:
            response = await provide_data(
                interval=interval,
                count=count,
                start=start,
                end=end,
                **kwargs,
            )
            responses.append(response)

            if not response.is_success:
                break

            raw = response.data.raw
            last_raw = raw
            if len(raw) == 0 or not raw.get("data"):
                break

            data = list(raw["data"])
            entire_data.extend(data)

            unique_data_count.add(len(data))

            c -= len(data)
            count = c
            end_date = data[-1][0]
            end = end_date

            if finished_date:
                end_date = hp_datetime_adapter.get_localize(end_date)

                if (end_date - finished_date).seconds < interval_sec:
                    break

        return entire_create_response(
            responses,
            last_raw,
            entire_data,
            kwargs,
        )

    def get_request_function(
        self,
        interval,
        count: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        **kwargs,
    ) -> Optional[Callable]:
        request_function = None

        if interval is None or get_day_interval_type(interval) is not DayIntervalType.INTRA:
            return request_function

        if start is not None and end is not None:
            request_function = self.request_with_dates

        elif count is not None and count > 0:
            request_function = self.request_with_count

        return request_function

    def get_request_function_async(
        self,
        interval,
        count: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        **kwargs,
    ) -> Optional[Callable]:
        request_function = None

        if interval is None or get_day_interval_type(interval) is not DayIntervalType.INTRA:
            return request_function

        if start is not None and end is not None:
            request_function = self.request_with_dates_async

        elif count is not None and count > 0:
            request_function = self.request_with_count_async

        return request_function


class EventsEntireDataProvider(EntireDataProvider):
    def request_with_dates(
        self,
        provide_data: Callable,
        start: str,
        end: str,
        count: Optional[int] = None,
        **kwargs,
    ) -> Response:
        entire_data = []
        responses = []
        last_raw = {}

        finished_date = hp_datetime_adapter.get_localize(start)
        # need do ... while
        end_date = finished_date + timedelta(microseconds=1)
        response_count = EVENTS_MAX_LIMIT

        while end_date > finished_date and response_count >= EVENTS_MAX_LIMIT:
            response = provide_data(count=count, start=start, end=end, **kwargs)
            responses.append(response)

            if not response.is_success:
                break

            raw = response.data.raw
            last_raw = raw
            if len(raw) == 0 or not raw.get("data"):
                break

            data = list(raw["data"])

            response_count = len(data)
            if response_count >= EVENTS_MAX_LIMIT:
                data = remove_last_date_elements(data)

            entire_data.extend(data)

            end_date = data[-1][0]
            end = end_date
            end_date = hp_datetime_adapter.get_localize(end_date)

            if count is not None and len(entire_data) >= count:
                entire_data = entire_data[:count]
                break

        return entire_create_response(
            responses,
            last_raw,
            entire_data,
            kwargs,
        )

    async def request_with_dates_async(
        self,
        provide_data: Callable,
        start: str,
        end: str,
        count: Optional[int] = None,
        **kwargs,
    ) -> Response:
        entire_data = []
        responses = []
        last_raw = {}

        finished_date = hp_datetime_adapter.get_localize(start)
        # need do ... while
        end_date = finished_date + timedelta(microseconds=1)
        response_count = EVENTS_MAX_LIMIT

        while end_date > finished_date and response_count >= EVENTS_MAX_LIMIT:
            response = await provide_data(count=count, start=start, end=end, **kwargs)
            responses.append(response)

            if not response.is_success:
                break

            raw = response.data.raw
            last_raw = raw
            if len(raw) == 0 or not raw.get("data"):
                break

            data = list(raw["data"])

            response_count = len(data)
            if response_count >= EVENTS_MAX_LIMIT:
                data = remove_last_date_elements(data)

            entire_data.extend(data)

            end_date = data[-1][0]
            end = end_date
            end_date = hp_datetime_adapter.get_localize(end_date)

            if count is not None and len(entire_data) >= count:
                entire_data = entire_data[:count]
                break

        return entire_create_response(
            responses,
            last_raw,
            entire_data,
            kwargs,
        )

    def request_with_count(self, provide_data: Callable, count: int, start: str, end: str, **kwargs) -> Response:
        entire_data = []
        responses = []
        c = count
        response_count = EVENTS_MAX_LIMIT
        last_raw = {}

        while c > 0 and response_count >= EVENTS_MAX_LIMIT:
            response = provide_data(count=count, start=start, end=end, **kwargs)
            responses.append(response)

            if not response.is_success:
                break

            raw = response.data.raw
            last_raw = raw
            if len(raw) == 0 or not raw.get("data"):
                break

            data = list(raw["data"])

            response_count = len(data)
            if response_count >= EVENTS_MAX_LIMIT:
                data = remove_last_date_elements(data)

            entire_data.extend(data)

            c -= len(data)
            count = c
            end_date = data[-1][0]
            end = end_date

        return entire_create_response(
            responses,
            last_raw,
            entire_data,
            kwargs,
        )

    async def request_with_count_async(
        self, provide_data: Callable, count: int, start: str, end: str, **kwargs
    ) -> Response:
        entire_data = []
        responses = []
        c = count
        response_count = EVENTS_MAX_LIMIT
        last_raw = {}

        while c > 0 and response_count >= EVENTS_MAX_LIMIT:
            response = await provide_data(count=count, start=start, end=end, **kwargs)
            responses.append(response)

            if not response.is_success:
                break

            raw = response.data.raw
            last_raw = raw
            if len(raw) == 0 or not raw.get("data"):
                break

            data = list(raw["data"])

            response_count = len(data)
            if response_count >= EVENTS_MAX_LIMIT:
                data = remove_last_date_elements(data)

            entire_data.extend(data)

            c -= len(data)
            count = c
            end_date = data[-1][0]
            end = end_date

        return entire_create_response(
            responses,
            last_raw,
            entire_data,
            kwargs,
        )

    def get_request_function(
        self,
        count: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        **kwargs,
    ) -> Optional[Callable]:
        request_function = None

        if start is not None and end is not None:
            request_function = self.request_with_dates

        elif count is not None and count > EVENTS_MAX_LIMIT:
            request_function = self.request_with_count

        return request_function

    def get_request_function_async(
        self,
        count: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        **kwargs,
    ) -> Optional[Callable]:
        request_function = None

        if start is not None and end is not None:
            request_function = self.request_with_dates_async

        elif count is not None and count > EVENTS_MAX_LIMIT:
            request_function = self.request_with_count_async

        return request_function


entire_data_provider_by_content_type = {
    ContentType.HISTORICAL_PRICING_EVENTS: EventsEntireDataProvider(),
    ContentType.CUSTOM_INSTRUMENTS_EVENTS: EventsEntireDataProvider(),
    ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES: SummariesEntireDataProvider(),
    ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES: SummariesEntireDataProvider(),
    ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES: SummariesEntireDataProvider(),
    ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES: SummariesEntireDataProvider(),
}


class EntireDataFactory(ContentDataFactory):
    def get_dfbuilder(self, **__):
        return build_empty_df


multi_entire_data_factory = EntireDataFactory()


def get_entire_data_provider(content_type: ContentType) -> EntireDataProvider:
    entire_data_provider = entire_data_provider_by_content_type.get(content_type)

    if not entire_data_provider:
        raise ValueError(f"Cannot find entire data provider for {content_type}")

    return entire_data_provider


def entire_create_response(responses: List["Response"], last_raw: dict, entire_data: list, kwargs) -> Response:
    _raw = dict(last_raw)
    _raw["data"] = entire_data

    raw = []
    request_messages = []
    http_responses = []
    http_statuses = []
    http_headers = []
    errors = []
    is_success = False

    for response in responses:
        is_success = is_success or response.is_success
        if response.errors:
            errors += response.errors

        raw.append(response.raw)

        # will remove
        http_responses.extend(response._http_response)
        request_messages.extend(response._request_message)
        http_statuses.extend(response._http_status)
        http_headers.extend(response._http_headers)

    return Response(
        is_success=is_success,
        raw=http_responses,
        errors=errors,
        closure=None,
        requests_count=len(responses),
        _data_factory=multi_entire_data_factory,
        _kwargs=kwargs,
        _raw=_raw,
        _request_message=request_messages,
        _http_response=http_responses,
        _http_headers=http_headers,
        _http_status=http_statuses,
    )
