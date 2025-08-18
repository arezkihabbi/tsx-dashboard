from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from ._property import Property


@dataclass
class Properties:
    """Properties objects that has dataframe and dict object that holds Property objects"""

    df: pd.DataFrame
    properties: Dict[str, "Property"]
