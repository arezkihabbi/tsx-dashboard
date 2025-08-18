from .._enums import MainConstituentAssetClass, RiskType
from ...._object_definition import ObjectDefinition


class BaseDefinitionMixin(ObjectDefinition):
    @property
    def main_constituent_asset_class(self):
        return self._get_enum_parameter(MainConstituentAssetClass, "mainConstituentAssetClass")

    @main_constituent_asset_class.setter
    def main_constituent_asset_class(self, value):
        self._set_enum_parameter(MainConstituentAssetClass, "mainConstituentAssetClass", value)

    @property
    def risk_type(self):
        return self._get_enum_parameter(RiskType, "riskType")

    @risk_type.setter
    def risk_type(self, value):
        self._set_enum_parameter(RiskType, "riskType", value)

    @property
    def base_currency(self):
        return self._get_parameter("baseCurrency")

    @base_currency.setter
    def base_currency(self, value):
        self._set_parameter("baseCurrency", value)

    @property
    def base_index_name(self):
        return self._get_parameter("baseIndexName")

    @base_index_name.setter
    def base_index_name(self, value):
        self._set_parameter("baseIndexName", value)

    @property
    def definition_expiry_date(self):
        return self._get_parameter("definitionExpiryDate")

    @definition_expiry_date.setter
    def definition_expiry_date(self, value):
        self._set_date_parameter("definitionExpiryDate", value)

    @property
    def is_fallback_for_fx_curve_definition(self):
        return self._get_parameter("isFallbackForFxCurveDefinition")

    @is_fallback_for_fx_curve_definition.setter
    def is_fallback_for_fx_curve_definition(self, value):
        self._set_parameter("isFallbackForFxCurveDefinition", value)

    @property
    def is_non_deliverable(self):
        return self._get_parameter("isNonDeliverable")

    @is_non_deliverable.setter
    def is_non_deliverable(self, value):
        self._set_parameter("isNonDeliverable", value)

    @property
    def name(self):
        return self._get_parameter("name")

    @name.setter
    def name(self, value):
        self._set_parameter("name", value)

    @property
    def quoted_currency(self):
        return self._get_parameter("quotedCurrency")

    @quoted_currency.setter
    def quoted_currency(self, value):
        self._set_parameter("quotedCurrency", value)

    @property
    def quoted_index_name(self):
        return self._get_parameter("quotedIndexName")

    @quoted_index_name.setter
    def quoted_index_name(self, value):
        self._set_parameter("quotedIndexName", value)

    @property
    def source(self):
        return self._get_parameter("source")

    @source.setter
    def source(self, value):
        self._set_parameter("source", value)


class BaseWithIdDefinitionMixin(BaseDefinitionMixin):
    @property
    def id(self):
        return self._get_parameter("id")

    @id.setter
    def id(self, value):
        self._set_parameter("id", value)
