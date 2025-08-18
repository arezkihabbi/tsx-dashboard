import base64
from os import makedirs
from os.path import join as join_path, exists
from typing import List

from ...._tools import get_from_path, cached_property


class Image:
    def __init__(self, data):
        self._data = data

    @cached_property
    def _image(self):
        file_base_64 = get_from_path(self._data, "newsItem/OtherContent/0/_", delim="/")
        return base64.b64decode(file_base_64)

    def save(self, path: str = None):
        """
        Parameters
        ----------
        path : str, optional
            Path to save file. Default is current working directory.

        """
        if path and not exists(path):
            makedirs(path)
        filename = self.filename
        if path:
            filename = join_path(path, filename)
        with open(filename, "wb+") as f:
            f.write(self._image)

    def show(self) -> "Union(Image, IPythonImage)":
        try:
            from IPython.display import Image as IPythonImage

            return IPythonImage(data=self._image)
        except ImportError:
            return self

    @property
    def size(self) -> int:
        return len(self._image)

    @cached_property
    def filename(self) -> str:
        return get_from_path(
            self._data,
            "newsItem/StoryProps/0/ContentMeta/0/HeadlineText/0/_",
            delim="/",
        )

    @cached_property
    def provider(self) -> "List[str]":
        return get_from_path(
            self._data,
            "newsItem/StoryProps/0/ItemMeta/0/Provider",
            delim="/",
        )

    @cached_property
    def body_type(self) -> "List[str]":
        return get_from_path(
            self._data,
            "newsItem/StoryProps/0/ItemMeta/0/BodyType",
            delim="/",
        )

    @cached_property
    def source(self) -> "List[str]":
        return get_from_path(
            self._data,
            "newsItem/StoryProps/0/ItemMeta/0/Source",
            delim="/",
        )

    @cached_property
    def version_created(self) -> "List[str]":
        return get_from_path(
            self._data,
            "newsItem/StoryProps/0/ItemMeta/0/VersionCreated",
            delim="/",
        )

    @cached_property
    def first_created(self) -> "List[str]":
        return get_from_path(
            self._data,
            "newsItem/StoryProps/0/ItemMeta/0/FirstCreated",
            delim="/",
        )

    @cached_property
    def available_rsf(self) -> "List[str]":
        return get_from_path(
            self._data,
            "newsItem/StoryProps/0/ItemMeta/0/AvailableRSF",
            delim="/",
        )


class ResizedImage(Image):
    @cached_property
    def _image(self):
        return self._data.get("image")

    @cached_property
    def filename(self):
        return self._data.get("filename")
