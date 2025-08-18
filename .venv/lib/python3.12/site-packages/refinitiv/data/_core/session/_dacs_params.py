from dataclasses import dataclass
from typing import Optional


@dataclass
class DacsParams:
    """DacsParams object."""

    deployed_platform_username: str = "user"
    dacs_application_id: str = "256"
    dacs_position: Optional[str] = None
