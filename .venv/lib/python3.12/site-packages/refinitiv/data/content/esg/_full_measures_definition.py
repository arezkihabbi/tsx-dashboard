from typing import TYPE_CHECKING

from ._base_definition import BaseDefinition
from ..._content_type import ContentType
from ..._tools import validate_types, validate_bool_value, try_copy_to_list

if TYPE_CHECKING:
    from ..._types import StrStrings, OptInt


class Definition(BaseDefinition):
    """
    Defines the ESG full measures data to retrieve.

    Parameters
    ----------
    universe : str, list of str
        Single instrument or list of instruments.
    start : int, optional
        Initial value of financial years range to return.
    end : int, optional
        End range of financial years to return.
    use_field_names_in_headers: bool, optional
        Boolean that indicates whether or not to display field names in the headers.

    Examples
    --------
    >>> from refinitiv.data.content import esg
    >>> definition = esg.full_measures.Definition("BNPP.PA")
    """

    def __init__(
        self,
        universe: "StrStrings",
        start: "OptInt" = None,
        end: "OptInt" = None,
        use_field_names_in_headers: bool = False,
    ):
        validate_types(start, [int, type(None)], "start")
        validate_types(end, [int, type(None)], "end")
        validate_bool_value(use_field_names_in_headers)
        universe = try_copy_to_list(universe)

        super().__init__(
            ContentType.ESG_FULL_MEASURES,
            universe=universe,
            start=start,
            end=end,
            use_field_names_in_headers=use_field_names_in_headers,
        )

    def __repr__(self):
        s = super().__repr__()
        return s.replace("esg", "esg.full_measures")
