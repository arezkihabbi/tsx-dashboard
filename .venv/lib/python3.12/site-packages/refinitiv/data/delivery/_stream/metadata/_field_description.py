from dataclasses import dataclass

from ._types import FieldType, RWFDataType
from ...._tools import create_repr


@dataclass(frozen=True)
class FieldDescription:
    name: str
    long_name: str
    fid: int
    type: FieldType
    length: int
    ripple_to: int
    rwf_type: RWFDataType
    rwf_len: int
    enum_length: int

    def __repr__(self):
        return create_repr(
            self,
            class_name=self.__class__.__name__,
            content=f"{{name=''{self.name}', "
            f"long_name='{self.long_name}', "
            f"fid={self.fid}, "
            f"type={self.type}, "
            f"length={self.length}"
            f"rwf_type={self.rwf_type}, "
            f"rwf_len={self.rwf_len}}}",
        )


def create_field_description(elements: dict) -> FieldDescription:
    return FieldDescription(
        name=elements["NAME"],
        long_name=elements["LONGNAME"],
        fid=elements["FID"]["Data"],
        type=FieldType(elements["TYPE"]["Data"]),
        length=elements["LENGTH"],
        ripple_to=elements.get("RIPPLETO", {}).get("Data", 0),
        rwf_type=RWFDataType(elements["RWFTYPE"]),
        rwf_len=elements["RWFLEN"],
        enum_length=elements["ENUMLENGTH"],
    )
