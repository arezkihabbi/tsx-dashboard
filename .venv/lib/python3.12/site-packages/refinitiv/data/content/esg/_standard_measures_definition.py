from typing import TYPE_CHECKING

from ._base_definition import BaseDefinition
from ..._content_type import ContentType
from ..._tools import validate_types, validate_bool_value, try_copy_to_list

if TYPE_CHECKING:
    from ..._types import StrStrings, OptInt


class Definition(BaseDefinition):
    """
    This class describe parameters to retrieve ESG standart measures data.

    Parameters
    ----------
    universe : str, list of str
        The Universe parameter allows the user to define the company they
        want content returned for, ESG content is delivered at the Company Level.

    start : int, optional
        Start & End parameter allows the user to request
         the number of Financial Years they would like returned.

    end : int, optional
        Start & End parameter allows the user to request
        the number of Financial Years they would like returned.

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    Examples
    --------
    >>> from refinitiv.data.content import esg
    >>> definition = esg.standard_measures.Definition("BNPP.PA")
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
            ContentType.ESG_STANDARD_MEASURES,
            universe=universe,
            start=start,
            end=end,
            use_field_names_in_headers=use_field_names_in_headers,
        )

    def __repr__(self):
        get_repr = super().__repr__()
        return get_repr.replace("esg", "esg.standard_measures")
