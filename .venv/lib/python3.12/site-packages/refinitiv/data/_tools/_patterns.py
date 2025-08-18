"""ADC patterns for fincoder layer and fundamental and reference content object."""

import re

# re for ADC fields like started with "TR." case is ignored
ADC_TR_PATTERN = re.compile(r"^tr\..+", re.I)

# re for finding expressions like
# "TR.F.TotRevPerShr(SDate=0,EDate=-2,Period=FY0,Frq=FY).date"
ADC_TR_F_FUNC_WITH_DATE_PATTERN = re.compile(r"^tr\.f\..+\(.+\)\.date$", re.I)
# "TR.F.TotRevPerShr(SDate=0,EDate=-2,Period=FY0,Frq=FY)"
ADC_TR_F_FUNC_PATTERN = re.compile(r"^tr\.f\..+\(.+\)$", re.I)

# re for finding expressions like AVAIL(, AVG(
# AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum))
ADC_FUNC_PATTERN = re.compile(r"^[A-Z_\d-]*\(", re.I)

# re for finding column name include sub-string
# ..._DATE...int
# ...DATE...int
# ..._DT...int
# ...DT...int
# ...DAT...int
PRICING_DATETIME_PATTERN = re.compile(r".*(DATE|DT|DAT)\d*$")

DATE_SUBSTRINGS = {"Date", "date", "_DT", "DATE"}
