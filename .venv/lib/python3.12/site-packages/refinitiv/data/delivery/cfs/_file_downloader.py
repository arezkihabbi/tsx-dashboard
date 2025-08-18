import os

import requests

from ._tools import path_join, create_dirs_if_no_exists
from ..._tools import get_correct_filename
from ..._core.log_reporter import _LogReporter


class _FileDownloader(_LogReporter):
    def __init__(self, logger):
        super().__init__(logger=logger)

    def download(self, url, filename_ext, path="") -> str:
        if path and not os.path.exists(path):
            self._is_debug() and self._debug(f"creating dir '{path}'")
            create_dirs_if_no_exists(path)

        self._is_debug() and self._debug(f"start downloading file by url {url}")

        r = requests.get(url, allow_redirects=True, stream=True)
        if not r.ok:
            self._error(f"url is not valid, status_code: {r.status_code}")
            raise ValueError(f"url is not valid, status_code: {r.status_code}")

        filepath = path_join(path, get_correct_filename(filename_ext))
        self._is_debug() and self._debug(f"save file to {filepath}")
        with open(filepath, "wb") as f:
            for data in r.iter_content(None):
                f.write(data)

        r.close()

        self._is_debug() and self._debug("file downloaded successfully")

        return filepath
