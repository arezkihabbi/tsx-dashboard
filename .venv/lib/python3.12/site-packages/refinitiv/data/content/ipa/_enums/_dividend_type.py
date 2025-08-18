from enum import unique

from ...._base_enum import StrEnum


@unique
class DividendType(StrEnum):
    FORECAST_TABLE = "ForecastTable"
    FORECAST_YIELD = "ForecastYield"
    FUTURES = "Futures"
    HISTORICAL_YIELD = "HistoricalYield"
    IMPLIED_TABLE = "ImpliedTable"
    IMPLIED_YIELD = "ImpliedYield"
    NONE = "None"
