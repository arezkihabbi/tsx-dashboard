from dataclasses import dataclass
from typing import List

import pandas as pd
from numpy import datetime64

from refinitiv.data._tools import get_from_path
from ._image_data import ImageData


def get_images_data(datum: dict) -> List[ImageData]:
    images_data = get_from_path(datum, "newsItem/itemMeta/link/0/remoteContent", "/") or []
    return [ImageData.from_dict(image) for image in images_data]


@dataclass
class Report:
    provider: dict
    version_created: datetime64
    first_created: datetime64
    title: str
    first_paragraph: str
    headline: str
    images: List[ImageData]

    @classmethod
    def from_dict(cls, datum) -> "Report":
        return cls(
            provider=get_from_path(datum, "newsItem/itemMeta/provider", "/"),
            version_created=pd.to_datetime(get_from_path(datum, "newsItem/itemMeta/versionCreated/$", "/")),
            first_created=pd.to_datetime(get_from_path(datum, "newsItem/itemMeta/firstCreated/$", "/")),
            title=get_from_path(datum, "newsItem/itemMeta/title/0/$", "/"),
            first_paragraph=get_from_path(datum, "newsItem/firstParagraph", "/"),
            headline=get_from_path(datum, "newsItem/contentMeta/headline/0/$", "/"),
            images=get_images_data(datum),
        )
