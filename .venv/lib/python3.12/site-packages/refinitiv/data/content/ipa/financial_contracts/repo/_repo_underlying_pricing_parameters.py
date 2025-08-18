from typing import Optional

from ._repo_parameters import RepoParameters
from ..bond import PricingParameters as BondPricingParameters
from ..._param_item import serializable_param_item, datetime_param_item, param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class UnderlyingPricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    pricing_parameters_at_end : BondPricingParameters, optional

    pricing_parameters_at_start : BondPricingParameters, optional

    repo_parameters : RepoParameters, optional

    market_data_date : str or date or datetime or timedelta, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    valuation_date : str or date or datetime or timedelta, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    """

    def __init__(
        self,
        pricing_parameters_at_end: Optional[BondPricingParameters] = None,
        pricing_parameters_at_start: Optional[BondPricingParameters] = None,
        repo_parameters: Optional[RepoParameters] = None,
        market_data_date: "OptDateTime" = None,
        report_ccy: Optional[str] = None,
        valuation_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.pricing_parameters_at_end = pricing_parameters_at_end
        self.pricing_parameters_at_start = pricing_parameters_at_start
        self.repo_parameters = repo_parameters
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.valuation_date = valuation_date

    def _get_items(self):
        return [
            serializable_param_item.to_kv("pricingParametersAtEnd", self.pricing_parameters_at_end),
            serializable_param_item.to_kv("pricingParametersAtStart", self.pricing_parameters_at_start),
            serializable_param_item.to_kv("repoParameters", self.repo_parameters),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("reportCcy", self.report_ccy),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
        ]
