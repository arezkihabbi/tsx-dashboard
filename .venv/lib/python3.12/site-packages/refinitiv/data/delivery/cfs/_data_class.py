from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..._types import OptStr, OptInt, OptBool, OptDict, OptStrings, OptDicts


@dataclass
class CFSBucket:
    attributes: "OptStrings" = None
    available_from: "OptStr" = None
    available_to: "OptStr" = None
    created: "OptStr" = None
    description: "OptStr" = None
    modified: "OptStr" = None
    name: "OptStr" = None
    private: "OptBool" = None
    publisher_name: "OptStr" = None
    restricted: "OptBool" = None

    def __iter__(self):
        return [CFSFileSet]


@dataclass
class CFSFileSet:
    attributes: "OptDicts" = None
    available_from: "OptStr" = None
    available_to: "OptStr" = None
    bucket_name: "OptStr" = None
    content_from: "OptStr" = None
    content_to: "OptStr" = None
    created: "OptStr" = None
    files: "OptStrings" = None
    id: "OptStr" = None
    modified: "OptStr" = None
    name: "OptStr" = None
    num_files: "OptInt" = None
    package_id: "OptStr" = None
    status: "OptStr" = None

    def __iter__(self):
        return [CFSFile]


@dataclass
class CFSFile:
    created: "OptStr" = None
    file_size_in_bytes: "OptInt" = None
    filename: "OptStr" = None
    fileset_id: "OptStr" = None
    href: "OptStr" = None
    id: "OptStr" = None
    modified: "OptStr" = None
    storage_location: "OptDict" = None


@dataclass
class CFSPackage:
    bucket_names: "OptStrings" = None
    claims: "OptDicts" = None
    contact_email: "OptStr" = None
    created: "OptStr" = None
    created_by: "OptStr" = None
    description: "OptStr" = None
    modified: "OptStr" = None
    modified_by: "OptStr" = None
    package_id: "OptStr" = None
    package_name: "OptStr" = None
    package_type: "OptStr" = None
    write_access_users: "OptStrings" = None
