import warnings
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
        Price Side to consider when retrieving Market Data.
    market_data_date : str or date or datetime or timedelta, optional
        The market data date for pricing.
        By default, the market_data_date date is the valuation_date or Today.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). It is set for the fields ending with 'xxxinreportccy'. Optional. The
        default value is the notional currency.
    valuation_date : str or date or datetime or timedelta, optional
        The valuation date for pricing. If not set the valuation date is equal to
        market_data_date or Today. For assets that contains a settlementConvention, the
        default valuation date  is equal to the settlementdate of the Asset that is
        usually the TradeDate+SettlementConvention.

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> rdf.term_deposit.PricingParameters(valuation_date="2020-04-24")
    """

    def __init__(
        self,
        price_side: Union[PriceSide, str] = None,
        income_tax_percent: Optional[float] = None,
        market_data_date: "OptDateTime" = None,
        report_ccy: Optional[str] = None,
        valuation_date: "OptDateTime" = None,
    ):
        if income_tax_percent is not None:
            warnings.warn(
                "The 'income_tax_percent' parameter "
                "for rd.content.ipa.financial_contracts.term_deposit.PricingParameters class "
                "will be removed in future library version v2.0. "
                "This parameter is not supported by the back-end anymore.",
                category=FutureWarning,
            )
        super().__init__()
        self.price_side = price_side
        self.income_tax_percent = income_tax_percent
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.valuation_date = valuation_date

    def _get_items(self):
        return [
            enum_param_item.to_kv("priceSide", self.price_side),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("reportCcy", self.report_ccy),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
        ]
