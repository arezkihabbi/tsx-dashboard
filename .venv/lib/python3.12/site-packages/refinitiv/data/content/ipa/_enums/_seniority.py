from enum import unique
from ...._base_enum import StrEnum


@unique
class Seniority(StrEnum):
    """
    - Secured (Secured Debt (Corporate/Financial) or Domestic Currency Sovereign
      Debt (Government)),
    - SeniorUnsecured (Senior Unsecured Debt (Corporate/Financial) or Foreign
      Currency Sovereign Debt (Government)),
    - Subordinated (Subordinated or Lower Tier 2 Debt (Banks)),
    - JuniorSubordinated (Junior Subordinated or Upper Tier 2 Debt (Banks)),
    - Preference (Preference Shares or Tier 1 Capital (Banks)).
    """

    JUNIOR_SUBORDINATED = "JuniorSubordinated"
    NONE = "None"
    PREFERENCE = "Preference"
    SECURED = "Secured"
    SENIOR_UNSECURED = "SeniorUnsecured"
    SUBORDINATED = "Subordinated"
