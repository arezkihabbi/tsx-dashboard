from ._discovery_universe import DiscoveryUniverse


class Peers(DiscoveryUniverse):
    """
    Class to get data from peers function.

    Parameters
    ----------
    expression : str
        peers expression


    Examples
    --------
    >>> peers = Peers("VOD.L")
    >>> print(list(peers))
    """

    def __init__(self, expression):
        super().__init__(f"peers({expression})")
