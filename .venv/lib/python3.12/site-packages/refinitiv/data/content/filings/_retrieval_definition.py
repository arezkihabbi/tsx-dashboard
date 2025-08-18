from typing import TYPE_CHECKING

from ._retrieval_data_provider import FilingsData
from ..._content_type import ContentType
from ..._tools import create_repr
from ...delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ..._types import OptStr


class Definition(DataProviderLayer[Response[FilingsData]]):
    """
    This class describe filename, dcn (Document Control Number), doc_id (Document ID) and
    filing_id (Financial Filing ID) to retrieve filings documents through a signed URL.

    One of the parameters is required for this class.

    Parameters
    ----------
    filename: str
        Filename is the given name of the document which also includes its file type
    dcn: str
        Document Control Number is an external identifier and an enclosed film-number specific to Edgar documents
    doc_id: str
        Document ID is a Refinitiv internal identifier assigned to financial filings documents
    filing_id: str
        Financial Filing ID is a Refinitiv internal permanent identifier assigned to each filing document

    Examples
    --------
    >>> from refinitiv.data.content import filings
    >>> definition = filings.retrieval.Definition(filename="ecpfilings_34359955599_pdf")
    >>> response = definition.get_data()
    >>> response.data.files[0].download(path="C:\\Downloads\\download_test")

    Download all files at once

    >>> response.data.files.download(path="C:\\Downloads\\download_test")
    """

    def __init__(
        self,
        filename: "OptStr" = None,
        dcn: "OptStr" = None,
        doc_id: "OptStr" = None,
        filing_id: "OptStr" = None,
    ):
        not_none_count = sum(param is not None for param in [filename, dcn, doc_id, filing_id])
        if not_none_count == 0:
            raise ValueError("One of filename, dcn, doc_id or filing_id, is required in a Definition.")
        elif not_none_count > 1:
            raise ValueError("Only one of filename, dcn, doc_id or filing_id, can be used in a Definition")

        self.filename = filename
        self.dcn = dcn
        self.doc_id = doc_id
        self.filing_id = filing_id

        super().__init__(
            ContentType.FILINGS_RETRIEVAL,
            filename=self.filename,
            dcn=self.dcn,
            doc_id=self.doc_id,
            filing_id=self.filing_id,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="retrieval",
            content=f"{{"
            f"filename='{self.filename}', "
            f"dcn='{self.dcn}', "
            f"doc_id='{self.doc_id}', "
            f"filing_id='{self.filing_id}'"
            f"}}",
        )
