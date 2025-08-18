import pandas as pd

from ..._tools import convert_dtypes, NotNoneList

DF_COLUMNS = ("DocumentTitle", "Filename", "MimeType", "Dcn", "DocId", "FinancialFilingId")


class FilingDocument:
    def __init__(self, data):
        self._data = data

    @property
    def dcn(self):
        identifiers = self._data.get("Identifiers") or [{}]
        return identifiers[0].get("Dcn", "")

    @property
    def doc_id(self):
        return self._data.get("DocId", "")

    @property
    def financial_filing_id(self):
        return self._data.get("FinancialFilingId", "")

    @property
    def document_title(self):
        return self._data.get("DocumentSummary", {}).get("DocumentTitle")

    @property
    def filenames(self):
        return self._data.get("FilesMetaData", [{}])


def build_filings_search_df(content_data: dict, **_) -> pd.DataFrame:
    data = []

    if isinstance(content_data, dict):
        content_data = [content_data]

    for item in content_data:
        financial_filings = item["data"].get("FinancialFiling", [])
        for financial_filing in financial_filings:
            filing_document = FilingDocument(financial_filing.get("FilingDocument", {}))
            for filename in filing_document.filenames:
                fields = NotNoneList(
                    filing_document.document_title,
                    filename.get("FileName"),
                    filename.get("MimeType"),
                    filing_document.dcn,
                    filing_document.doc_id,
                    filing_document.financial_filing_id,
                )

                data.append(fields)

    df = pd.DataFrame(data=data, columns=DF_COLUMNS)
    df = convert_dtypes(df)

    return df
