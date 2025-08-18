from typing import Optional, Union

from ..._enums import Direction, DocClause, Seniority
from ..._param_item import enum_param_item, param_item
from ..._serializable import Serializable


class ProtectionLegDefinition(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    direction : Direction or str, optional
        The direction of the leg. Optional for a single leg instrument (like a bond), in that case default value
        is Received. It is mandatory for a multi-instrument leg instrument (like Swap
        or CDS leg).
    notional_ccy : str, optional
        The ISO code of the notional currency. Mandatory if instrument code or
        instrument style has not been defined. In case an instrument code/style has been
        defined, value may comes from the reference data.
    notional_amount : float, optional
        The notional amount of the leg at the period start date. Optional. By default
        1,000,000 is used.
    doc_clause : DocClause or str, optional
        The restructuring clause or credit event for Single Name Cds. Optional.
        By default the doc_clause of the reference_entity's
        Primary Ric is used.
    seniority : Seniority or str, optional
        The order of repayment in the case of a credit event for Single Name Cds. Optional. By default
        the seniority of the reference_entity's Primary Ric is used.
    index_factor : float, optional
        The factor that is applied to the notional in case a credit event happens in one
        of the constituents of the Cds Index. Optional. By default no factor (1)
        applies.
    index_series : int, optional
        The series of the Cds Index.  Optional. By default the series of the BenchmarkRic
        is used.
    recovery_rate : float, optional
        The percentage of recovery in case of a credit event. Optional. By default the
        recovery_rate of the Cds built from reference_entity, seniority, doc_clause and
        notional_currency is used.
    recovery_rate_percent : float, optional
        The percentage of recovery in case of a credit event. Optional. By default the
        recovery_rate of the Cds built from reference_entity, seniority, doc_clause and
        notional_currency is used.
    reference_entity : str, optional
        The identifier of the reference entity, it can be:
        - for Single Name : a RedCode, an OrgId, a reference entity's RIC,
        - for Index : a RedCode, a ShortName, a CommonName. Mandatory.
    settlement_convention : str, optional
        The cashSettlementRule of the CDS. Optional. By default "3WD" (3 week days) is
        used.
    """

    def __init__(
        self,
        *,
        direction: Union[Direction, str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        doc_clause: Union[DocClause, str] = None,
        seniority: Union[Seniority, str] = None,
        index_factor: Optional[float] = None,
        index_series: Optional[int] = None,
        recovery_rate: Optional[float] = None,
        recovery_rate_percent: Optional[float] = None,
        reference_entity: Optional[str] = None,
        settlement_convention: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.direction = direction
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.doc_clause = doc_clause
        self.seniority = seniority
        self.index_factor = index_factor
        self.index_series = index_series
        self.recovery_rate = recovery_rate
        self.recovery_rate_percent = recovery_rate_percent
        self.reference_entity = reference_entity
        self.settlement_convention = settlement_convention

    def _get_items(self):
        return [
            enum_param_item.to_kv("direction", self.direction),
            enum_param_item.to_kv("docClause", self.doc_clause),
            enum_param_item.to_kv("seniority", self.seniority),
            param_item.to_kv("indexFactor", self.index_factor),
            param_item.to_kv("indexSeries", self.index_series),
            param_item.to_kv("notionalAmount", self.notional_amount),
            param_item.to_kv("notionalCcy", self.notional_ccy),
            param_item.to_kv("recoveryRate", self.recovery_rate),
            param_item.to_kv("recoveryRatePercent", self.recovery_rate_percent),
            param_item.to_kv("referenceEntity", self.reference_entity),
            param_item.to_kv("settlementConvention", self.settlement_convention),
        ]
