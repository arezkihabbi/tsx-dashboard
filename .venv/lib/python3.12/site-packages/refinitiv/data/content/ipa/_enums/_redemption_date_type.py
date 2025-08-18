from enum import unique

from ...._base_enum import StrEnum


@unique
class RedemptionDateType(StrEnum):
    """
    - RedemptionAtAverageLife : yield and price are computed at average life (case
      of sinkable bonds)
    - RedemptionAtBestDate : yield and price are computed at the highest yield date.
    - RedemptionAtCallDate : yield and price are computed at call date (next call
      date by default).
    - RedemptionAtCustomDate : yield and price are computed at custom date specified in RedemptionDate parameter.
    - RedemptionAtMakeWholeCallDate : yield and price are computed at Make Whole
      Call date.
    - RedemptionAtMaturityDate : yield and price are computed at maturity date.
    - RedemptionAtNextDate : yield and price are computed at next redemption date
      available.
    - RedemptionAtParDate : yield and price are computed at next par.
    - RedemptionAtPremiumDate : yield and price are computed at next premium.
    - RedemptionAtPutDate : yield and price are computed at put date (next put date
      by default)..
    - RedemptionAtSinkDate : yield and price are computed at sinking fund date.
    - RedemptionAtWorstDate : yield and price are computed at the lowest yield date.
    """

    REDEMPTION_AT_AVERAGE_LIFE = "RedemptionAtAverageLife"
    REDEMPTION_AT_BEST_DATE = "RedemptionAtBestDate"
    REDEMPTION_AT_CALL_DATE = "RedemptionAtCallDate"
    REDEMPTION_AT_CUSTOM_DATE = "RedemptionAtCustomDate"
    REDEMPTION_AT_MAKE_WHOLE_CALL_DATE = "RedemptionAtMakeWholeCallDate"
    REDEMPTION_AT_MATURITY_DATE = "RedemptionAtMaturityDate"
    REDEMPTION_AT_NEXT_DATE = "RedemptionAtNextDate"
    REDEMPTION_AT_PAR_DATE = "RedemptionAtParDate"
    REDEMPTION_AT_PARTIAL_CALL_DATE = "RedemptionAtPartialCallDate"
    REDEMPTION_AT_PARTIAL_PUT_DATE = "RedemptionAtPartialPutDate"
    REDEMPTION_AT_PERPETUITY = "RedemptionAtPerpetuity"
    REDEMPTION_AT_PREMIUM_DATE = "RedemptionAtPremiumDate"
    REDEMPTION_AT_PUT_DATE = "RedemptionAtPutDate"
    REDEMPTION_AT_SINK_DATE = "RedemptionAtSinkDate"
    REDEMPTION_AT_WORST_DATE = "RedemptionAtWorstDate"
