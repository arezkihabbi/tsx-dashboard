from typing import TYPE_CHECKING

from ._db_manager import create_db_manager_by_package_name, DBManager
from ...._tools import try_copy_to_list, fields_arg_parser, universe_arg_parser

if TYPE_CHECKING:
    from ...._types import StrStrings, OptStrStrs


class Response:
    pass


class Definition:
    """
    Defines the ESG full measures data to retrieve.

    Parameters
    ----------
    package_name : str
        Name of the package to download.
    universe : str, list of str
        Single instrument or list of instruments.
    fields : list, optional
        List of fields to return.

    Examples
    --------
    >>> import refinitiv.data.content.esg.bulk as bulk
    >>> definition = bulk.Definition(
    ...     package_name='standard_scores',
    ...     universe=['4295875817', '4295889298'],
    ...     fields=["instrument", "periodenddate"]
    ... )
    >>> response = definition.get_db_data()
    >>> df = response.data.df
    >>> print(df)

    """

    def __init__(
        self,
        package_name: str,
        universe: "StrStrings",
        fields: "OptStrStrs" = None,
    ) -> None:
        fields = try_copy_to_list(fields)
        self._fields = fields and fields_arg_parser.get_list(fields)
        universe = try_copy_to_list(universe)
        self._universe = universe_arg_parser.get_list(universe)
        self._db_manager: DBManager = create_db_manager_by_package_name(package_name)

    def get_db_data(self) -> Response:
        """
        Sends a request to the previously created database to retrieve the defined ESG data.

        Returns
        -------
        Response

        """
        data = self._db_manager.get_data(universe=self._universe, fields=self._fields)
        response = Response()
        response.data = data
        return response
