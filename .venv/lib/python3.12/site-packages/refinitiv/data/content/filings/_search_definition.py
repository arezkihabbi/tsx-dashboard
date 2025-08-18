from typing import TYPE_CHECKING, Union, List

from ._feed_name import Feed
from ._search_data_provider import FilingsSearchData
from ..._content_type import ContentType
from ..._errors import RDError
from ..._tools import filling_search_datetime_adapter
from ...delivery._data._data_provider import DataProviderLayer, Response
from ...delivery._data._endpoint_data import RequestMethod

if TYPE_CHECKING:
    from ..._types import DateTime


class Definition(DataProviderLayer[Response[FilingsSearchData]]):
    """
    This class provide searching and filtering for Filings documents
    Query string can be built by using data-store endpoint in API playgound

    Parameters
    ----------
    query: str
        Full query string to request the search. This will override other parameters.
        Can't be used with parameters form_type, feed, org_id, start_date, end_date, text, sections.
    variables: dict
        Variables can be used for this query.
        Can't be used with parameters form_type, feed, org_id, start_date, end_date, text, sections.
    form_type: str
        Defines the Form Type used to query across the Filings database
    feed: str
        Defines the Feed used to query across the Filings database
    org_id: str
        Defines the Organization ID used to query across the Filings database
    start_date: str
        Defines a from date to use in our date range to search for filings
    end_date: str
        Defines a to date to use in our date range to search for filings
    text: str
        Defines the text string to search across the Filings database
    sections: list[str]
        Defines the sections of data within the filings to retrieve
    limit: int
        Defines the limit of document hits per response. Default: 10
    sort_order: str
        Defines the response sort order. Possible values: ASC, DESC. Default: DESC

    Examples
    --------
    >>> from refinitiv.data.content import filings
    >>> query = '{  FinancialFiling(filter: {AND: [{FilingDocument: {DocumentSummary: {FeedName: {EQ: "Edgar"}}}}, {FilingDocument: {DocumentSummary: {FormType: {EQ: "10-Q"}}}}, {FilingDocument: {DocumentSummary: {FilingDate: {BETWN: {FROM: "2020-01-01T00:00:00Z", TO: "2020-12-31T00:00:00Z"}}}}}]}, sort: {FilingDocument: {DocumentSummary: {FilingDate: DESC}}}, limit: 10) {    _metadata {      totalCount    }    FilingDocument {      Identifiers {        Dcn      }      DocId      FinancialFilingId      DocumentSummary {        DocumentTitle        FeedName        FormType        HighLevelCategory        MidLevelCategory        FilingDate        SecAccessionNumber        SizeInBytes          }  FilesMetaData {        FileName        MimeType      }    }  }}'
    >>> definition = filings.search.Definition(query=query)
    >>> response = definition.get_data()
    >>> # response.data.df for prioritize information
    >>> # response.data.raw to see all data responded from the service
    >>> response.data.files[0].download(path="C:\\Downloads\\download_test")
    >>> # To download all files from search
    >>> response.data.files.download()

    >>> # async download files
    >>> await response.data.files[0].download_async()
    >>> await response.data.files.download_async()
    """

    def __init__(
        self,
        query: str = None,
        variables: dict = None,
        form_type: str = None,
        feed: Union[str, Feed] = None,
        org_id: str = None,
        start_date: "DateTime" = None,
        end_date: "DateTime" = None,
        text: str = None,
        limit=None,
        sort_order=None,
        sections: List[str] = None,
    ):
        self.query = query
        self.variables = variables
        start_date = filling_search_datetime_adapter.get_localize(start_date)
        end_date = filling_search_datetime_adapter.get_localize(end_date)
        if any((query, variables)) and any(
            (form_type, feed, org_id, start_date, end_date, text, sections, sort_order, limit)
        ):
            raise RDError(
                -1,
                "Mix parameters. Can't use query and variables parameters together with "
                "[form_type, feed, org_id, start_date, end_date, text, limit, sort_order, sections].",
            )

        super().__init__(
            ContentType.FILINGS_SEARCH,
            method=RequestMethod.POST,
            query=self.query,
            variables=self.variables,
            form_type=form_type,
            feed=feed,
            org_id=org_id,
            start_date=start_date,
            end_date=end_date,
            text=text,
            sections=sections,
            limit=limit,
            sort_order=sort_order,
        )
