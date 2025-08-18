from dataclasses import dataclass
from typing import List, Optional, Union

import pandas as pd
from pandas.core.tools.datetimes import DatetimeScalar

from .. import Urgency
from .._tools import _get_headline_from_story
from ...._tools import get_from_path
from ....delivery._data._endpoint_data import EndpointData


@dataclass
class NewsStoryContent:
    html: str
    text: str


@dataclass
class Story:
    title: str
    creator: str
    source: List[dict]
    language: List[dict]
    item_codes: List[str]
    urgency: int
    content: NewsStoryContent
    headline: str
    creation_date: "DatetimeScalar"
    update_date: "DatetimeScalar"


def get_item_path(items: Union[dict, list]) -> str:
    return "0.$" if isinstance(items, list) else "$"


def story_from_dict(datum: dict) -> Story:
    inline_xml = get_from_path(datum, "newsItem.contentSet.inlineXML")
    html = get_from_path(inline_xml, get_item_path(inline_xml))

    inline_data = get_from_path(datum, "newsItem.contentSet.inlineData")
    text = get_from_path(inline_data, get_item_path(inline_data))

    story = Story(
        title=get_from_path(datum, "newsItem.itemMeta.title.0.$"),
        creator=get_from_path(datum, "newsItem.contentMeta.creator.0._qcode"),
        source=get_from_path(datum, "newsItem.contentMeta.infoSource"),
        language=get_from_path(datum, "newsItem.contentMeta.language"),
        item_codes=[item.get("_qcode") for item in get_from_path(datum, "newsItem.contentMeta.subject")],
        urgency=Urgency(get_from_path(datum, "newsItem.contentMeta.urgency.$")),
        content=NewsStoryContent(html, text),
        creation_date=pd.to_datetime(get_from_path(datum, "newsItem.itemMeta.firstCreated.$")),
        update_date=pd.to_datetime(get_from_path(datum, "newsItem.itemMeta.versionCreated.$")),
        headline=_get_headline_from_story(datum),
    )
    return story


@dataclass
class NewsStoryData(EndpointData):
    _story: Optional[Story] = None

    @staticmethod
    def _build_story(raw: dict) -> Story:
        return story_from_dict(raw)

    @property
    def story(self) -> Story:
        if self._story is None:
            self._story = self._build_story(self.raw)
        return self._story
