from dataclasses import dataclass
from typing import Optional


@dataclass
class StakeholderData:
    instrument: str
    is_public: bool
    relationship_type: str
    company_common_name: str
    related_organization_id: str
    value_chains_relationship_confidence_score: str
    value_chain_relationship_freshness_score: str
    value_chains_relationship_update_date: str
    country_of_headquarters: str
    trbc_industry_name: str
    credit_smartratios_implied_rating: str
    private_company_smartratios_implied_rating: str
    document_title: Optional[str] = None
    ric: Optional[str] = None
    issue_isin: Optional[str] = None
    sedol: Optional[str] = None

    @classmethod
    def from_list(cls, datum: list) -> "StakeholderData":
        return cls(
            instrument=datum[0],
            is_public=datum[1],
            relationship_type=datum[2],
            related_organization_id=datum[3],
            company_common_name=datum[4],
            value_chains_relationship_confidence_score=datum[5],
            value_chain_relationship_freshness_score=datum[6],
            value_chains_relationship_update_date=datum[7],
            country_of_headquarters=datum[8],
            trbc_industry_name=datum[9],
            credit_smartratios_implied_rating=datum[10],
            private_company_smartratios_implied_rating=datum[11],
        )

    def update(self, datum: dict):
        self.document_title = datum.get("DocumentTitle")
        self.ric = datum.get("RIC")
        self.issue_isin = datum.get("IssueISIN")
        self.sedol = datum.get("SEDOL")


class Customer(StakeholderData):
    pass


class Supplier(StakeholderData):
    pass
