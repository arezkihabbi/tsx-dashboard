import asyncio
import mimetypes
import os
import urllib
from dataclasses import dataclass
from typing import Callable, List
from uuid import uuid4

import httpx

from ._errors import DownloadFileError
from .._content_data import Data
from .._content_data_provider import ContentDataProvider
from .._content_response_factory import ContentResponseFactory
from .._error_parser import ErrorParser
from .._universe_content_validator import UniverseContentValidator
from ..._content_type import ContentType
from ..._tools import get_response_reason
from ...delivery._data._data_provider import EndpointData, Error, RequestFactory
from ...delivery._data._endpoint_data import RequestMethod


# ---------------------------------------------------------------------------
#   Request factory
# ---------------------------------------------------------------------------


class FilingsRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        url = super().get_url(*args, **kwargs)
        # check for value of the key, must not be None
        if kwargs.get("filename"):
            return url + "/{filename}"
        elif kwargs.get("dcn") or kwargs.get("doc_id") or kwargs.get("filing_id"):
            return url + "/search/{identifier}/{value}"
        else:
            return url

    def get_path_parameters(self, session=None, *, path_parameters=None, filename=None, **kwargs) -> dict:
        path_parameters = path_parameters or {}
        # only one of filename, dcn, doc_id and filing_id will be included in the parameter
        if filename:
            path_parameters["filename"] = filename
        else:
            identifiers = {"dcn", "doc_id", "filing_id"}
            for key, value in kwargs.items():
                if key in identifiers and value is not None:
                    path_parameters["identifier"] = key.replace("_", "")
                    path_parameters["value"] = value
        return path_parameters

    def get_header_parameters(self, session, **kwargs) -> dict:
        # This is the only header available right now. It is hard-coded in their document
        from ...delivery._data._data_provider_factory import get_api_config

        api_config = get_api_config(ContentType.FILINGS_RETRIEVAL, session.config)
        return api_config.get_dict("headers")


# ---------------------------------------------------------------------------
#   Data
# ---------------------------------------------------------------------------


@dataclass
class DownloadFileData(EndpointData):
    file_location: str = None
    is_success: bool = False


@dataclass
class DownloadFilesData:
    files: List = None


# ---------------------------------------------------------------------------
#   Download response
# ---------------------------------------------------------------------------


class DownloadFileResponse:
    def __init__(self, *args, **kwargs):
        self._is_success: bool = kwargs.get("is_success")
        files_data = [kwargs.get("content_data")]
        self.data = DownloadFilesData(files_data)
        self._status = kwargs.get("status")

        err_code = kwargs.get("error_code")
        err_message = kwargs.get("error_message")

        if err_code or err_message:
            if isinstance(err_code, list) and isinstance(err_message, list):
                errors = [Error(code, msg) for code, msg in zip(err_code, err_message)]
            else:
                errors = [Error(err_code, err_message)]
            self.errors = errors
        else:
            self.errors = []
        self._raw_response = kwargs.get("raw_response")


class DownloadAllFileResponse:
    def __init__(self, files: [DownloadFilesData] = None, errors: list = None):
        self.data = DownloadFilesData(files)
        self.errors = errors


# ---------------------------------------------------------------------------
#   File
# ---------------------------------------------------------------------------
def get_file_location_with_extension(file_location: str, extension: str):
    if file_location.endswith(extension):
        return file_location
    return file_location + extension


class FilingsFile:
    def __init__(self, filename: str = None, signed_url: str = None, mimetype: str = None):
        """
        Parameters
        ----------
        filename : str
            Name of the file
        signed_url : str
            Signed URL to download the file
        mimetype : str
            Mime type of the file
        """
        self.filename = filename
        self.signed_url = signed_url
        # Retrieving file using filename doesn't return mimetype of the file
        self.mimetype = mimetype

    @staticmethod
    def _process_response(
        file_location: str = None,
        http_response: httpx.Response = None,
        error: DownloadFileError = None,
    ) -> (DownloadFileResponse, str):
        extension = None
        if http_response is not None:
            data = {
                "is_success": http_response.is_success,
                "status": {
                    "http_status_code": http_response.status_code,
                    "http_reason": get_response_reason(http_response),
                },
                "raw_response": http_response,
            }

            if http_response.is_success:
                extension = mimetypes.guess_extension(http_response.headers.get("content-type"))
                data["content_data"] = DownloadFileData(
                    raw=http_response.__dict__,
                    file_location=get_file_location_with_extension(file_location, extension),
                    is_success=http_response.is_success,
                )
            else:
                data["error_code"] = http_response.status_code
                data["error_message"] = error.message or get_response_reason(http_response)
                data["content_data"] = DownloadFileData(
                    raw={
                        "error": {
                            "code": data["error_code"],
                            "description": data["error_message"],
                        }
                    },
                    file_location=None,
                    is_success=False,
                )
        else:
            # Only error before http request will come here
            data = {
                "is_success": False,
                "status": {
                    "http_status_code": None,
                    "http_reason": get_response_reason(http_response),
                },
                "raw_response": http_response,
                "error_code": error.code,
                "error_message": error.message,
            }
            data["content_data"] = DownloadFileData(
                raw={
                    "error": {
                        "code": data["error_code"],
                        "description": data["error_message"],
                    }
                },
                file_location=None,
                is_success=False,
            )

        return (
            DownloadFileResponse(**data),
            extension,
        )

    def _process_exception(self, http_response: httpx.Response = None, error: Exception = None) -> DownloadFileResponse:
        exception_response, _ = self._process_response(http_response=http_response, error=error)
        return exception_response

    def _prepare_and_validate_file_path(self, path):
        file_location = os.path.join(f"{path or os.getcwd()}", f"{self.filename}")
        temp_file = file_location + str(uuid4())
        if path is not None and not os.path.exists(path):
            raise DownloadFileError(None, f"No such directory exists: '{path}'")
        return file_location, temp_file

    def download(self, path: str = None) -> DownloadFileResponse:
        """

        Parameters
        ----------
        path : str
            Destination of the download file. Default is current working directory.

        Returns
        -------
        DownloadFileResponse

        """
        file_response = None
        http_response = None
        extension = ""
        file_location = ""
        temp_file = ""

        try:
            file_location, temp_file = self._prepare_and_validate_file_path(path)
            with open(temp_file, "wb") as f:
                with httpx.stream(method=RequestMethod.GET, url=self.signed_url) as http_response:
                    if http_response.is_error:
                        # Raise Error
                        raise DownloadFileError(http_response.status_code, http_response.read().decode())
                    # Process streaming data
                    for chunk in http_response.iter_bytes():
                        f.write(chunk)
                    # Check if streaming data is completely consumed
                    if http_response.is_stream_consumed:
                        file_response, extension = self._process_response(file_location, http_response)
                    else:
                        raise DownloadFileError(400, "File download is not completed.")
        except DownloadFileError as err:
            file_response = self._process_exception(http_response, err)
        except Exception as err:
            error = DownloadFileError(None, err.__str__())
            file_response = self._process_exception(http_response, error)

        if file_response is None:
            raise ValueError("File response is None!")

        if len(file_response.errors) > 0:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise DownloadFileError(
                code=file_response.errors[0].code,
                message=file_response.errors[0].message,
            )
        else:
            file_location = get_file_location_with_extension(file_location, extension)

            if os.path.exists(file_location):
                os.remove(file_location)
            os.rename(temp_file, file_location)

        return file_response

    async def download_async(self, path: str = None, callback: Callable = None) -> DownloadFileResponse:
        """

        Parameters
        ----------
        path : str
            Destination of the download file. Default is current working directory.
        callback : Callable
            Callback function will be called after the process is completed

        Returns
        -------
        DownloadFileResponse

        """
        file_response = None
        http_response = None
        extension = ""
        file_location = ""
        temp_file = ""
        client = httpx.AsyncClient()

        try:
            file_location, temp_file = self._prepare_and_validate_file_path(path)
            with open(temp_file, "wb") as f:
                async with client.stream(method=RequestMethod.GET, url=self.signed_url) as http_response:
                    if http_response.is_error:
                        # Raise Error
                        error_message = await http_response.aread()
                        raise DownloadFileError(http_response.status_code, error_message.decode())
                    # Process streaming data
                    async for chunk in http_response.aiter_bytes():
                        f.write(chunk)
                    # Check if streaming data is completely consumed
                    if http_response.is_stream_consumed:
                        file_response, extension = self._process_response(file_location, http_response)
                    else:
                        raise DownloadFileError(400, "File download is not completed.")
        except DownloadFileError as err:
            file_response = self._process_exception(http_response, err)
        except Exception as err:
            error = DownloadFileError(None, err.__str__())
            file_response = self._process_exception(http_response, error)

        await client.aclose()
        if file_response is None:
            return DownloadFileResponse(error=ValueError("File response is None!"))

        if len(file_response.errors) > 0:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        else:
            file_location = get_file_location_with_extension(file_location, extension)

            if os.path.exists(file_location):
                os.remove(file_location)
            os.rename(temp_file, file_location)

        if callback is not None and callable(callback):
            callback(file_response)

        return file_response


class ListOfFile(list):
    # For download all file at once
    # response.data.files.download() while response.data.files is a list of file
    def download(self, path: str = None) -> DownloadAllFileResponse:
        """
        Parameters
        ----------
        path : str
            Destination of the download file. Default is current working directory.

        Returns
        -------
        DownloadAllFileResponse

        """
        # Raise an exception if there are errors
        if len(self) == 0:
            raise DownloadFileError(code=None, message="Cannot download any file. Files are empty.")

        files = []
        errors = []

        for each_file in self:
            # might raise an error in case there are problems while downloading files
            try:
                response = each_file.download(path=path)
                files.extend(response.data.files)
            except DownloadFileError as err:
                errors.append(err)
        # errors should be empty because any errors will raise an exception
        download_all_response = DownloadAllFileResponse(files=files, errors=errors)

        return download_all_response

    def _chunks(self, path, n):
        for i in range(0, len(self), n):
            yield [each_file.download_async(path=path) for each_file in self[i : i + n]]

    async def download_async(self, path: str = None, callback: Callable = None) -> DownloadAllFileResponse:
        """
        Parameters
        ----------
        path : str
            Destination of the download file. Default is current working directory.
        callback: Callable
            Callback function will be called after the process is completed

        Returns
        -------
        DownloadAllFileResponse

        """
        files = []
        errors = []

        if len(self) == 0:
            errors.append(DownloadFileError(code=None, message="Cannot download any file. Files are empty."))
            return DownloadAllFileResponse(files=files, errors=errors)

        responses = []
        # Split into chunks because there will be errors when calling too many tasks at the same time
        for task in self._chunks(path, 10):
            responses.extend(await asyncio.gather(*task))

        for response in responses:
            files.extend(response.data.files)
            errors.extend(response.errors)
        errors = list(set(errors))
        download_all_response = DownloadAllFileResponse(files=files, errors=errors)

        if callback is not None and callable(callback):
            callback(download_all_response)

        return download_all_response


# ---------------------------------------------------------------------------
#   Response data
# ---------------------------------------------------------------------------


@dataclass
class FilingsData(Data):
    _files: ListOfFile = None

    @property
    def df(self):
        if self._dataframe is None and self.raw:
            # generate headers for df
            headers = [
                {"title": "Filename", "type": "string"},
                {"title": "SignedURL", "type": "string"},
                {"title": "MimeType", "type": "string"},
            ]

            # manipulate data for df
            """
            Example self._raw
            
            1. Request with filename
            {'signedUrl': 'https://cdn-filings.filings.refinitiv.com/retrieval/filings/ecpfilings_34359955599_pdf?ClientID=API_Playground&Expires=1648731287&Signature=asmxIEJpcNjF5DsbtGOVea-liyis3G53I2EJsbXJdr6wWt1~U~pntwcC7wbEvBWCLe7w0Oq0E6-NzeBkM8-W5ejIWYCsWOgGRekF1OPgBexZbVDULFqOqiFnk2tu6EXaZlExIU1DzYadnrxowDLbNSdlpYUmesWP9oTvOyyaBIFfvKaQ4dkjNYS9Bht2P7qSxqnQIGTELTAV~OIiM96JgY6eAYLdi0Yjv8TWZSqlDmapSZd~WFVnvrpKb24zt8g2Zg40XXKeI9lp1KuZ7qQqX1Bvi329Eg4L6Tx6lyBPivO1gf84xXHYyc-jSve4e5AF4FqKBDX0itWbODV1hFzdJQ__&Key-Pair-Id=APKAIDW27KNAZ6YUBN7A'}
            
            2. Request with dcn, doc_id, filing_id
            {
                'ecpfilings_97654291060_html': {
                    'signedUrl': 'https://cdn-filings.filings.refinitiv.com/retrieval/filings/ecpfilings_97654291060_html?ClientID=API_Playground&Expires=1648731287&Signature=Mj689Rgx4lMR4zMJ8ZBKW7vIVdYdl8Cy8bEkW84Lh1xe530GnzE~xHBuGV1AexrGP2QYa9lKO-DF5nVwnHzGm3RstsHtqsAFA5gbXFFp8qjgid-y-dDkV53z7YM0eePrb2fBtlKN5gSlY5jU-ueyIdiEKkhpSKQt05~SR3GXV5lPXBmyZJNEwjsVsmud6p5LjjWXPDFe1KexFSgjbtZ1QPvD5lyoPnGMJtGtPuUEtnBuJBel8Wj07LlLK9yLfJR-eMEJwreptO9IaOwFXZ78epP8~eYVSjcMFYhT5i3ku~I8OynVsBl9eA3vbWZ63-Z6qjotA93jf1hrIeYu8BdCmw__&Key-Pair-Id=APKAIDW27KNAZ6YUBN7A',
                    'mimeType': 'text/html'
                },
                'ecpfilings_97654291060_pdf': {
                    'signedUrl': 'https://cdn-filings.filings.refinitiv.com/retrieval/filings/ecpfilings_97654291060_pdf?ClientID=API_Playground&Expires=1648731287&Signature=dY~A~MSnyqTAErY2AAmHWNWOycncbGWnRvImAfxtXVd3Jz7DcofN-7rhZK6~5CEwtPY9oE1NLDlHhm4TbprAV7SEEG~h2n4iqZUtF7qC8bHQgiSTmwV10KIURLp-uto7aZIrsJQZHTmNJ4C1SrfhE041Ko6pxu-9hsMhF8VDC76mxy~l4eDqDzsxMOyGxNGMSl8a6sTNqlTGZyW61CnsUhOLGiGVfNz3itKv54GWsudAhNOtS1DwcDr~D-5b3dinJduyH4XmOJgKvMJlPxxI5ciBKZ-k2GF~2~bl08gm-XVxLyrlYdtlHPB6KohZDEgppvs921yZuOZ--NMBMPl4zg__&Key-Pair-Id=APKAIDW27KNAZ6YUBN7A',
                    'mimeType': 'application/pdf'
                },
                'ecpfilings_97654291060_dissemination_txt': {
                    'signedUrl': 'https://cdn-filings.filings.refinitiv.com/retrieval/filings/ecpfilings_97654291060_dissemination_txt?ClientID=API_Playground&Expires=1648731287&Signature=e-FxtjqWnh~Q20uL4xaNXxlZhlP7Gvqqa1uVHsbIOFgpVqZd39oKUnyNn1do8MdpUYveP~YRvHzJ8uAYncjY1NaMHixYmfoZxqcfAHasmdMwdtaAzihPxmZobLHu7kK0iIfpCglF9RH2e7yT-WhglXbdUDvlY~eVnAFPMf4Q-tkGPQGAtmR1pZvYX53GCo-XIHO3-bX-YcY4MbsAQdzqKNdaHVKySZ0RoyfJsjdOKmJFmEygfoKQvg3zL-HV2FsD9uCZXPlV9elN3OnGyXoOSOmX4unroh7vwI5NBV3pO5x37JIl~WE4a9KU6~sacGpXiz8Sg~RkaiyQMbSUR1tsVA__&Key-Pair-Id=APKAIDW27KNAZ6YUBN7A',
                    'mimeType': 'text/plain'
                }
            }
            """
            if "signedUrl" in self.raw:
                # Need to extract filename from signedURL
                url_parse = urllib.parse.urlparse(self.raw["signedUrl"])

                # url_parse.path can be '/retrieval/filings/ecpfilings_34359955599_pdf'
                # [[Filename, SignedURL, MimeType]]
                # [["ecpfilings_34359955599_pdf", self._raw["signedUrl"], ""]]
                data = [[url_parse.path.split("/")[-1], self.raw["signedUrl"], ""]]
            else:
                # we can get filename from key in self._raw in this case
                data = [
                    [filename, attributes["signedUrl"], attributes["mimeType"]]
                    for filename, attributes in self.raw.items()
                ]

            self.raw.update({"headers": headers, "data": data})
            self._dataframe = self._dfbuilder(self.raw, **self._kwargs)
        return self._dataframe

    @property
    def files(self):
        """
        Returns
        -------
        ListOfFile[FilingsFile]
        """
        if self._files is None:
            self._files = ListOfFile()
            if self.df is not None and not self.df.empty:
                self._files.extend(FilingsFile(*row) for row in self.df.values)
        return self._files


filings_retrieval_data_provider = ContentDataProvider(
    request=FilingsRequestFactory(),
    response=ContentResponseFactory(data_class=FilingsData),
    validator=UniverseContentValidator(),
    parser=ErrorParser(),
)
