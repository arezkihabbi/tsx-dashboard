from typing import TYPE_CHECKING

from ._base_definition import BaseDefinition
from ..._content_type import ContentType
from ..._tools import validate_types, validate_bool_value, try_copy_to_list

if TYPE_CHECKING:
    from ..._types import StrStrings, OptInt


class Definition(BaseDefinition):
    """
    Defines the ESG standard scores data to retrieve.

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
    >>> definition = esg.standard_scores.Definition("6758.T")
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
            ContentType.ESG_STANDARD_SCORES,
            universe=universe,
            start=start,
            end=end,
            use_field_names_in_headers=use_field_names_in_headers,
        )

    def __repr__(self):
        get_repr = super().__repr__()
        return get_repr.replace("esg", "esg.standard_scores")
