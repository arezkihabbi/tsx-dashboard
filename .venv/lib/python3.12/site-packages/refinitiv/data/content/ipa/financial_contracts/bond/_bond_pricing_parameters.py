from typing import Optional, Union

from ..._enums import (
    DividendType,
    ProjectedIndexCalculationMethod,
    CreditSpreadType,
    PriceSide,
    RedemptionDateType,
    VolatilityType,
    VolatilityTermStructureType,
    BenchmarkYieldSelectionMode,
    YieldType,
    QuoteFallbackLogic,
    InflationMode,
)
from ..._models import BondRoundingParameters
from ..._param_item import enum_param_item, serializable_param_item, param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class PricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    trade_date : str or date or datetime or timedelta, optional
        Trade date of the bond. The trade_date is used to compute the default
        valuation_date : By default the rule is that valuation_date = trade_date +
        settlement_convention. Optional. By default, it is equal to market_data_date.
    benchmark_yield_selection_mode : BenchmarkYieldSelectionMode or str, optional
        The benchmark yield.
        Default value is "Interpolate".
    credit_spread_type : CreditSpreadType or str, optional
        Credit curve spread type to use during pricing. Applicable for Convertible
        Bonds.
    dividend_type : DividendType or str, optional
        Underlying stock dividend type used during pricing convertible bond. Applicable
        for Convertible Bonds.
    fx_price_side : PriceSide or str, optional
        FX price side to consider when retrieving FX rates (Mid, Bid, Ask, Last, Close)
    inflation_mode : InflationMode or str, optional
        The indicator used to define whether instrument parameters should be adjusted
        from inflation or not. Available only for inflation-linked instruments.
        optional. By default, 'default' is used. That means it depends on the instrument
        quotation convention.
    price_side : PriceSide or str, optional
        Quoted price side of the bond to use for pricing Analysis: Bid(Bid value),
        Ask(Ask value), Mid(Mid value) Optional. By default the "Mid" price of the bond
        is used.
    projected_index_calculation_method : ProjectedIndexCalculationMethod or str, optional
        Flag used to define how projected index is computed.
        Default value is "ConstantIndex". It is defaulted to "ForwardIndex"
        for Preferreds and Brazilian Debenture bonds.
    quote_fallback_logic : QuoteFallbackLogic or str, optional
        Enumeration used to define the fallback logic for the quotation of the
        instrument.
    redemption_date_type : RedemptionDateType or str, optional
        Redemption type of the bond. It is used to compute the default redemption date.
        Default value is "RedemptionAtWorstDate" for callable bond,
        "RedemptionAtBestDate" for puttable bond or "RedemptionAtMaturityDate".
    rounding_parameters : BondRoundingParameters, optional
        Definition of rounding parameters to be applied on accrued, price or yield.
        By default, rounding parameters are the ones defined in the bond structure.
    volatility_term_structure_type : VolatilityTermStructureType or str, optional
        Stock volatility trem structure type to use during pricing. Applicable for
        Convertible Bonds.
    volatility_type : VolatilityType or str, optional
        Volatility type to use during pricing. Applicable for Convertible Bonds.
    yield_type : YieldType or str, optional
        yield_type that specifies the rate structure.
        The default value is Native.
    adjusted_clean_price : float, optional
        Inflation Adjusted Clean price to override and that will be used as pricing
        analysis input. The currency of the clean price is the cash flow currency (that
        can be different to deal currency especially if "ComputeCashFlowWithReportCcy"
        flag has been set to true). No override is applied by default. Note that only
        one pricing analysis input should be defined.
    adjusted_dirty_price : float, optional
        Inflation Adjusted Dirty price to override and that will be used as pricing
        analysis input. The currency of the dirty price is the cash flow currency (that
        can be different to deal currency especially if "ComputeCashFlowWithReportCcy"
        flag has been set to true). No override is applied by default. Note that only
        one pricing analysis input should be defined.
    adjusted_yield_percent : float, optional
        Inflation Adjusted Yield (expressed in percent) to override and that will be
        used as pricing analysis input. No override is applied by default.
        Note that only one pricing analysis input should be defined.
    apply_tax_to_full_pricing : bool, optional
        Tax Parameters Flag to set these tax parameters for all
        pricing/schedule/risk/spread.
        By default Tax Params are applied only to Muni.
    asset_swap_spread_bp : float, optional
        AssetSwapSpread to override and that will be used as pricing analysis input to
        compute the bond price. No override is applied by default. Note that
        only one pricing anlysis input should be defined.
    benchmark_at_issue_price : float, optional
        Price of benchmark at issue to override and that will be used to compute
        benchmark at redemption spread. No override is applied by default and
        price is computed or retrieved from market data.
    benchmark_at_issue_ric : str, optional
        Ric of benchmark at issue to override and that will be used as pricing analysis
        input to compute the bond price. Optional. No override is applied by default.
        Note that only one pricing analysis input should be defined.
    benchmark_at_issue_spread_bp : float, optional
        Spread of benchmark at issue to override and that will be used as pricing
        analysis input to compute the bond price. No override is applied by
        default. Note that only one pricing analysis input should be defined.
    benchmark_at_issue_yield_percent : float, optional
        Yield of benchmark at issue to override and that will be used to compute
        benchmark at redemption spread. No override is applied by default and
        yield is computed or retrieved from market data.
    benchmark_at_redemption_price : float, optional
        Price of benchmark at redemption to override and that will be used to compute
        benchmark at redemption spread. No override is applied by default and
        price is computed or retrieved from market data.
    benchmark_at_redemption_spread_bp : float, optional
        Spread of benchmark at redemption to override and that will be used as pricing
        analysis input to compute the bond price. No override is applied by
        default. Note that only one pricing analysis input should be defined.
    benchmark_at_redemption_yield_percent : float, optional
        Yield of benchmark at redemption to override and that will be used to compute
        benchmark at redemption spread. No override is applied by default and
        yield is computed or retrieved from market data.
    bond_recovery_rate_percent : float, optional
        Bond Recovery Rate Percent set for convertible bond. Applicable for Convertible
        Bonds.
    cash_amount : float, optional
        Cash amount to override and that will be used as pricing analysis input.
        No override is applied by default. Note that only one pricing analysis
        input should be defined.
    cds_recovery_rate_percent : float, optional
        Recovery rate percent used in credit curve related to convertible. Applicable
        for Convertible Bonds.
    clean_price : float, optional
        Clean price to override and that will be used as pricing analysis input. The
        currency of the clean price is the cash flow currency (that can be different to
        deal currency especially if "ComputeCashFlowWithReportCcy" flag has been set to
        true). No override is applied by default. Note that only one pricing analysis
        input should be defined.
    compute_cash_flow_from_issue_date : bool, optional
        The indicator defines the date, from which the cash flows will be computed. The
        possible values are:
        - true: from issuedate,
        - false: from tradedate. optional. default value is 'false'.
    compute_cash_flow_with_report_ccy : bool, optional
        The indicator used to express the instrument cash flows in the report currency.
        The possible values are:
        - true: the pricing will be done in the reporting currency using a fx forward
          curve,
        - false: the pricing will be done using notional currency. Optional. Default
          value is 'false'.
    concession_fee : float, optional
        Fee to apply to the bond price; It is expressed in the same unit that the bond
        price (percent or cash).
    current_yield_percent : float, optional
        Current Yield (expressed in percent) to override and that will be used as
        pricing analysis input. No override is applied by default. Note that
        only one pricing anlysis input should be defined.
    dirty_price : float, optional
        Dirty price to override and that will be used as pricing analysis input. The
        currency of the dirty price is the cash flow currency (that can be different to
        deal currency especially if "ComputeCashFlowWithReportCcy" flag has been set to
        true). No override is applied by default. Note that only one pricing analysis
        input should be defined.
    discount_margin_bp : float, optional
        Discount Margin basis points to override and that will be used as pricing
        analysis input. Available only for Floating Rate Notes. No override is
        applied by default. Note that only one pricing anlysis input should be defined.
    discount_percent : float, optional
        Discount (expressed in percent) to override and that will be used as pricing
        analysis input. Should be used only for bond quoted in discount. Optional. No
        override is applied by default. Note that only one pricing anlysis input should
        be defined.
    dividend_yield_percent : float, optional
        Underlying Stock dividend yield percent. Applicable for Convertible Bonds.
    edsf_benchmark_curve_yield_percent : float, optional
        Yield of Euro-Dollar future benchmark curve (Edsf) to override and that will be
        used to compute Euro-Dollar (Edsf) spread. No override is applied by
        default and yield is computed or retrieved from market data.
    edsf_spread_bp : float, optional
        Spread of Euro-Dollar future benchmark curve (Edsf) to override and that will be
        used as pricing analysis input to compute the bond price. This spread is
        computed for USD Bond whose maturity is under 2 Years. No override is
        applied by default. Note that only one pricing anlysis input should be defined.
    efp_benchmark_price : float, optional
        Price of EFP benchmark to override and that will be used to compute benchmark at
        redemption spread in case the bond is an australian FRN. No override
        is applied by default and price is computed or retrieved from market data.
    efp_benchmark_ric : str, optional
        RIC of EFP benchmark to override and that will be used as pricing analysis input
        to compute the bond price in case the bond is an australian FRN. Ric can be
        only "YTTc1" or "YTCc1".
        Default value is "YTTc1".
    efp_benchmark_yield_percent : float, optional
        Yield of EFP benchmark to override and that will be used to compute benchmark at
        redemption spread in case the bond is an australian FRN. No override
        is applied by default and yield is computed or retrieved from market data.
    efp_spread_bp : float, optional
        Spread of EFP benchmark to override and that will be used as pricing analysis
        input to compute the bond price in case the bond is an australian FRN.
        No override is applied by default. Note that only one pricing analysis input
        should be defined.
    flat_credit_spread_bp : float, optional
        Flat credit spread applied during pricing in basis points. Applicable when
        SpreadType = FlatSpread. Applicable for Convertible Bonds.
    flat_credit_spread_tenor : str, optional
        Flat credit spread tenor on credit curve used during pricing to source credit
        spread value. Applicable for Convertible Bonds.
    fx_stock_correlation : float, optional
        Correlation rate between underlying stock price and FX rate. Applicable for
        cross-currency Convertible Bonds.
    fx_volatility_percent : float, optional
        FX volatility rate percent. Applicable for cross-currency Convertible Bonds.
    fx_volatility_tenor : str, optional
        Tenor on FX volatility to source FX volatility Rate Percent. Applicable for
        cross-currency Convertible Bonds.
    gov_country_benchmark_curve_price : float, optional
        Price of government country benchmark to override and that will be used to
        compute user defined spread. No override is applied by default and price is
        computed or retrieved from market data.
    gov_country_benchmark_curve_yield_percent : float, optional
        Yield of government country benchmark to override and that will be used to
        compute government country spread. No override is applied by default
        and yield is computed or retrieved from market data.
    gov_country_spread_bp : float, optional
        Spread of government country benchmark to override and that will be used as
        pricing analysis input to compute the bond price. Optional. No override is
        applied by default. Note that only one pricing analysis input should be defined.
    government_benchmark_curve_price : float, optional
        Price of government benchmark to override and that will be used to compute user
        defined spread. No override is applied by default and price is
        computed or retrieved from market data.
    government_benchmark_curve_yield_percent : float, optional
        Yield of government benchmark to override and that will be used to compute
        government spread. No override is applied by default and yield is
        computed or retrieved from market data.
    government_spread_bp : float, optional
        Spread of government benchmark to override and that will be used as pricing
        analysis input to compute the bond price. No override is applied by
        default. Note that only one pricing analysis input should be defined.
    issuer_benchmark_curve_yield_percent : float, optional
        Yield of issuer benchmark to override and that will be used to compute issuer
        spread. No override is applied by default and yield is computed or retrieved
        from market data.
    issuer_spread_bp : float, optional
        Spread of issuer benchmark to override and that will be used as pricing analysis
        input to compute the bond price. This spread is computed is for coprorate bonds.
        Optional. No override is applied by default. Note that only one pricing anlysis
        input should be defined.
    market_data_date : str or date or datetime or timedelta, optional
        The market data date for pricing.
        By default, the market_data_date date is the valuation_date or Today
    market_value_in_deal_ccy : float, optional
        Market value in deal currency. This field can be used to compute notionalAmount
        to apply to get this market value. Optional. By default the value is computed
        from notional amount. NotionalAmount field, market_value_in_deal_ccy field and
        market_value_in_report_ccy field cannot be set at defined at the same time.
    market_value_in_report_ccy : float, optional
        Market value in report currency. This field can be used to compute
        notionalAmount to apply to get this market value. By default the value
        is computed from notional amount. NotionalAmount field, market_value_in_deal_ccy
        field and market_value_in_report_ccy field cannot be set at defined at the same
        time.
    net_price : float, optional
        Net price to override and that will be used as pricing analysis input.
        No override is applied by default. Note that only one pricing anlysis input
        should be defined.
    neutral_yield_percent : float, optional
        Neutral Yield (expressed in percent) to override and that will be used as
        pricing analysis input. This is available only for floating rate notes.
        No override is applied by default. Note that only one pricing analysis
        input should be defined.
    ois_zc_benchmark_curve_yield_percent : float, optional
        Yield of OIS benchmark to override and that will be used to compute OIS spread.
        No override is applied by default and yield is computed or retrieved from market
        data.
    ois_zc_spread_bp : float, optional
        Yield of OIS benchmark to override and that will be used as pricing analysis
        input to compute the bond price. No override is applied by default.
        Note that only one pricing analysis input should be defined.
    option_adjusted_spread_bp : float, optional
        Option Adjusted Spread to override and that will be used as pricing analysis
        input to compute the bond price. No override is applied by default.
        Note that only one pricing analysis input should be defined.
    price : float, optional
        Price to override and that will be used as pricing analysis input. This price
        can be the clean price or dirty price depending on price type defined in bond
        structure. The currency of the price is the cash flow currency (that can be
        different to deal currency especially if "ComputeCashFlowWithReportCcy" flag has
        been set to true). Optional. No override is applied by default. Note that only
        one pricing analysis input should be defined.
    quoted_price : float, optional
        Quoted price to override and that will be used as pricing analysis input. Note
        that a quoted price can be a price, a yield, a discount margin, a spread,...
        depending on quotation type. The currency of the quoted price in case the bonnd
        is price-quoted or cash-quoted is the deal currency (that can be different to
        cash flow currency especially if "ComputeCashFlowWithReportCcy" flag has been
        set to true). No override is applied by default. Note that only one pricing
        analysis input should be defined.
    rating_benchmark_curve_yield_percent : float, optional
        Yield of rating benchmark to override and that will be used to compute rating
        spread. No override is applied by default and yield is computed or retrieved
        from market data.
    rating_spread_bp : float, optional
        Spread of rating benchmark to override and that will be used as pricing analysis
        input to compute the bond price. No override is applied by default.
        Note that only one pricing anlysis input should be defined.
    redemption_date : str or date or datetime or timedelta, optional
        Redemption date that defines the end date for yield and price computation. Used
        only if redemption date type is set to "RedemptionAtCustomDate"
    sector_rating_benchmark_curve_yield_percent : float, optional
        Yield of sector rating benchmark to override and that will be used to compute
        sector rating spread. No override is applied by default and yield is computed
        or retrieved from market data.
    sector_rating_spread_bp : float, optional
        Spread of sector rating benchmark to override and that will be used as pricing
        analysis input to compute the bond price. No override is applied by default.
        Note that only one pricing anlysis input should be defined.
    settlement_convention : str, optional
        Settlement convention for the bond. By default the rule is that valuation_date =
        trade_date + settlement_convention. By default use the settlement tenor defined
        in the bond structure. Only two parameters among "settlement_convention",
        "market_data_date" and "valuation_date" can be overriden at the same time.
    simple_margin_bp : float, optional
        Simple Margin basis points  to override and that will be used as pricing
        analysis input. Available only for Floating Rate Notes. No override is
        applied by default. Note that only one pricing anlysis input should be defined.
    stock_borrow_rate_percent : float, optional
        Underlying stock borrow rate percent. Applicable for Convertible Bonds.
    stock_flat_volatility_percent : float, optional
        Underlying stock volatility percent used for convertible pricing. Applicable
        when volatility_type = Flat Applicable for Convertible Bonds.
    stock_flat_volatility_tenor : str, optional
        Underlying Stock volatility tenor used during pricing to source volatility
        percent value. Applicable when volatility_type = Flat Applicable for Convertible
        Bonds.
    stock_price_on_default : float, optional
        Assumed stock price agreed in event of default. Applicable for Convertible
        Bonds.
    strip_yield_percent : float, optional
        Strip Yield (expressed in percent) to override and that will be used as pricing
        analysis input. No override is applied by default. Note that only one pricing
        anlysis input should be defined.
    swap_benchmark_curve_yield_percent : float, optional
        Yield of swap benchmark to override and that will be used to compute swap
        spread. No override is applied by default and yield is computed or
        retrieved from market data.
    swap_spread_bp : float, optional
        Spread of swap benchmark to override and that will be used as pricing analysis
        input to compute the bond price. No override is applied by default.
        Note that only one pricing analysis input should be defined.
    tax_on_capital_gain_percent : float, optional
        Tax Rate on capital gain expressed in percent.
        By default no tax is applied that means value is equal to 0.
    tax_on_coupon_percent : float, optional
        Tax Rate on Coupon  expressed in percent.
        By default no tax is applied that means value is equal to 0.
    tax_on_price_percent : float, optional
        Tax Rate on price expressed in percent.
        By default no tax is applied that means value is equal to 0.
    tax_on_yield_percent : float, optional
        Tax Rate on Yield expressed in percent. Also named Tax on Yield Optional.
        By default no tax is applied that means value is equal to 0.
    use_settlement_date_from_quote : bool, optional
        Specify whether to use the settlment date of the quote or the one computed from
        the MarketData Date.
    user_defined_benchmark_price : float, optional
        price of user defined instrument to override and that will be used to compute
        user defined spread. No override is applied by default and price is computed
        or retrieved from market data.
    user_defined_benchmark_yield_percent : float, optional
        Yield of user defined instrument to override and that will be used to compute
        user defined spread. No override is applied by default and yield is computed
        or retrieved from market data.
    user_defined_spread_bp : float, optional
        Spread of user defined instrument to override and that will be used as pricing
        analysis input to compute the bond price. No override is applied by default.
        Note that only one pricing analysis input should be defined.
    valuation_date : str or date or datetime or timedelta, optional
        The valuation date for pricing. If not set the valuation date is equal
        to market_data_date or Today. For assets that contains a settlement_convention,
        the default valuation date is equal to the settlementdate of the Asset that
        is usually the trade_date+settlement_convention.
    yield_percent : float, optional
        Yield (expressed in percent) to override and that will be used as pricing
        analysis input. No override is applied by default. Note that only one pricing
        analysis input should be defined.
    z_spread_bp : float, optional
        ZSpread to override and that will be used as pricing analysis input to compute
        the bond price. No override is applied by default. Note that only one pricing
        analysis input should be defined.

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> definition = rdf.bond.Definition(
    ...    instrument_code="US5YT=RR",
    ...    payment_business_day_convention=rdf.bond.BusinessDayConvention.PREVIOUS_BUSINESS_DAY,
    ...    pricing_parameters=rdf.bond.PricingParameters(
    ...        benchmark_yield_selection_mode=rdf.bond.BenchmarkYieldSelectionMode.INTERPOLATE
    ...    ),
    ...    fields=["InstrumentDescription", "MarketDataDate", "Price", "YieldPercent", "ZSpreadBp"]
    ...)
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        trade_date: OptDateTime = None,
        benchmark_yield_selection_mode: Union[BenchmarkYieldSelectionMode, str] = None,
        credit_spread_type: Union[CreditSpreadType, str] = None,
        dividend_type: Union[DividendType, str] = None,
        fx_price_side: Union[PriceSide, str] = None,
        inflation_mode: Union[InflationMode, str] = None,
        price_side: Union[PriceSide, str] = None,
        projected_index_calculation_method: Union[ProjectedIndexCalculationMethod, str] = None,
        quote_fallback_logic: Union[QuoteFallbackLogic, str] = None,
        redemption_date_type: Union[RedemptionDateType, str] = None,
        rounding_parameters: Union[BondRoundingParameters, dict] = None,
        volatility_term_structure_type: Union[VolatilityTermStructureType, str] = None,
        volatility_type: Union[VolatilityType, str] = None,
        yield_type: Union[YieldType, str] = None,
        adjusted_clean_price: Optional[float] = None,
        adjusted_dirty_price: Optional[float] = None,
        adjusted_yield_percent: Optional[float] = None,
        apply_tax_to_full_pricing: Optional[bool] = None,
        asset_swap_spread_bp: Optional[float] = None,
        benchmark_at_issue_price: Optional[float] = None,
        benchmark_at_issue_ric: Optional[str] = None,
        benchmark_at_issue_spread_bp: Optional[float] = None,
        benchmark_at_issue_yield_percent: Optional[float] = None,
        benchmark_at_redemption_price: Optional[float] = None,
        benchmark_at_redemption_spread_bp: Optional[float] = None,
        benchmark_at_redemption_yield_percent: Optional[float] = None,
        bond_recovery_rate_percent: Optional[float] = None,
        cash_amount: Optional[float] = None,
        cds_recovery_rate_percent: Optional[float] = None,
        clean_price: Optional[float] = None,
        compute_cash_flow_from_issue_date: Optional[bool] = None,
        compute_cash_flow_with_report_ccy: Optional[bool] = None,
        concession_fee: Optional[float] = None,
        current_yield_percent: Optional[float] = None,
        dirty_price: Optional[float] = None,
        discount_margin_bp: Optional[float] = None,
        discount_percent: Optional[float] = None,
        dividend_yield_percent: Optional[float] = None,
        edsf_benchmark_curve_yield_percent: Optional[float] = None,
        edsf_spread_bp: Optional[float] = None,
        efp_benchmark_price: Optional[float] = None,
        efp_benchmark_ric: Optional[str] = None,
        efp_benchmark_yield_percent: Optional[float] = None,
        efp_spread_bp: Optional[float] = None,
        flat_credit_spread_bp: Optional[float] = None,
        flat_credit_spread_tenor: Optional[str] = None,
        fx_stock_correlation: Optional[float] = None,
        fx_volatility_percent: Optional[float] = None,
        fx_volatility_tenor: Optional[str] = None,
        gov_country_benchmark_curve_price: Optional[float] = None,
        gov_country_benchmark_curve_yield_percent: Optional[float] = None,
        gov_country_spread_bp: Optional[float] = None,
        government_benchmark_curve_price: Optional[float] = None,
        government_benchmark_curve_yield_percent: Optional[float] = None,
        government_spread_bp: Optional[float] = None,
        is_coupon_payment_adjustedfor_leap_year: Optional[bool] = None,
        issuer_benchmark_curve_yield_percent: Optional[float] = None,
        issuer_spread_bp: Optional[float] = None,
        market_data_date: OptDateTime = None,
        market_value_in_deal_ccy: Optional[float] = None,
        market_value_in_report_ccy: Optional[float] = None,
        net_price: Optional[float] = None,
        neutral_yield_percent: Optional[float] = None,
        next_coupon_rate_percent: Optional[float] = None,
        ois_zc_benchmark_curve_yield_percent: Optional[float] = None,
        ois_zc_spread_bp: Optional[float] = None,
        option_adjusted_spread_bp: Optional[float] = None,
        price: Optional[float] = None,
        projected_index_percent: Optional[float] = None,
        quoted_price: Optional[float] = None,
        rating_benchmark_curve_yield_percent: Optional[float] = None,
        rating_spread_bp: Optional[float] = None,
        redemption_date: OptDateTime = None,
        report_ccy: Optional[str] = None,
        sector_rating_benchmark_curve_yield_percent: Optional[float] = None,
        sector_rating_spread_bp: Optional[float] = None,
        settlement_convention: Optional[str] = None,
        simple_margin_bp: Optional[float] = None,
        stock_borrow_rate_percent: Optional[float] = None,
        stock_flat_volatility_percent: Optional[float] = None,
        stock_flat_volatility_tenor: Optional[str] = None,
        stock_price_on_default: Optional[float] = None,
        strip_yield_percent: Optional[float] = None,
        swap_benchmark_curve_yield_percent: Optional[float] = None,
        swap_spread_bp: Optional[float] = None,
        tax_on_capital_gain_percent: Optional[float] = None,
        tax_on_coupon_percent: Optional[float] = None,
        tax_on_price_percent: Optional[float] = None,
        tax_on_yield_percent: Optional[float] = None,
        use_settlement_date_from_quote: Optional[bool] = None,
        user_defined_benchmark_price: Optional[float] = None,
        user_defined_benchmark_yield_percent: Optional[float] = None,
        user_defined_spread_bp: Optional[float] = None,
        valuation_date: OptDateTime = None,
        yield_percent: Optional[float] = None,
        z_spread_bp: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.trade_date = trade_date
        self.benchmark_yield_selection_mode = benchmark_yield_selection_mode
        self.credit_spread_type = credit_spread_type
        self.dividend_type = dividend_type
        self.fx_price_side = fx_price_side
        self.inflation_mode = inflation_mode
        self.price_side = price_side
        self.projected_index_calculation_method = projected_index_calculation_method
        self.quote_fallback_logic = quote_fallback_logic
        self.redemption_date_type = redemption_date_type
        self.rounding_parameters = rounding_parameters
        self.volatility_term_structure_type = volatility_term_structure_type
        self.volatility_type = volatility_type
        self.yield_type = yield_type
        self.adjusted_clean_price = adjusted_clean_price
        self.adjusted_dirty_price = adjusted_dirty_price
        self.adjusted_yield_percent = adjusted_yield_percent
        self.apply_tax_to_full_pricing = apply_tax_to_full_pricing
        self.asset_swap_spread_bp = asset_swap_spread_bp
        self.benchmark_at_issue_price = benchmark_at_issue_price
        self.benchmark_at_issue_ric = benchmark_at_issue_ric
        self.benchmark_at_issue_spread_bp = benchmark_at_issue_spread_bp
        self.benchmark_at_issue_yield_percent = benchmark_at_issue_yield_percent
        self.benchmark_at_redemption_price = benchmark_at_redemption_price
        self.benchmark_at_redemption_spread_bp = benchmark_at_redemption_spread_bp
        self.benchmark_at_redemption_yield_percent = benchmark_at_redemption_yield_percent
        self.bond_recovery_rate_percent = bond_recovery_rate_percent
        self.cash_amount = cash_amount
        self.cds_recovery_rate_percent = cds_recovery_rate_percent
        self.clean_price = clean_price
        self.compute_cash_flow_from_issue_date = compute_cash_flow_from_issue_date
        self.compute_cash_flow_with_report_ccy = compute_cash_flow_with_report_ccy
        self.concession_fee = concession_fee
        self.current_yield_percent = current_yield_percent
        self.dirty_price = dirty_price
        self.discount_margin_bp = discount_margin_bp
        self.discount_percent = discount_percent
        self.dividend_yield_percent = dividend_yield_percent
        self.edsf_benchmark_curve_yield_percent = edsf_benchmark_curve_yield_percent
        self.edsf_spread_bp = edsf_spread_bp
        self.efp_benchmark_price = efp_benchmark_price
        self.efp_benchmark_ric = efp_benchmark_ric
        self.efp_benchmark_yield_percent = efp_benchmark_yield_percent
        self.efp_spread_bp = efp_spread_bp
        self.flat_credit_spread_bp = flat_credit_spread_bp
        self.flat_credit_spread_tenor = flat_credit_spread_tenor
        self.fx_stock_correlation = fx_stock_correlation
        self.fx_volatility_percent = fx_volatility_percent
        self.fx_volatility_tenor = fx_volatility_tenor
        self.gov_country_benchmark_curve_price = gov_country_benchmark_curve_price
        self.gov_country_benchmark_curve_yield_percent = gov_country_benchmark_curve_yield_percent
        self.gov_country_spread_bp = gov_country_spread_bp
        self.government_benchmark_curve_price = government_benchmark_curve_price
        self.government_benchmark_curve_yield_percent = government_benchmark_curve_yield_percent
        self.government_spread_bp = government_spread_bp
        self.is_coupon_payment_adjustedfor_leap_year = is_coupon_payment_adjustedfor_leap_year
        self.issuer_benchmark_curve_yield_percent = issuer_benchmark_curve_yield_percent
        self.issuer_spread_bp = issuer_spread_bp
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.market_value_in_report_ccy = market_value_in_report_ccy
        self.net_price = net_price
        self.neutral_yield_percent = neutral_yield_percent
        self.next_coupon_rate_percent = next_coupon_rate_percent
        self.ois_zc_benchmark_curve_yield_percent = ois_zc_benchmark_curve_yield_percent
        self.ois_zc_spread_bp = ois_zc_spread_bp
        self.option_adjusted_spread_bp = option_adjusted_spread_bp
        self.price = price
        self.projected_index_percent = projected_index_percent
        self.quoted_price = quoted_price
        self.rating_benchmark_curve_yield_percent = rating_benchmark_curve_yield_percent
        self.rating_spread_bp = rating_spread_bp
        self.redemption_date = redemption_date
        self.report_ccy = report_ccy
        self.sector_rating_benchmark_curve_yield_percent = sector_rating_benchmark_curve_yield_percent
        self.sector_rating_spread_bp = sector_rating_spread_bp
        self.settlement_convention = settlement_convention
        self.simple_margin_bp = simple_margin_bp
        self.stock_borrow_rate_percent = stock_borrow_rate_percent
        self.stock_flat_volatility_percent = stock_flat_volatility_percent
        self.stock_flat_volatility_tenor = stock_flat_volatility_tenor
        self.stock_price_on_default = stock_price_on_default
        self.strip_yield_percent = strip_yield_percent
        self.swap_benchmark_curve_yield_percent = swap_benchmark_curve_yield_percent
        self.swap_spread_bp = swap_spread_bp
        self.tax_on_capital_gain_percent = tax_on_capital_gain_percent
        self.tax_on_coupon_percent = tax_on_coupon_percent
        self.tax_on_price_percent = tax_on_price_percent
        self.tax_on_yield_percent = tax_on_yield_percent
        self.use_settlement_date_from_quote = use_settlement_date_from_quote
        self.user_defined_benchmark_price = user_defined_benchmark_price
        self.user_defined_benchmark_yield_percent = user_defined_benchmark_yield_percent
        self.user_defined_spread_bp = user_defined_spread_bp
        self.valuation_date = valuation_date
        self.yield_percent = yield_percent
        self.z_spread_bp = z_spread_bp

    def _get_items(self):
        return [
            enum_param_item.to_kv("benchmarkYieldSelectionMode", self.benchmark_yield_selection_mode),
            enum_param_item.to_kv("creditSpreadType", self.credit_spread_type),
            enum_param_item.to_kv("dividendType", self.dividend_type),
            enum_param_item.to_kv("fxPriceSide", self.fx_price_side),
            enum_param_item.to_kv("inflationMode", self.inflation_mode),
            enum_param_item.to_kv("priceSide", self.price_side),
            enum_param_item.to_kv("projectedIndexCalculationMethod", self.projected_index_calculation_method),
            enum_param_item.to_kv("quoteFallbackLogic", self.quote_fallback_logic),
            enum_param_item.to_kv("redemptionDateType", self.redemption_date_type),
            serializable_param_item.to_kv("roundingParameters", self.rounding_parameters),
            enum_param_item.to_kv("volatilityTermStructureType", self.volatility_term_structure_type),
            enum_param_item.to_kv("volatilityType", self.volatility_type),
            enum_param_item.to_kv("yieldType", self.yield_type),
            param_item.to_kv("adjustedCleanPrice", self.adjusted_clean_price),
            param_item.to_kv("adjustedDirtyPrice", self.adjusted_dirty_price),
            param_item.to_kv("adjustedYieldPercent", self.adjusted_yield_percent),
            param_item.to_kv("applyTaxToFullPricing", self.apply_tax_to_full_pricing),
            param_item.to_kv("assetSwapSpreadBp", self.asset_swap_spread_bp),
            param_item.to_kv("benchmarkAtIssuePrice", self.benchmark_at_issue_price),
            param_item.to_kv("benchmarkAtIssueRic", self.benchmark_at_issue_ric),
            param_item.to_kv("benchmarkAtIssueSpreadBp", self.benchmark_at_issue_spread_bp),
            param_item.to_kv("benchmarkAtIssueYieldPercent", self.benchmark_at_issue_yield_percent),
            param_item.to_kv("benchmarkAtRedemptionPrice", self.benchmark_at_redemption_price),
            param_item.to_kv("benchmarkAtRedemptionSpreadBp", self.benchmark_at_redemption_spread_bp),
            param_item.to_kv("benchmarkAtRedemptionYieldPercent", self.benchmark_at_redemption_yield_percent),
            param_item.to_kv("bondRecoveryRatePercent", self.bond_recovery_rate_percent),
            param_item.to_kv("cashAmount", self.cash_amount),
            param_item.to_kv("cdsRecoveryRatePercent", self.cds_recovery_rate_percent),
            param_item.to_kv("cleanPrice", self.clean_price),
            param_item.to_kv("computeCashFlowFromIssueDate", self.compute_cash_flow_from_issue_date),
            param_item.to_kv("computeCashFlowWithReportCcy", self.compute_cash_flow_with_report_ccy),
            param_item.to_kv("concessionFee", self.concession_fee),
            param_item.to_kv("currentYieldPercent", self.current_yield_percent),
            param_item.to_kv("dirtyPrice", self.dirty_price),
            param_item.to_kv("discountMarginBp", self.discount_margin_bp),
            param_item.to_kv("discountPercent", self.discount_percent),
            param_item.to_kv("dividendYieldPercent", self.dividend_yield_percent),
            param_item.to_kv("edsfBenchmarkCurveYieldPercent", self.edsf_benchmark_curve_yield_percent),
            param_item.to_kv("edsfSpreadBp", self.edsf_spread_bp),
            param_item.to_kv("efpBenchmarkPrice", self.efp_benchmark_price),
            param_item.to_kv("efpBenchmarkRic", self.efp_benchmark_ric),
            param_item.to_kv("efpBenchmarkYieldPercent", self.efp_benchmark_yield_percent),
            param_item.to_kv("efpSpreadBp", self.efp_spread_bp),
            param_item.to_kv("flatCreditSpreadBp", self.flat_credit_spread_bp),
            param_item.to_kv("flatCreditSpreadTenor", self.flat_credit_spread_tenor),
            param_item.to_kv("fxStockCorrelation", self.fx_stock_correlation),
            param_item.to_kv("fxVolatilityPercent", self.fx_volatility_percent),
            param_item.to_kv("fxVolatilityTenor", self.fx_volatility_tenor),
            param_item.to_kv("govCountryBenchmarkCurvePrice", self.gov_country_benchmark_curve_price),
            param_item.to_kv("govCountryBenchmarkCurveYieldPercent", self.gov_country_benchmark_curve_yield_percent),
            param_item.to_kv("govCountrySpreadBp", self.gov_country_spread_bp),
            param_item.to_kv("governmentBenchmarkCurvePrice", self.government_benchmark_curve_price),
            param_item.to_kv("governmentBenchmarkCurveYieldPercent", self.government_benchmark_curve_yield_percent),
            param_item.to_kv("governmentSpreadBp", self.government_spread_bp),
            param_item.to_kv("isCouponPaymentAdjustedforLeapYear", self.is_coupon_payment_adjustedfor_leap_year),
            param_item.to_kv("issuerBenchmarkCurveYieldPercent", self.issuer_benchmark_curve_yield_percent),
            param_item.to_kv("issuerSpreadBp", self.issuer_spread_bp),
            param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("marketValueInDealCcy", self.market_value_in_deal_ccy),
            param_item.to_kv("marketValueInReportCcy", self.market_value_in_report_ccy),
            param_item.to_kv("netPrice", self.net_price),
            param_item.to_kv("neutralYieldPercent", self.neutral_yield_percent),
            param_item.to_kv("nextCouponRatePercent", self.next_coupon_rate_percent),
            param_item.to_kv("oisZcBenchmarkCurveYieldPercent", self.ois_zc_benchmark_curve_yield_percent),
            param_item.to_kv("oisZcSpreadBp", self.ois_zc_spread_bp),
            param_item.to_kv("optionAdjustedSpreadBp", self.option_adjusted_spread_bp),
            param_item.to_kv("price", self.price),
            param_item.to_kv("projectedIndexPercent", self.projected_index_percent),
            param_item.to_kv("quotedPrice", self.quoted_price),
            param_item.to_kv("ratingBenchmarkCurveYieldPercent", self.rating_benchmark_curve_yield_percent),
            param_item.to_kv("ratingSpreadBp", self.rating_spread_bp),
            param_item.to_kv("redemptionDate", self.redemption_date),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv(
                "sectorRatingBenchmarkCurveYieldPercent", self.sector_rating_benchmark_curve_yield_percent
            ),
            param_item.to_kv("sectorRatingSpreadBp", self.sector_rating_spread_bp),
            param_item.to_kv("settlementConvention", self.settlement_convention),
            param_item.to_kv("simpleMarginBp", self.simple_margin_bp),
            param_item.to_kv("stockBorrowRatePercent", self.stock_borrow_rate_percent),
            param_item.to_kv("stockFlatVolatilityPercent", self.stock_flat_volatility_percent),
            param_item.to_kv("stockFlatVolatilityTenor", self.stock_flat_volatility_tenor),
            param_item.to_kv("stockPriceOnDefault", self.stock_price_on_default),
            param_item.to_kv("stripYieldPercent", self.strip_yield_percent),
            param_item.to_kv("swapBenchmarkCurveYieldPercent", self.swap_benchmark_curve_yield_percent),
            param_item.to_kv("swapSpreadBp", self.swap_spread_bp),
            param_item.to_kv("taxOnCapitalGainPercent", self.tax_on_capital_gain_percent),
            param_item.to_kv("taxOnCouponPercent", self.tax_on_coupon_percent),
            param_item.to_kv("taxOnPricePercent", self.tax_on_price_percent),
            param_item.to_kv("taxOnYieldPercent", self.tax_on_yield_percent),
            datetime_param_item.to_kv("tradeDate", self.trade_date),
            param_item.to_kv("useSettlementDateFromQuote", self.use_settlement_date_from_quote),
            param_item.to_kv("userDefinedBenchmarkPrice", self.user_defined_benchmark_price),
            param_item.to_kv("userDefinedBenchmarkYieldPercent", self.user_defined_benchmark_yield_percent),
            param_item.to_kv("userDefinedSpreadBp", self.user_defined_spread_bp),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
            param_item.to_kv("yieldPercent", self.yield_percent),
            param_item.to_kv("zSpreadBp", self.z_spread_bp),
        ]
