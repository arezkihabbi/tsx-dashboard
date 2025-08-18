"""Builtin discovery search templates

Created as JSON configuration by Product Owner and Search Team.
Converted to code using code-generation.
Please, don't do manual changes to it, they may be lost after the next code-generation
"""

import pandas as pd

from .namespaces import Namespace
from .search import DiscoverySearchTemplate

_filter = "RIC eq '#{ric}'"


class RICCategoryTemplate(DiscoverySearchTemplate):
    """Returns the category for a given RIC"""

    def __init__(self):
        super().__init__(
            name="RICCategory",
            pass_through_defaults={
                "view": "QuotesAndSTIRs",
                "select": "RCSAssetCategoryLeaf",
                "top": 1000,
            },
            filter=_filter,
        )

    def _search_kwargs(self, *, ric, **kwargs) -> dict:
        return super()._search_kwargs(ric=ric, **kwargs)

    def search(self, *, ric, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame

        Parameters
        ----------
        ric
            The RIC for which to search the category.

        Returns
        -------
        DataFrame
        Default columns: RCSAssetCategoryLeaf
        """
        return super().search(ric=ric, **kwargs)


class UnderlyingRICToOptionTemplate(DiscoverySearchTemplate):
    """Simple search for options on any underlying"""

    def __init__(self):
        super().__init__(
            name="UnderlyingRICToOption",
            pass_through_defaults={
                "view": "SearchAll",
                "select": "RIC,DTSubjectName,ExpiryDateString,StrikePrice,CallPutOption,ContractType,Currency",
                "order_by": "ExpiryDate,StrikePrice,CallPutOption",
                "top": 1000,
            },
            optional_placeholders=(
                "strike_price",
                "expiry_date",
                "put_call",
                "contract_type",
            ),
            filter="UnderlyingQuoteRIC eq '#{ric}' and RCSAssetCategoryLeaf eq 'Option' and IsChain eq false {{if strike_price is not none}} and StrikePrice eq #{strike_price}{{endif}} {{if expiry_date}} and ExpiryDate eq #{expiry_date}{{endif}} {{if put_call}} and CallPutOption eq '#{put_call}'{{endif}} {{if contract_type}} and ContractType eq '#{contract_type}'{{endif}}",
        )

    def _search_kwargs(
        self,
        *,
        ric,
        contract_type=None,
        expiry_date=None,
        put_call=None,
        strike_price=None,
        **kwargs,
    ) -> dict:
        return super()._search_kwargs(
            contract_type=contract_type,
            expiry_date=expiry_date,
            put_call=put_call,
            ric=ric,
            strike_price=strike_price,
            **kwargs,
        )

    def search(
        self,
        *,
        ric,
        contract_type=None,
        expiry_date=None,
        put_call=None,
        strike_price=None,
        **kwargs,
    ) -> pd.DataFrame:
        """Launch search, get DataFrame

        Parameters
        ----------
        ric

        strike_price

        expiry_date

        put_call

        contract_type

        Returns
        -------
        DataFrame
        Default columns: RIC, DTSubjectName, ExpiryDateString, StrikePrice, CallPutOption, ContractType, Currency
        """
        return super().search(
            contract_type=contract_type,
            expiry_date=expiry_date,
            put_call=put_call,
            ric=ric,
            strike_price=strike_price,
            **kwargs,
        )


class UnderlyingRICToFutureTemplate(DiscoverySearchTemplate):
    """Simple search for futures on any underlying"""

    def __init__(self):
        super().__init__(
            name="UnderlyingRICToFuture",
            pass_through_defaults={
                "view": "SearchAll",
                "select": "RIC,DTSubjectName,ExpiryDateString,ContractType,Currency",
                "order_by": "ExpiryDate",
                "top": 1000,
            },
            filter="UnderlyingQuoteRIC eq '#{ric}' and RCSAssetCategoryLeaf eq 'Future' and IsChain eq false and AssetStateName eq 'Active'",
        )

    def _search_kwargs(self, *, ric, **kwargs) -> dict:
        return super()._search_kwargs(ric=ric, **kwargs)

    def search(self, *, ric, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame

        Parameters
        ----------
        ric
            The underlying instrument for which to search for futures.

        Returns
        -------
        DataFrame
        Default columns: RIC, DTSubjectName, ExpiryDateString, ContractType, Currency
        """
        return super().search(ric=ric, **kwargs)


class RICToIssuerTemplate(DiscoverySearchTemplate):
    """Find issuer of a RIC"""

    def __init__(self):
        super().__init__(
            name="RICToIssuer",
            pass_through_defaults={
                "view": "SearchAll",
                "select": "DTSubjectName,RCSIssuerCountryLeaf,IssuerOAPermID,PrimaryRIC",
                "top": 1000,
            },
            filter=_filter,
        )

    def _search_kwargs(self, *, ric, **kwargs) -> dict:
        return super()._search_kwargs(ric=ric, **kwargs)

    def search(self, *, ric, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame

        Parameters
        ----------
        ric
            The RIC for which to search the issuer.

        Returns
        -------
        DataFrame
        Default columns: DTSubjectName, RCSIssuerCountryLeaf, IssuerOAPermID, PrimaryRIC
        """
        return super().search(ric=ric, **kwargs)


class FutureRICToFutureTemplate(DiscoverySearchTemplate):
    """From one future RIC, find all other futures on its underlying"""

    def __init__(self):
        super().__init__(
            name="FutureRICToFuture",
            pass_through_defaults={
                "view": "SearchAll",
                "select": "RicRoot,RIC,DTSubjectName,ExpiryDateString,ContractType,Currency",
                "order_by": "GrossTonnage desc",
                "top": 1000,
            },
            filter="RicRoot eq '#{_.GetRoot.RicRoot.0}' and RCSAssetCategoryLeaf xeq 'Equity Future' and IsChain eq false and AssetStateName eq 'Active' and DisplayType ne 'CONTN'",
            ns=Namespace(
                _=Namespace(
                    GetRoot=DiscoverySearchTemplate(
                        pass_through_defaults={
                            "view": "SearchAll",
                            "select": "RicRoot",
                            "top": 1,
                        },
                        filter=_filter,
                    )
                )
            ),
        )

    def _search_kwargs(self, **kwargs) -> dict:
        return super()._search_kwargs(**kwargs)

    def search(self, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame

        Parameters
        ----------
        ric

        Returns
        -------
        DataFrame
        Default columns: RicRoot, RIC, DTSubjectName, ExpiryDateString, ContractType, Currency
        """
        return super().search(**kwargs)


class OrganisationPermIDToUPTemplate(DiscoverySearchTemplate):
    """Find ultimate parent of an organisation"""

    def __init__(self):
        super().__init__(
            name="OrganisationPermIDToUP",
            pass_through_defaults={
                "view": "SearchAll",
                "select": "UltimateParentCompanyOAPermID,UltimateParentOrganisationName",
                "top": 1000,
            },
            filter="OAPermID eq '#{entity_id}'",
        )

    def _search_kwargs(self, *, entity_id, **kwargs) -> dict:
        return super()._search_kwargs(entity_id=entity_id, **kwargs)

    def search(self, *, entity_id, **kwargs) -> pd.DataFrame:
        """Launch search, get DataFrame

        Parameters
        ----------
        entity_id
            PermID of the organisation.

        Returns
        -------
        DataFrame
        Default columns: UltimateParentCompanyOAPermID, UltimateParentOrganisationName
        """
        return super().search(entity_id=entity_id, **kwargs)
