"""Early access module

This module contains early access features still under development and has an unstable API.
API is subject to change without notice and a new major version release.
Please use it with caution. Avoid using it in the production code.

The structure of the module mirrors the structure of refinitiv.data library itself, just with "early_access" prefix.
When a particular feature API will be considered stable - it will be moved to the refinitiv.data, with the same path,
excluding "early_access" prefix.
For example, module "refinitiv.data.early_access.delivery.example" will be moved to "refinitiv.data.delivery.example".

To disable the warning on import, use the following code:

import sys

if not sys.warnoptions:  # avoid overriding interpreter options
    import warnings
    from refinitiv.data.errors import UnstableAPIWarning
    warnings.filterwarnings("ignore", category=UnstableAPIWarning)
"""

import warnings

from . import discovery, content
from ..warnings import UnstableAPIWarning

__all__ = ("discovery", "content")

warnings.warn(
    "You are using an unstable early access module. Avoid using its functionality in the production code."
    " To know more (including how to disable this warning), call help(refinitiv.data.early_access).",
    category=UnstableAPIWarning,
)
