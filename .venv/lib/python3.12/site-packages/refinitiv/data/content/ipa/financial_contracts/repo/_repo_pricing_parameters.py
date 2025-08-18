from typing import Optional, Union

from ..._enums import RepoCurveType
from ..._param_item import enum_param_item, datetime_param_item, param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class PricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    repo_curve_type : RepoCurveType or str, optional
        Curve used to compute the repo rate. it can be computed using following methods:
        - repocurve : rate is computed by interpolating a repo curve.     - depositcurve
        : rate is computed by interpolating a deposit curve.     - fixinglibor : rate is
        computed by interpolating libor rates.  if no curve can be found, the rate is
        computed using a deposit curve.
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
        repo_curve_type: Union[RepoCurveType, str] = None,
        market_data_date: "OptDateTime" = None,
        report_ccy: Optional[str] = None,
        valuation_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.repo_curve_type = repo_curve_type
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.valuation_date = valuation_date

    def _get_items(self):
        return [
            enum_param_item.to_kv("repoCurveType", self.repo_curve_type),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("reportCcy", self.report_ccy),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
        ]
