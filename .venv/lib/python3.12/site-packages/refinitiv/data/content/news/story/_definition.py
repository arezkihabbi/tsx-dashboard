from .._news_data_provider_layer import NewsDataProviderLayer
from ...._content_type import ContentType
from ...._tools import create_repr
from ...._types import ExtendedParams


class Definition(NewsDataProviderLayer):
    """
    This class describes parameters to retrieve data for news story.

    Parameters
    ----------
    story_id : str
        The ID of news story.

    extended_params: dict, optional
        Other parameters can be provided if necessary


    Examples
    --------
    >>> from refinitiv.data.content import news
    >>> definition = news.story.Definition("urn:newsml:reuters.com:20201026:nPt6BSyBh")
    """

    def __init__(
        self,
        story_id: str,
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_STORY,
            story_id=story_id,
            extended_params=extended_params,
        )
        self.story_id = story_id

    def __repr__(self):
        return create_repr(self, content=f"{{story_id='{self.story_id}'}}")
