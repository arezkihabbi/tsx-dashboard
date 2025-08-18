"""
I/B/E/S (Institutional Brokers' Estimate System) delivers a complete suite of Estimates content with a global view
and is the largest contributor base in the industry. The RDP I/B/E/S Estimates API provides information about
consensus and aggregates data (26 generic measures, 23 KPI measures), company guidance data and advanced analytics.
With over 40 years of collection experience and extensive quality controls that include thousands of automated error
checks and stringent manual analysis, RDP I/B/E/S gives the clients the content they need for superior insight,
research and investment decision-making.

The I/B/E/S database currently covers over 56,000 companies in 100 markets. More than 900 firms contribute data to
I/B/E/S, from the largest global houses to regional and local brokers, with US data back to 1976 and international
data back to 1987.
"""

__all__ = (
    "Package",
    "view_actuals",
    "view_actuals_kpi",
    "view_summary",
    "view_summary_kpi",
)

from . import view_actuals, view_actuals_kpi, view_summary, view_summary_kpi
from ._enums import Package
