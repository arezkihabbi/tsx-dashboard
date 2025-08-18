from typing import Union, TYPE_CHECKING

from numpy import iterable

from .._content_provider_layer import IPAContentProviderLayer
from ...._content_type import ContentType
from ...._tools import try_copy_to_list

if TYPE_CHECKING:
    from . import swaption, fx, cap, eti

    DefnDefns = Union[swaption.Definition, fx.Definition, cap.Definition, eti.Definition]


class Definitions(IPAContentProviderLayer):
    def __init__(
        self,
        universe: "DefnDefns",
    ):
        universe = try_copy_to_list(universe)
        if not iterable(universe):
            universe = [universe]

        super().__init__(
            content_type=ContentType.SURFACES,
            universe=universe,
            __plural__=True,
        )
