"""Content layer.

The Content layer refers to logical market data objects, representing financial items like level 1 market data prices
and quotes, News, Historical Pricing, Bond Analytics and so on. These objects are built on top of the Delivery layer
and provide value-add capabilities to manage and access the content within the interface. For example,
the pricing.stream interface is a thin layer on top of the data services offering streaming realtime market data.

In addition, interfaces such as Historical pricing and Environmental & Social Governance (ESG) are available to allow
intuitive access to request and process results. While the native back-end data format supports JSON structured
messages, the Content layer conveniently prepares data messages in a user-friendly format specific to the programming
language, such as Pandas DataFrame for Python.

Because Content layer objects are designed to simplify access to specific Web Services exposed by the Refinitiv Data,
these objects have a strong dependency on specific API versions of these services. They are easy to use but also
service dependant. This is not the case for the object of the Delivery layer that are lower level but also service
agnostic. Please refer to the Delivery layer documentation to learn more about these objects and when to use them.

The Content layer can easily be used by both professional developers and financial coders. It provides great
flexibility for familiar and commonly used financial data models.
"""

from typing import TYPE_CHECKING as _TYPE_CHECKING

from .._tools import lazy_attach as _attach

if _TYPE_CHECKING:
    from . import (
        custom_instruments,
        esg,
        estimates,
        filings,
        fundamental_and_reference,
        historical_pricing,
        ipa,
        news,
        ownership,
        pricing,
        search,
        symbol_conversion,
        trade_data_service,
    )
    from ..delivery._data._data_provider import Response  # noqa: F401

_submodules = {
    "custom_instruments",
    "esg",
    "estimates",
    "filings",
    "fundamental_and_reference",
    "historical_pricing",
    "ipa",
    "news",
    "ownership",
    "pricing",
    "search",
    "symbol_conversion",
    "trade_data_service",
}

_submod_attrs = {".delivery._data._data_provider": ["Response"]}

__getattr__, __dir__, __all__ = _attach(__name__, submodules=_submodules, submod_attrs=_submod_attrs)
