from typing import Any, Callable, Dict, Union

import pandas as pd

from ._df_build_type import DFBuildType
from ._df_builder import (
    build_dates_calendars_date_schedule_df,
    build_dates_calendars_df,
    build_dates_calendars_holidays_df,
    build_empty_df,
    default_build_df,
    dfbuilder_fundamental_and_reference_rdp,
    dfbuilder_rdp,
    dfbuilder_udf,
)
from ._historical_df_builder import custom_insts_builder, historical_builder, historical_events_builder
from .custom_instruments._custom_instruments_data_provider import (
    custom_instruments_build_df,
    custom_instruments_search_build_df,
)
from .filings._search_df_builder import build_filings_search_df
from .ipa.curves._curves_builder_df import (
    bond_curve_build_df,
    cross_currency_curves_curve_build_df,
    cross_currency_curves_definitions_search_build_df,
    forward_curve_build_df,
    zc_curve_definitions_build_df,
    zc_curves_build_df,
)
from .ipa.financial_contracts._data_provider import financial_contracts_build_df
from .news._tools import news_build_df
from .news.online_reports._df_builder import news_online_reports_build_df
from .news.online_reports.hierarchy._df_builder import news_online_reports_hierarchy_build_df
from .news.top_news._df_builder import news_top_build_df
from .news.top_news.hierarchy._df_builder import news_top_hierarchy_build_df
from .pricing._pricing_content_provider import pricing_build_df
from .pricing.chain._chains_data_provider import chains_build_df
from .search._data_provider import discovery_lookup_build_df, discovery_metadata_build_df, discovery_search_build_df
from .._content_type import ContentType
from ..delivery._data._data_type import DataType

content_type_by_build_type: Dict[Union[ContentType, DataType], Callable[[Any, Dict[str, Any]], pd.DataFrame]] = {
    ContentType.CHAINS: chains_build_df,
    ContentType.CONTRACTS: financial_contracts_build_df,
    ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS: custom_instruments_build_df,
    ContentType.CUSTOM_INSTRUMENTS_SEARCH: custom_instruments_search_build_df,
    ContentType.DATA_GRID_RDP: {
        DFBuildType.INDEX: dfbuilder_fundamental_and_reference_rdp.build_index,
        DFBuildType.DATE_AS_INDEX: dfbuilder_rdp.build_date_as_index,
    },
    ContentType.DATA_GRID_UDF: {
        DFBuildType.EMPTY: build_empty_df,
        DFBuildType.INDEX: dfbuilder_udf.build_index,
        DFBuildType.DATE_AS_INDEX: dfbuilder_udf.build_date_as_index,
    },
    ContentType.DEFAULT: default_build_df,
    ContentType.DISCOVERY_LOOKUP: discovery_lookup_build_df,
    ContentType.DISCOVERY_METADATA: discovery_metadata_build_df,
    ContentType.DISCOVERY_SEARCH: discovery_search_build_df,
    ContentType.ESG_BASIC_OVERVIEW: dfbuilder_rdp.build_index,
    ContentType.ESG_FULL_MEASURES: dfbuilder_rdp.build_index,
    ContentType.ESG_FULL_SCORES: dfbuilder_rdp.build_index,
    ContentType.ESG_STANDARD_MEASURES: dfbuilder_rdp.build_index,
    ContentType.ESG_STANDARD_SCORES: dfbuilder_rdp.build_index,
    ContentType.ESG_UNIVERSE: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_ACTUALS_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_ACTUALS_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_ACTUALS_KPI_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_NON_PERIODIC_MEASURES: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_PERIODIC_MEASURES_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_HISTORICAL_SNAPSHOTS_RECOMMENDATIONS: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_ANNUAL: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_HISTORICAL_SNAPSHOTS_KPI: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_KPI_INTERIM: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_NON_PERIODIC_MEASURES: dfbuilder_rdp.build_index,
    ContentType.ESTIMATES_VIEW_SUMMARY_RECOMMENDATIONS: dfbuilder_rdp.build_index,
    ContentType.FILINGS_RETRIEVAL: dfbuilder_rdp.build_index,
    ContentType.FILINGS_SEARCH: build_filings_search_df,
    ContentType.BOND_CURVE: bond_curve_build_df,
    ContentType.FORWARD_CURVE: forward_curve_build_df,
    ContentType.CROSS_CURRENCY_CURVES_CURVES: cross_currency_curves_curve_build_df,
    ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_CREATE: build_empty_df,
    ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_DELETE: build_empty_df,
    ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_GET: build_empty_df,
    ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_UPDATE: build_empty_df,
    ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_SEARCH: cross_currency_curves_definitions_search_build_df,
    ContentType.CROSS_CURRENCY_CURVES_TRIANGULATE_DEFINITIONS_SEARCH: default_build_df,
    ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES: custom_insts_builder,
    ContentType.CUSTOM_INSTRUMENTS_EVENTS: custom_insts_builder,
    ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES: custom_insts_builder,
    ContentType.HISTORICAL_PRICING_EVENTS: historical_events_builder,
    ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES: historical_builder,
    ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES: historical_builder,
    ContentType.NEWS_HEADLINES: news_build_df,
    ContentType.NEWS_TOP_NEWS_HIERARCHY: news_top_hierarchy_build_df,
    ContentType.NEWS_TOP_NEWS: news_top_build_df,
    ContentType.NEWS_ONLINE_REPORTS: news_online_reports_build_df,
    ContentType.NEWS_ONLINE_REPORTS_HIERARCHY: news_online_reports_hierarchy_build_df,
    ContentType.OWNERSHIP_CONSOLIDATED_BREAKDOWN: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_CONCENTRATION: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_INVESTORS: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_RECENT_ACTIVITY: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_HISTORY_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_SHAREHOLDERS_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_CONSOLIDATED_TOP_N_CONCENTRATION: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_BREAKDOWN: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_CONCENTRATION: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_HOLDINGS: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_INVESTORS: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_RECENT_ACTIVITY: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_HISTORY_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_SHAREHOLDERS_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_FUND_TOP_N_CONCENTRATION: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_INSIDER_SHAREHOLDERS_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_INSIDER_TRANSACTION_REPORT: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_INVESTOR_HOLDINGS: dfbuilder_rdp.build_index,
    ContentType.OWNERSHIP_ORG_INFO: dfbuilder_rdp.build_index,
    ContentType.PRICING: pricing_build_df,
    ContentType.SURFACES: default_build_df,
    ContentType.DATES_AND_CALENDARS_COUNT_PERIODS: default_build_df,
    ContentType.DATES_AND_CALENDARS_DATE_SCHEDULE: build_dates_calendars_date_schedule_df,
    ContentType.DATES_AND_CALENDARS_HOLIDAYS: build_dates_calendars_holidays_df,
    ContentType.DATES_AND_CALENDARS_ADD_PERIODS: build_dates_calendars_df,
    ContentType.DATES_AND_CALENDARS_IS_WORKING_DAY: build_dates_calendars_df,
    ContentType.ZC_CURVE_DEFINITIONS: zc_curve_definitions_build_df,
    ContentType.ZC_CURVES: zc_curves_build_df,
}


def get_dfbuilder(
    content_type: ContentType, dfbuild_type: DFBuildType = DFBuildType.INDEX
) -> Callable[[Any, Dict[str, Any]], pd.DataFrame]:
    builder_by_build_type = content_type_by_build_type.get(content_type)

    if not builder_by_build_type:
        raise ValueError(f"Cannot find mapping for content_type={content_type}")

    if hasattr(builder_by_build_type, "get"):
        builder = builder_by_build_type.get(dfbuild_type)

    else:
        builder = builder_by_build_type

    if not builder:
        raise ValueError(f"Cannot find mapping for dfbuild_type={dfbuild_type}")

    return builder
