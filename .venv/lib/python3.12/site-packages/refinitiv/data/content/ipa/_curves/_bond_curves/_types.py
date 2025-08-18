from typing import Optional


from ._curves._credit_curve_definition import CreditCurveDefinition
from ._curves._credit_constituents import CreditConstituents
from ._curves._credit_curve_parameters import CreditCurveParameters


CurveDefinition = Optional[CreditCurveDefinition]
OptCreditConstituents = Optional[CreditConstituents]
CurveParameters = Optional[CreditCurveParameters]
