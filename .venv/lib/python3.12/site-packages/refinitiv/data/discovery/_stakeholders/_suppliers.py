from ._relationship_type import RelationshipType
from ._stakeholders import Stakeholders


class Suppliers(Stakeholders):
    """
    Gets suppliers data from fundamental and reference data as well as symbol conversion data.

    Parameters
    ----------
    instrument : str
        Instrument to request.

    Examples
    --------
    >>> suppliers = Suppliers("VOD.L")
    >>> suppliers.get_data()
    >>> print(suppliers.df)
    """

    _relationship_type = RelationshipType.SUPPLIER
