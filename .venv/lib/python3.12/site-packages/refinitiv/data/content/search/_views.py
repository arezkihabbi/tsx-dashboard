from enum import unique

from ..._base_enum import StrEnum


@unique
class Views(StrEnum):
    """Possible views values to request data from 'search' endpoint"""

    BOND_FUT_OPT_QUOTES = "BondFutOptQuotes"
    CDS_INSTRUMENTS = "CdsInstruments"
    CDS_QUOTES = "CdsQuotes"
    CMO_INSTRUMENTS = "CmoInstruments"
    CMO_QUOTES = "CmoQuotes"
    COMMODITY_QUOTES = "CommodityQuotes"
    DEALS_MERGERS_AND_ACQUISITIONS = "DealsMergersAndAcquisitions"
    DERIVATIVE_INSTRUMENTS = "DerivativeInstruments"
    DERIVATIVE_QUOTES = "DerivativeQuotes"
    EQUITY_DERIVATIVE_INSTRUMENTS = "EquityDerivativeInstruments"
    EQUITY_DERIVATIVE_QUOTES = "EquityDerivativeQuotes"
    EQUITY_INSTRUMENTS = "EquityInstruments"
    EQUITY_QUOTES = "EquityQuotes"
    FIXED_INCOME_INSTRUMENTS = "FixedIncomeInstruments"
    FIXED_INCOME_QUOTES = "FixedIncomeQuotes"
    FUND_QUOTES = "FundQuotes"
    GOV_CORP_INSTRUMENTS = "GovCorpInstruments"
    GOV_CORP_QUOTES = "GovCorpQuotes"
    INDEX_INSTRUMENTS = "IndexInstruments"
    INDEX_QUOTES = "IndexQuotes"
    INDICATOR_QUOTES = "IndicatorQuotes"
    INSTRUMENTS = "Instruments"
    IRD_QUOTES = "IRDQuotes"
    LOAN_INSTRUMENTS = "LoanInstruments"
    LOAN_QUOTES = "LoanQuotes"
    MONEY_QUOTES = "MoneyQuotes"
    MORTGAGE_INSTRUMENTS = "MortgageInstruments"
    MORT_QUOTES = "MortQuotes"
    MUNICIPAL_INSTRUMENTS = "MunicipalInstruments"
    MUNICIPAL_QUOTES = "MunicipalQuotes"
    ORGANISATIONS = "Organisations"
    PEOPLE = "People"
    PHYSICAL_ASSETS = "PhysicalAssets"
    QUOTES = "Quotes"
    QUOTES_AND_STIRS = "QuotesAndSTIRs"
    SEARCH_ALL = "SearchAll"
    STIRS = "STIRs"
    VESSEL_PHYSICAL_ASSETS = "VesselPhysicalAssets"
    YIELD_CURVE_CONT_QUOTES = "YieldCurveContQuotes"
    RCS = "RCS"
    INVESTORS = "Investors"
    CATALOG_ITEMS = "CatalogItems"
    ENTITIES = "Entities"

    @classmethod
    def possible_values(cls):
        return [s for s in cls.__members__.values()]
