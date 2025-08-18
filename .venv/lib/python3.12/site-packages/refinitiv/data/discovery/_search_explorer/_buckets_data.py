from dataclasses import dataclass
from typing import List, Tuple

import pandas as pd


def get_counts_labels_filters(buckets: List[dict]) -> Tuple[List[int], List[str], List[str]]:
    filters = []
    labels = []
    counts = []
    for bucket in buckets:
        counts.append(bucket.get("Count", 0))
        labels.append(bucket.get("Label", pd.NA))

        if "Filter" in bucket:
            filters.append(bucket["Filter"])

    return counts, labels, filters


@dataclass
class BucketsData:
    """BucketsData has properties for requested navigator."""

    name: str
    value: list
    count: list
