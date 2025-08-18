from typing import Union

from ._file_downloader_facade import FileDownloader
from ._iter_object import CFSFile
from ._stream import CFSStream


class Definition:
    """
    Describes the particular file inside the bucket for further downloading.

    Parameters
    __________
    file: dict, CFSFile
        Dictionary or file object that contains the file ID and file name.

    Methods
    _______
        retrieve(session)
            Returns FileDownloader object
    """

    def __init__(self, file: Union[dict, CFSFile]):
        self._file_id = file["id"]
        self._filename_ext = file["filename"]

    def retrieve(self, session=None) -> FileDownloader:
        """
        Retrieves the FileDownloader object for further retrieval or extraction of files.

        Parameters
        ----------
        session: Session
            Session object. If it's not passed the default session will be used.

        Returns
        -------
        FileDownloader instance

        """
        stream = CFSStream(id=self._file_id).get_data(session=session)
        raw = stream.data.raw

        if raw.get("error", None):
            raise ValueError(raw["error"]["message"])

        url = raw.get("url", None)

        if not url:
            raise FileNotFoundError("file not found")

        return FileDownloader(url, self._filename_ext)
