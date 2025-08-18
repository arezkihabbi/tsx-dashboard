from ._discovery_universe import DiscoveryUniverse


class Screener(DiscoveryUniverse):
    """
    Class to get data from screen function.

    Parameters
    ----------
    expression : str
        screen expression


    Examples
    --------
    >>> screener = Screener('U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010")')
    >>> print(list(screener))
    """

    def __init__(self, expression):
        super().__init__(f"screen({expression})")
