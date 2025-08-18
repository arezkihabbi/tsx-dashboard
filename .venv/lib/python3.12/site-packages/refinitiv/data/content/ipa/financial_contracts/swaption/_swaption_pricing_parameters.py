from typing import Optional, Union

from ..._enums import PriceSide
from ..._param_item import enum_param_item, datetime_param_item, param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class PricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    price_side : PriceSide or str, optional
        The quoted price side of the instrument. optional. default value is 'mid'.
    exercise_date : str or date or datetime or timedelta, optional

    market_data_date : str or date or datetime or timedelta, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    market_value_in_deal_ccy : float, optional
        The market value of the instrument. the value is expressed in the deal currency.
        optional. no default value applies. note that premium takes priority over
        volatility input.
    nb_iterations : int, optional
        The number of steps for the bermudan swaption pricing via the hull-white
        one-factor (hw1f) tree.  no default value applies.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    simulate_exercise : bool, optional
        Tells if in case of future cashflows should be considered as exercised or not.
        possible values:    true,    false.
    valuation_date : str or date or datetime or timedelta, optional
        The valuation date for pricing. If not set the valuation date is equal to
        market_data_date or Today. For assets that contains a settlementConvention,
        the default valuation date  is equal to the settlementdate of the Asset that is
        usually the TradeDate+SettlementConvention.

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> rdf.swaption.PricingParameters(valuation_date="2020-04-24", nb_iterations=80)
    """

    def __init__(
        self,
        price_side: Union[PriceSide, str] = None,
        exercise_date: "OptDateTime" = None,
        market_data_date: "OptDateTime" = None,
        market_value_in_deal_ccy: Optional[float] = None,
        nb_iterations: Optional[int] = None,
        report_ccy: Optional[str] = None,
        simulate_exercise: Optional[bool] = None,
        valuation_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.price_side = price_side
        self.exercise_date = exercise_date
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.nb_iterations = nb_iterations
        self.report_ccy = report_ccy
        self.simulate_exercise = simulate_exercise
        self.valuation_date = valuation_date

    def _get_items(self):
        return [
            enum_param_item.to_kv("priceSide", self.price_side),
            datetime_param_item.to_kv("exerciseDate", self.exercise_date),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("marketValueInDealCcy", self.market_value_in_deal_ccy),
            param_item.to_kv("nbIterations", self.nb_iterations),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv("simulateExercise", self.simulate_exercise),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
        ]
