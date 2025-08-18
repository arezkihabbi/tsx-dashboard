from ._relationship_type import RelationshipType
from ._stakeholders import Stakeholders


class Customers(Stakeholders):
    """
    Gets customer data from fundamental and reference data as well as symbol conversion data.

    Parameters
    ----------
    instrument : str
        Instrument to request.

    Examples
    --------
    >>> customers = Customers("VOD.L")
    >>> customers.get_data()
    >>> print(customers.df)
    """

    _relationship_type = RelationshipType.CUSTOMER
