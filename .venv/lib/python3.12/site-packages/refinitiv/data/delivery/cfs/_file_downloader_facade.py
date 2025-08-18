from ._file_downloader import _FileDownloader
from ._unpacker import _Unpacker
from ... import _log as log
from ..._tools import cached_property


def logger():
    return log.root_logger().getChild("file-downloader")


class FileDownloader:
    def __init__(self, url, filename_ext) -> None:
        self._url = url
        self._filename_ext = filename_ext
        self._downloaded_filepath = None

    @cached_property
    def _downloader(self) -> _FileDownloader:
        return _FileDownloader(logger())

    @cached_property
    def _unpacker(self) -> _Unpacker:
        return _Unpacker(logger())

    def download(self, path="") -> "FileDownloader":
        self._downloaded_filepath = self._downloader.download(self._url, self._filename_ext, path)
        return self

    def extract(self, path="") -> str:
        filepath = self._downloaded_filepath or self._filename_ext
        extracted_filepath = self._unpacker.unpack(filepath, path)
        return extracted_filepath
