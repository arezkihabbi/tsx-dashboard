"""
Client File Store (CFS) is a capability of the Refinitiv Data Platform (RDP) that provides authorization and
enables access to content files stored in the publisher-supplied repository. CFS defines content ownership that is
publisher isolated. And subscribers can trust the source of the content.

CFS is engineered as a self-service metadata tool intended for publishers and subscribers. CFS provides a bucket and
file-set to organize files to simplify the interaction with publishers or subscribers. CFS doesn't store files
directly. Actual files are stored in publisher-supplied AWS S3 only one type storage that is supported by the current
CFS.
"""

__all__ = (
    "buckets",
    "file_downloader",
    "file_sets",
    "files",
    "packages",
)

from . import buckets, file_downloader, file_sets, files, packages
