"""
A package is an indivisible set of file-sets that are all delivered together. Packages can consist of multiple
file-sets.

The publisher will define the metadata for each package of content that is  available to subscribers in CFS.
Publishers are responsible for creating Packages and assigning claims to them.

The Publisher needs to create the package first and then the publisher is able to create file-sets into Packages.
"""

__all__ = ("Definition",)

from ._packages_definition import Definition
