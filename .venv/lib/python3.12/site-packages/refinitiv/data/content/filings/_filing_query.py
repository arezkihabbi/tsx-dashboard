from typing import Union, List

from ._feed_name import Feed
from ..._tools import filling_search_datetime_adapter
from ..._types import OptDateTime

DEFAULT_LIMIT = 10

FORM_TYPE_TEMPLATE = '{FilingDocument: {DocumentSummary: {FormType: {EQ: "%s"}}}}'
FEED_TEMPLATE = '{FilingDocument: {DocumentSummary: {FeedName: {EQ: "%s"}}}}'
ORG_ID_TEMPLATE = '{FilingDocument: {Identifiers: {OrganizationId: {EQ: "%s"}}}}'
KEYWORDS_TEMPLATE = ""
CURSOR_EXPR = ', cursor: "$cursor"'

QUERY_TEMPLATE = (
    "{"
    "        FinancialFiling($filter $keywords"
    "                        sort: {FilingDocument: {DocumentSummary: {FilingDate: $sortOrder}}},"
    "                        limit: $limit $cursorExpr) {"
    "           _metadata {"
    "               totalCount"
    "               cursor"
    "               hasMore"
    "           }"
    "           FilingOrganization {"
    "               Names {"
    "                   Name{"
    "                       OrganizationName("
    '                          filter: {AND: [{LanguageId_v2: {EQ: "505062"}}, {NameTypeCode: {EQ: "LNG"}}]}'
    "                       ) {"
    "                          Name"
    "                       }"
    "                   }"
    "               }"
    "           }"
    "           FilingDocument {"
    "               Identifiers {"
    "                   OrganizationId"
    "                   Dcn"
    "               }"
    "               DocId"
    "               FinancialFilingId"
    "               $sections"
    "               DocumentSummary {"
    "                  DocumentTitle"
    "                  FeedName"
    "                  FormType"
    "                  HighLevelCategory"
    "                  MidLevelCategory"
    "                  FilingDate"
    "                  SecAccessionNumber"
    "                  SizeInBytes"
    "               }"
    "               FilesMetaData {"
    "                  FileName"
    "                  MimeType"
    "               }"
    "           }"
    "       }"
    "    }"
)


def get_dates_expression(start_date: "OptDateTime" = None, end_date: "OptDateTime" = None) -> str:
    dates = ""
    if start_date and end_date:
        dates = f'BETWN: {{FROM: "{filling_search_datetime_adapter.get_str(start_date)}", TO: "{filling_search_datetime_adapter.get_str(end_date)}"}}'
    elif start_date:
        dates = f'GTE: "{filling_search_datetime_adapter.get_str(start_date)}"'
    elif end_date:
        dates = f'LTE: "{filling_search_datetime_adapter.get_str(end_date)}"'

    filling_date = f"{{FilingDocument: {{DocumentSummary: {{FilingDate: {{{dates}}}}}}}}}"
    return filling_date


def _get_filter_expression(
    form_type: Union[Feed, str] = None,
    feed: str = None,
    org_id: str = None,
    start_date: "OptDateTime" = None,
    end_date: "OptDateTime" = None,
) -> str:
    filters = []
    if form_type:
        filters.append(FORM_TYPE_TEMPLATE % form_type)

    if feed:
        filters.append(FEED_TEMPLATE % feed)

    if org_id:
        filters.append(ORG_ID_TEMPLATE % org_id)

    if start_date or end_date:
        filters.append(get_dates_expression(start_date, end_date))

    if not filters:
        return ""

    filter_expression = ", ".join(filters)

    if len(filters) > 1:
        filter_expression = f"{{AND: [{filter_expression}]}}"

    return f"filter: {filter_expression},"


def _get_keywords_expression(text: str) -> str:
    if text:
        return f'keywords: {{searchstring: "FinancialFiling.FilingDocument.DocumentText:{text}"}},'
    return ""


def _get_sections_expression(sections: List[str]) -> str:
    if sections:
        contents = " ".join([f"{section} {{Text}}" for section in sections])
        return f"Sections{{ {contents} }}"
    return ""


def get_query(
    form_type: str = None,
    feed: Union[Feed, str] = None,
    org_id: str = None,
    start_date: "OptDateTime" = None,
    end_date: "OptDateTime" = None,
    text: str = None,
    sections: List[str] = None,
    limit: int = None,
    sort_order: str = None,
    cursor: str = None,
) -> str:
    if limit is None:
        limit = DEFAULT_LIMIT

    if sort_order is None:
        sort_order = "DESC"
    query = QUERY_TEMPLATE.replace("$limit", str(limit)).replace("$sortOrder", sort_order)

    if cursor:
        query = query.replace("$cursorExpr", CURSOR_EXPR).replace("$cursor", cursor)
    else:
        query = query.replace("$cursorExpr", "")

    filter_expression = _get_filter_expression(form_type, feed, org_id, start_date, end_date)
    query = query.replace("$filter", filter_expression)

    keywords_expression = _get_keywords_expression(text)
    query = query.replace("$keywords", keywords_expression)

    sections_expression = _get_sections_expression(sections)
    query = query.replace("$sections", sections_expression)

    return query
