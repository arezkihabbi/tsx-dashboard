from dataclasses import dataclass

import pandas as pd


@dataclass
class Subcategory:
    name: str
    revision_id: int
    revision_date: str
    top_news_id: str

    @classmethod
    def from_dict(cls, datum: dict) -> "Subcategory":
        return cls(
            name=datum.get("name"),
            revision_id=datum.get("revisionId"),
            revision_date=pd.to_datetime(datum.get("revisionDate")),
            top_news_id=datum.get("topNewsId"),
        )
