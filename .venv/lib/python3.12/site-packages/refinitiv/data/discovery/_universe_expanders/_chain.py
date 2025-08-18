from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

from ._universe_expander import UniverseExpander
from ..._core.session import get_default
from ..._errors import RDError, ScopeError
from ..._tools import cached_property
from ...content import fundamental_and_reference
from ...content.pricing import chain
from ...delivery import endpoint_request
from ...delivery._data._data_provider_layer import _check_response

if TYPE_CHECKING:
    from ...content.pricing.chain._stream_facade import Stream
    from ...delivery._data._response import Response

default_error_message = "No values to unpack"


def get_chain_data_from_stream(name):
    def on_error(message: tuple, universe: str, stream: "Stream"):
        message = message[0]
        state = message.get("State", {})
        message = state.get("Text", default_error_message)
        code = state.get("Code", -1)
        chain_stream.close()
        raise RDError(code, f"{message}\nuniverse: {universe}")

    chain_stream = chain.Definition(name).get_stream()
    chain_stream.on_error(on_error)
    chain_stream.open()
    chain_stream.close()
    constituents = chain_stream.constituents
    summary_links = chain_stream.summary_links
    if not constituents:
        raise RDError(-1, default_error_message)
    return ChainData(constituents, summary_links)


def get_chain_data_from_adc(name):
    adc_response = fundamental_and_reference.Definition(universe=name, fields=["TR.RIC"]).get_data()
    constituents = [item[0] for item in adc_response.data.raw.get("data", {})]
    return ChainData(constituents)


def _get_constituents(response: "Response") -> list:
    return response.data.raw.get("data", {}).get("constituents", [])


def get_chain_data_from_chain_endpoint(name):
    url = "/data/pricing/chains/v1/"
    session = get_default()
    session.verify_scope(url, "get")
    chain_response = endpoint_request.Definition(url=url, query_parameters={"universe": name}).get_data()
    _check_response(chain_response, session.config)

    summary_links = []
    constituents = []

    for item in _get_constituents(chain_response):
        if item.startswith(".") or item.startswith("/") or item.endswith("="):
            summary_links.append(item)
        else:
            constituents.append(item)

    next_link = chain_response.data.raw.get("meta", {}).get("nextLink")
    while next_link:
        chain_response = endpoint_request.Definition(
            url=url, query_parameters={"universe": name, "target": next_link}
        ).get_data()

        next_link = chain_response.data.raw.get("meta", {}).get("nextLink")
        constituents.extend(_get_constituents(chain_response))

    return ChainData(constituents, summary_links)


def get_chain_data(name):
    for func in (
        get_chain_data_from_stream,
        get_chain_data_from_adc,
    ):
        try:
            return func(name)
        except ScopeError:
            continue
    return get_chain_data_from_chain_endpoint(name)


@dataclass
class ChainData:
    constituents: List = field(default_factory=lambda: [])
    summary_links: List = field(default_factory=lambda: [])


class Chain(UniverseExpander):
    """
    Class to get data from chain.

    Parameters
    ----------
    name : str
        chain name


    Examples
    --------
    >>> chain = Chain("0#.DJI")
    >>> print(list(chain))
    >>> print(chain.constituents)
    >>> print(chain.summary_links)
    """

    def __init__(self, name):
        self._name = name

    @cached_property
    def _chains(self):
        return get_chain_data(self._name)

    @property
    def name(self):
        return self._name

    @property
    def summary_links(self):
        return self._chains.summary_links

    @property
    def constituents(self):
        return self._chains.constituents

    @property
    def _universe(self):
        return self.constituents
