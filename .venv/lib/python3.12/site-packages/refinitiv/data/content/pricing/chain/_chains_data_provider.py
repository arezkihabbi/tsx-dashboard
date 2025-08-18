from pandas import DataFrame

from ..._content_data_provider import ContentDataProvider
from ...._tools import convert_dtypes
from ....delivery._data._data_provider import RequestFactory

# ---------------------------------------------------------------------------
#   Content data
# ---------------------------------------------------------------------------

_response_universe_name = "universe"
_response_ric_name = "ric"
_response_display_name_name = "displayName"
_response_service_name_name = "serviceName"
_response_data_name = "data"
_response_constituents_name = "constituents"


def chains_build_df(raw, **_):
    universe = raw[_response_universe_name]
    ric = universe[_response_ric_name]
    data = raw[_response_data_name]
    constituents = data[_response_constituents_name]
    _df = None
    if len(constituents):
        _df = DataFrame({ric: constituents})
        _df = convert_dtypes(_df)
    else:
        _df = DataFrame([], columns=[ric])

    return _df


# ---------------------------------------------------------------------------
#   Request factory
# ---------------------------------------------------------------------------


class ChainsRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        url = args[1]
        url = url + "?universe={universe}"
        return url

    def get_path_parameters(self, session=None, *, universe=None, **kwargs):
        if universe is None:
            return {}
        return {"universe": universe}


# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

chains_data_provider = ContentDataProvider(
    request=ChainsRequestFactory(),
)
