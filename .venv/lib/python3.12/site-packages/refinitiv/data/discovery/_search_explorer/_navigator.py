from dataclasses import dataclass
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from ._buckets_data import BucketsData


@dataclass
class Navigator:
    """Navigator object that has dataframe and BucketsData object for requested navigator."""

    df: pd.DataFrame
    navigator: "BucketsData"
