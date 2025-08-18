from typing import TYPE_CHECKING

from ._data_provider import ImageData
from ...._content_type import ContentType
from ...._types import ExtendedParams
from ....delivery._data._data_provider_layer import DataProviderLayer
from ....delivery._data._response import Response

if TYPE_CHECKING:
    from typing import Optional


class Definition(DataProviderLayer[Response[ImageData]]):
    """
    This class describes parameters to retrieve data for news analyze.

    Parameters
    ----------
    image_id: str
        Image ID

    width: int, optional
        New width of the image

    height: int, optional
        New height of the image

    extended_params: dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import news
    >>> definition = news.images.Definition("image_id")
    >>> response = definition.get_data()
    >>> image = response.data.image
    >>> image.save("images")
    """

    def __init__(
        self,
        image_id: str,
        width: "Optional[int]" = None,
        height: "Optional[int]" = None,
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_IMAGES,
            image_id=image_id,
            width=width,
            height=height,
            extended_params=extended_params,
        )
