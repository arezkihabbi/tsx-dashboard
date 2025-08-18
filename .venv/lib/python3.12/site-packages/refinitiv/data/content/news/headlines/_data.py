from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
from pandas.core.tools.datetimes import DatetimeScalar

from .. import Urgency
from .._tools import get_headlines
from ..._content_data import Data
from ...._tools import get_from_path
from ...._types import OptInt


@dataclass
class NewsHeadlinesData(Data):
    _headlines: Optional[List["Headline"]] = None
    _limit: "OptInt" = None

    @staticmethod
    def _build_headlines(raw: dict, limit: int) -> List["Headline"]:
        return get_headlines(raw, headline_from_dict, limit)

    @property
    def headlines(self) -> List["Headline"]:
        if self._headlines is None:
            self._headlines = self._build_headlines(self.raw, self._limit)

        return self._headlines


@dataclass
class Headline:
    title: str
    creator: str
    source: List[dict]
    language: List[dict]
    item_codes: List[str]
    urgency: Urgency
    first_created: "DatetimeScalar"
    version_created: "DatetimeScalar"
    story_id: str


def headline_from_dict(datum: dict) -> Headline:
    subject = get_from_path(datum, "newsItem.contentMeta.subject")
    item_codes = [item.get("_qcode") for item in subject]

    urgency = get_from_path(datum, "newsItem.contentMeta.urgency.$")
    urgency = Urgency(urgency)

    first_created = get_from_path(datum, "newsItem.itemMeta.firstCreated.$")
    first_created = pd.to_datetime(first_created)

    version_created = get_from_path(datum, "newsItem.itemMeta.versionCreated.$")
    version_created = pd.to_datetime(version_created)

    headline = Headline(
        title=get_from_path(datum, "newsItem.itemMeta.title.0.$"),
        creator=get_from_path(datum, "newsItem.contentMeta.creator.0._qcode"),
        source=get_from_path(datum, "newsItem.contentMeta.infoSource"),
        language=get_from_path(datum, "newsItem.contentMeta.language"),
        item_codes=item_codes,
        urgency=urgency,
        first_created=first_created,
        version_created=version_created,
        story_id=datum["storyId"],
    )
    return headline
