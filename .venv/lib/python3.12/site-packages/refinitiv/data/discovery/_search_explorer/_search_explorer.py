from typing import Union

from ._df_builder import build_navigators_df, build_search_df, build_metadata_df, merge_metadata_df_and_search_df
from ._property import create_properties
from ._search_explorer_response import SearchPropertyExplorerResponse
from ...content import search
from ...content.search import Views


class SearchPropertyExplorer:
    """
    SearchPropertyExplorer object provides ability to get search data and metadata by
    merging responses from two requests.
    """

    @staticmethod
    def get_properties_for(
        query: str = None,
        filter: str = None,
        view: Union[Views, str] = Views.SEARCH_ALL,
        order_by: str = None,
        navigators: str = None,
    ) -> SearchPropertyExplorerResponse:
        """
        Retrieve search data and metadata. Transform results, create
        properties and navigators objects, merge responses into single object.

        Parameters
        ----------
        query: str, optional
            Keyword argument for view.

        view: Views or str, optional
            Picks a subset of the data universe to search against.
            Default: Views.SEARCH_ALL

        filter: str, optional
            Filter values are boolean predicate expressions that can be defined with help
            of metadata for building more precise requests.

        order_by: str, optional
            Defines the order in which matching documents should be returned.

        navigators: str, optional
            This can name one or more properties, separated by commas, each of which must
            be Navigable. It returns supplemental information about the distribution of the whole matched set.

        Returns
        -------
            SearchPropertyExplorerResponse

        Examples
        --------
        >>> from refinitiv.data.discovery._search_explorer import SearchPropertyExplorer
        >>> explorer = SearchPropertyExplorer()
        >>> santander_bonds = explorer.get_properties_for(
        ...    view=search.Views.GOV_CORP_INSTRUMENTS,
        ...    query="santander bonds",
        ...    filter="IsPerpetualSecurity ne true and IsActive eq true and not(AssetStatus in ('MAT' 'DC'))"
        ... )
        """
        search_response = search.Definition(
            view=view,
            query=query,
            filter=filter,
            top=1,
            select="_debugall",
            order_by=order_by,
            navigators=navigators,
        ).get_data()
        search_raw = search_response.data.raw
        search_total = search_response.total
        navigators = build_navigators_df(search_raw)
        search_df = build_search_df(search_raw, search_total)
        metadata_response = search.metadata.Definition(view=view).get_data()
        metadata_raw = metadata_response.data.raw
        metadata_df = build_metadata_df(metadata_raw["Properties"], search_df)
        request_arguments = {
            "query": query,
            "filter": filter,
            "view": view,
            "order_by": order_by,
            "navigators": navigators,
        }
        df = merge_metadata_df_and_search_df(metadata_df, search_df)
        return SearchPropertyExplorerResponse(
            hits_count=search_total,
            properties=create_properties(df, request_arguments, search_response, metadata_response),
            df=df,
            navigators=navigators,
        )
