"""
A file-set is an indivisible set of files that are all delivered together. They can consist of multiple files that
make up one large file or a grouping of files that represent related content. A file-set can also contain a single
file. The Publisher decides the appropriate organization of their file-sets.

Publishers are responsible for creating file-sets into Packages. A Publisher can have multiple file-sets in a bucket.

Once all files have been added to the file-set and are ready for download, the Publisher updates the file-set status
to READY. This enables the Publisher to control the release of their files and sets expectations for when the files
will be available to subscribers. File-sets with a status of READY cannot be updated or modified. Updates must be
published as a new file-set.

To access a file-set, Subscribers must have access to the bucket in which the file-set resides and have all the
claims associated with the file-set.
"""

__all__ = ("Definition",)

from ._file_sets_definition import Definition
