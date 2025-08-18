from typing import Optional, TYPE_CHECKING

from ....._content_provider_layer import PosArgsWarnMixin
from ......_tools import try_copy_to_list
from ..._bond_curves._enums import (
    BusinessSector,
    CurveSubType,
    EconomicSector,
    Industry,
    IndustryGroup,
    IssuerType,
    MainConstituentAssetClass,
    Rating,
    RatingScaleSource,
    ReferenceEntityType,
    Seniority,
)
from ...._object_definition import ObjectDefinition

if TYPE_CHECKING:
    from ......_types import OptStrings, OptStr


class CreditCurveDefinition(ObjectDefinition, PosArgsWarnMixin):
    """
    Generates the credit curves for the definition provided

    Parameters
    ----------
    business_sector : BusinessSector, optional
        Trbc business sector of the economic sector.
    credit_curve_type_fallback_logic : string, optional
        Credit curve types list used to define the fallback logic in order to find the
        best credit curve. curves types are ordered by priority.
    curve_sub_type : CurveSubType, optional

    curve_tenors : string, optional
        User defined maturities to compute.
    economic_sector : EconomicSector, optional
        Trbc economic sector of the issuer.  available values are: basicmaterials,
        consumer cyclicals, consumer non-cyclicals, energy, financials, healthcare,
        industrials, technology, utilities
    industry : Industry, optional
        Trbc industry of the industry group.
    industry_group : IndustryGroup, optional
        Trbc industry group of the business sector.
    issuer_type : IssuerType, optional
        Type of the issuer. available values are: agency, corporate, munis,
        nonfinancials, sovereign, supranational
    main_constituent_asset_class : MainConstituentAssetClass, optional

    rating : Rating, optional
        Rating of the issuer. the rating can be defined by using any of: "refinitiv",
        "s&p", "moody's", "fitch", "dbrs" convention
    rating_scale_source : RatingScaleSource, optional

    reference_entity_type : ReferenceEntityType, optional
        Type of the reference entity (mandatory if referenceentity is defined).
        avialable values are:   - chainric   - bondisin   - bondric   - organisationid
        - ticker
    seniority : Seniority, optional
        Type of seniority. available values are: senior preferred, subordinate
        unsecured, senior non-preferred
    country : str, optional
        Country code of the issuer defined with alpha-2 code iso 3166 country code
        convention
    currency : str, optional
        Bond curve currency code
    id : str, optional

    name : str, optional

    reference_entity : str, optional
        Code to define the reference entity.
    source : str, optional
        Source or contributor code default value is "refinitiv"
    """

    def __init__(
        self,
        business_sector: Optional[BusinessSector] = None,
        credit_curve_type_fallback_logic: "OptStrings" = None,
        curve_sub_type: Optional[CurveSubType] = None,
        curve_tenors: "OptStrings" = None,
        economic_sector: Optional[EconomicSector] = None,
        industry: Optional[Industry] = None,
        industry_group: Optional[IndustryGroup] = None,
        issuer_type: Optional[IssuerType] = None,
        main_constituent_asset_class: Optional[MainConstituentAssetClass] = None,
        rating: Optional[Rating] = None,
        rating_scale_source: Optional[RatingScaleSource] = None,
        reference_entity_type: Optional[ReferenceEntityType] = None,
        seniority: Optional[Seniority] = None,
        country: "OptStr" = None,
        currency: "OptStr" = None,
        id: "OptStr" = None,
        name: "OptStr" = None,
        reference_entity: "OptStr" = None,
        source: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.business_sector = business_sector
        self.credit_curve_type_fallback_logic = credit_curve_type_fallback_logic
        self.curve_sub_type = curve_sub_type
        self.curve_tenors = try_copy_to_list(curve_tenors)
        self.economic_sector = economic_sector
        self.industry = industry
        self.industry_group = industry_group
        self.issuer_type = issuer_type
        self.main_constituent_asset_class = main_constituent_asset_class
        self.rating = rating
        self.rating_scale_source = rating_scale_source
        self.reference_entity_type = reference_entity_type
        self.seniority = seniority
        self.country = country
        self.currency = currency
        self.id = id
        self.name = name
        self.reference_entity = reference_entity
        self.source = source

    @property
    def business_sector(self):
        """
        Trbc business sector of the economic sector.
        :return: enum BusinessSector
        """
        return self._get_enum_parameter(BusinessSector, "businessSector")

    @business_sector.setter
    def business_sector(self, value):
        self._set_enum_parameter(BusinessSector, "businessSector", value)

    @property
    def credit_curve_type_fallback_logic(self):
        """
        Credit curve types list used to define the fallback logic in order to find the
        best credit curve. curves types are ordered by priority.
        :return: list string
        """
        return self._get_list_parameter(str, "creditCurveTypeFallbackLogic")

    @credit_curve_type_fallback_logic.setter
    def credit_curve_type_fallback_logic(self, value):
        self._set_list_parameter(str, "creditCurveTypeFallbackLogic", value)

    @property
    def curve_sub_type(self):
        """
        :return: enum CurveSubType
        """
        return self._get_enum_parameter(CurveSubType, "curveSubType")

    @curve_sub_type.setter
    def curve_sub_type(self, value):
        self._set_enum_parameter(CurveSubType, "curveSubType", value)

    @property
    def curve_tenors(self):
        """
        User defined maturities to compute.
        :return: list string
        """
        return self._get_list_parameter(str, "curveTenors")

    @curve_tenors.setter
    def curve_tenors(self, value):
        self._set_list_parameter(str, "curveTenors", value)

    @property
    def economic_sector(self):
        """
        Trbc economic sector of the issuer.  available values are: basicmaterials,
        consumer cyclicals, consumer non-cyclicals, energy, financials, healthcare,
        industrials, technology, utilities
        :return: enum EconomicSector
        """
        return self._get_enum_parameter(EconomicSector, "economicSector")

    @economic_sector.setter
    def economic_sector(self, value):
        self._set_enum_parameter(EconomicSector, "economicSector", value)

    @property
    def industry(self):
        """
        Trbc industry of the industry group.
        :return: enum Industry
        """
        return self._get_enum_parameter(Industry, "industry")

    @industry.setter
    def industry(self, value):
        self._set_enum_parameter(Industry, "industry", value)

    @property
    def industry_group(self):
        """
        Trbc industry group of the business sector.
        :return: enum IndustryGroup
        """
        return self._get_enum_parameter(IndustryGroup, "industryGroup")

    @industry_group.setter
    def industry_group(self, value):
        self._set_enum_parameter(IndustryGroup, "industryGroup", value)

    @property
    def issuer_type(self):
        """
        Type of the issuer. available values are: agency, corporate, munis,
        nonfinancials, sovereign, supranational
        :return: enum IssuerType
        """
        return self._get_enum_parameter(IssuerType, "issuerType")

    @issuer_type.setter
    def issuer_type(self, value):
        self._set_enum_parameter(IssuerType, "issuerType", value)

    @property
    def main_constituent_asset_class(self):
        """
        :return: enum MainConstituentAssetClass
        """
        return self._get_enum_parameter(MainConstituentAssetClass, "mainConstituentAssetClass")

    @main_constituent_asset_class.setter
    def main_constituent_asset_class(self, value):
        self._set_enum_parameter(MainConstituentAssetClass, "mainConstituentAssetClass", value)

    @property
    def rating(self):
        """
        Rating of the issuer. the rating can be defined by using any of: "refinitiv",
        "s&p", "moody's", "fitch", "dbrs" convention
        :return: enum Rating
        """
        return self._get_enum_parameter(Rating, "rating")

    @rating.setter
    def rating(self, value):
        self._set_enum_parameter(Rating, "rating", value)

    @property
    def rating_scale_source(self):
        """
        :return: enum RatingScaleSource
        """
        return self._get_enum_parameter(RatingScaleSource, "ratingScaleSource")

    @rating_scale_source.setter
    def rating_scale_source(self, value):
        self._set_enum_parameter(RatingScaleSource, "ratingScaleSource", value)

    @property
    def reference_entity_type(self):
        """
        Type of the reference entity (mandatory if referenceentity is defined).
        avialable values are:   - chainric   - bondisin   - bondric   - organisationid
        - ticker
        :return: enum ReferenceEntityType
        """
        return self._get_enum_parameter(ReferenceEntityType, "referenceEntityType")

    @reference_entity_type.setter
    def reference_entity_type(self, value):
        self._set_enum_parameter(ReferenceEntityType, "referenceEntityType", value)

    @property
    def seniority(self):
        """
        Type of seniority. available values are: senior preferred, subordinate
        unsecured, senior non-preferred
        :return: enum Seniority
        """
        return self._get_enum_parameter(Seniority, "seniority")

    @seniority.setter
    def seniority(self, value):
        self._set_enum_parameter(Seniority, "seniority", value)

    @property
    def country(self):
        """
        Country code of the issuer defined with alpha-2 code iso 3166 country code
        convention
        :return: str
        """
        return self._get_parameter("country")

    @country.setter
    def country(self, value):
        self._set_parameter("country", value)

    @property
    def currency(self):
        """
        Bond curve currency code
        :return: str
        """
        return self._get_parameter("currency")

    @currency.setter
    def currency(self, value):
        self._set_parameter("currency", value)

    @property
    def id(self):
        """
        :return: str
        """
        return self._get_parameter("id")

    @id.setter
    def id(self, value):
        self._set_parameter("id", value)

    @property
    def name(self):
        """
        :return: str
        """
        return self._get_parameter("name")

    @name.setter
    def name(self, value):
        self._set_parameter("name", value)

    @property
    def reference_entity(self):
        """
        Code to define the reference entity.
        :return: str
        """
        return self._get_parameter("referenceEntity")

    @reference_entity.setter
    def reference_entity(self, value):
        self._set_parameter("referenceEntity", value)

    @property
    def source(self):
        """
        Source or contributor code default value is "refinitiv"
        :return: str
        """
        return self._get_parameter("source")

    @source.setter
    def source(self, value):
        self._set_parameter("source", value)
