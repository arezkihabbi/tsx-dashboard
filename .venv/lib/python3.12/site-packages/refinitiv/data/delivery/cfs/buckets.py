"""
CFS facilitates buckets for use by Publishers to organize file-sets and files. Buckets store metadata about the files
stored in publisher-supplied repositories. Buckets align with subscriptions and can contain multiple file-sets and
files.

Publishers are responsible for creating buckets with the CFS API. This is a one-time process. The resulting bucket is
owned by one or more Publishers and is assigned a unique name that cannot be assigned to another bucket. A Publisher
can have multiple buckets if they provide more than one dataset.

Claims are used to control access to buckets, file-sets and files. CFS does not manage or create claims,
CFS only enforces them. Claims must be created in AAA. Subscribers must have at least one of the claims on the bucket
in order to access the bucket.

Attributes are used to allow Subscribers to filter and search for content. Attributes are one method that a
Subscriber can use to find files and/or file-sets.
"""

__all__ = ("Definition",)

from ._buckets_definition import Definition
