from dataclasses import dataclass


@dataclass
class ImageData:
    width: int
    height: int
    size: int
    id: str
    content_type: str
    rendition: str

    @classmethod
    def from_dict(cls, datum: dict) -> "ImageData":
        return cls(
            width=datum.get("_width"),
            height=datum.get("_height"),
            size=datum.get("_size"),
            id=datum.get("_residref"),
            content_type=datum.get("_contenttype"),
            rendition=datum.get("_rendition"),
        )
