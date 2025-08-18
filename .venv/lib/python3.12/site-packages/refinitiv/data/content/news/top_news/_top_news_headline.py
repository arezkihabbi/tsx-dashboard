from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
from numpy import datetime64


@dataclass
class TopNewsHeadline:
    version_created: datetime64
    headline: str
    story_id: str
    date_line: str
    first_created: datetime64
    snippet: str
    related_headlines: "Optional[List[TopNewsHeadline]]" = None

    @classmethod
    def from_dict(cls, datum: dict) -> "TopNewsHeadline":
        return cls(
            version_created=pd.to_datetime(datum.get("versionCreated")),
            headline=datum.get("text"),
            story_id=datum.get("storyId"),
            date_line=datum.get("dateLine"),
            first_created=pd.to_datetime(datum.get("firstCreated")),
            snippet=datum.get("snippet"),
            related_headlines=[cls.from_dict(data) for data in datum.get("relatedHeadlines", [])] or None,
        )
