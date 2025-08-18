"""Fundamental and reference.

The Fundamental And Reference module provides the access to private and public company information via "TR." data
items, includes:
- Fundamentals
- Price
- Estimates
- Indexes
- Corporate Actions
- Fixed Income
- Lipper
- Ownership, and so on.

"TR." data items and their parameters can easily be discovered in Refinitiv Workspace using the Data Item Browser (DIB).
"""

__all__ = (
    "Definition",
    "Response",
    "RowHeaders",
)

from ._definition import Definition
from ...delivery._data._data_provider import Response
from ._definition import RowHeaders
