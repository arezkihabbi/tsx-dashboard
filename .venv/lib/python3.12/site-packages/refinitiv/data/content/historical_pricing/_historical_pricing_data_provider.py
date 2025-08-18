from ._historical_pricing_request_factory import (
    HistoricalPricingEventsRequestFactory,
    HistoricalPricingSummariesRequestFactory,
)
from .._historical_content_validator import HistoricalContentValidator
from .._historical_data_provider import (
    EventsDataProvider,
    SummariesDataProvider,
)
from .._historical_response_factory import HistoricalResponseFactory

hp_events_data_provider = EventsDataProvider(
    request=HistoricalPricingEventsRequestFactory(),
    response=HistoricalResponseFactory(),
    validator=HistoricalContentValidator(),
)

hp_summaries_data_provider = SummariesDataProvider(
    request=HistoricalPricingSummariesRequestFactory(),
    response=HistoricalResponseFactory(),
    validator=HistoricalContentValidator(),
)
