import gzip
import os

from ._tools import path_join, create_dirs_if_no_exists
from ._tools import remove_ext
from ..._core.log_reporter import _LogReporter


class _Unpacker(_LogReporter):
    def __init__(self, logger) -> None:
        super().__init__(logger=logger)

    def unpack(self, filepath, extract_path="") -> str:
        self._is_debug() and self._debug("start extracting file")

        *_, filename_ext = os.path.split(filepath)
        extracted_filename = remove_ext(filename_ext)

        if not extract_path:
            extract_filepath = remove_ext(filepath)

        else:
            create_dirs_if_no_exists(extract_path)
            extract_filepath = path_join(extract_path, extracted_filename)

        self._is_debug() and self._debug(f"extract file '{filename_ext}' to '{extract_filepath}'")

        with gzip.open(filepath, "rb") as gzip_file:
            try:
                with open(extract_filepath, "wb+") as file:
                    file.write(gzip_file.read())
            except Exception as e:
                self._error(str(e))
                raise e

        self._is_debug() and self._debug("file extracted successfully")

        return extract_filepath
