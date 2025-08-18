"""
Represents files that are stored in CFS.

Subscribers can only access the files to which they are entitled. On AWS S3, Subscribers can access files using a
signed URI that redirects to the file on AWS S3 for downloading.

Files are available for a defined period of time that is determined by the Publisher.
"""
__all__ = ("Definition",)

from ._files_definition import Definition
