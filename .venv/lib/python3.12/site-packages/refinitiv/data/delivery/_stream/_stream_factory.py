import itertools
from dataclasses import dataclass
from typing import Dict, Type, TYPE_CHECKING, Union, Tuple

from ._dictionary_stream import PrvDictionaryStream
from ._off_stream_contrib_connection import OffStreamContribConnection
from ._offstream import _OffStreamContrib
from ._protocol_type import ProtocolType
from ._stream_cxn_config_provider import get_cxn_config, release_cxn_cfg_provider
from .omm_stream_connection import OMMStreamConnection
from .rdp_stream_connection import RDPStreamConnection
from .._data._api_type import APIType
from ... import _log as log
from ..._content_type import ContentType
from ..._types import OptDict, OptStr, ExtendedParams

if TYPE_CHECKING:
    from ._stream_cxn_config_data import StreamCxnConfig
    from . import StreamConnection
    from ..._core.session import Session


def get_logger():
    return log.root_logger().getChild("stream-factory")


protocol_type_by_name: Dict[str, ProtocolType] = {
    "OMM": ProtocolType.OMM,
    "RDP": ProtocolType.RDP,
}

default_api_config_key_by_api_type = {
    APIType.STREAMING_FINANCIAL_CONTRACTS: "financial-contracts",
    APIType.STREAMING_PRICING: "main",
    APIType.STREAMING_TRADING: "redi",
    APIType.STREAMING_BENCHMARK: "resource",
    APIType.STREAMING_CUSTOM_INSTRUMENTS: "resource",
}

api_config_key_by_api_type: Dict[APIType, str] = {
    APIType.STREAMING_FINANCIAL_CONTRACTS: "apis.streaming.quantitative-analytics.endpoints",
    APIType.STREAMING_PRICING: "apis.streaming.pricing.endpoints",
    APIType.STREAMING_TRADING: "apis.streaming.trading-analytics.endpoints",
    APIType.STREAMING_BENCHMARK: "apis.streaming.benchmark.endpoints",
    APIType.STREAMING_CUSTOM_INSTRUMENTS: "apis.streaming.custom-instruments.endpoints",
}

service_config_key_by_api_type = {
    APIType.STREAMING_FINANCIAL_CONTRACTS: "apis.streaming.quantitative-analytics.service",
    APIType.STREAMING_PRICING: "apis.streaming.pricing.service",
    APIType.STREAMING_TRADING: "apis.streaming.trading-analytics.service",
    APIType.STREAMING_BENCHMARK: "apis.streaming.benchmark.service",
    APIType.STREAMING_CUSTOM_INSTRUMENTS: "apis.streaming.custom-instruments.service",
}

api_type_by_content_type: Dict[ContentType, APIType] = {
    ContentType.STREAMING_CHAINS: APIType.STREAMING_PRICING,
    ContentType.STREAMING_PRICING: APIType.STREAMING_PRICING,
    ContentType.STREAMING_DICTIONARY: APIType.STREAMING_PRICING,
    ContentType.STREAMING_TRADING: APIType.STREAMING_TRADING,
    ContentType.STREAMING_CONTRACTS: APIType.STREAMING_FINANCIAL_CONTRACTS,
    ContentType.STREAMING_CUSTOM_INSTRUMENTS: APIType.STREAMING_CUSTOM_INSTRUMENTS,
    ContentType.STREAMING_CONTRIB: APIType.STREAMING_PRICING,
    ContentType.STREAMING_OFF_CONTRIB: APIType.STREAMING_PRICING,
    ContentType.STREAMING_OMM: APIType.STREAMING_PRICING,
    ContentType.STREAMING_RDP: APIType.STREAMING_CUSTOM,
}

connection_id_iterator = itertools.count(0)


def get_default_config_path(api_type) -> Union[str, None]:
    default_config_path = None
    api_key = api_config_key_by_api_type.get(api_type)
    default_api = default_api_config_key_by_api_type.get(api_type)
    if api_key and default_api:
        default_config_path = f"{api_key}.{default_api}"

    return default_config_path


@dataclass
class StreamDetails:
    content_type: ContentType
    protocol_type: ProtocolType
    api_type: APIType
    _api_config_key: str = ""

    @property
    def api_config_key(self):
        if not self._api_config_key:
            self._api_config_key = get_default_config_path(self.api_type)
        return self._api_config_key


def content_type_to_details(content_type: ContentType) -> StreamDetails:
    api_type = api_type_by_content_type.get(content_type, APIType.STREAMING_CUSTOM)

    if content_type is ContentType.NONE:
        raise ValueError("Cannot create StreamDetails, without api.")

    return StreamDetails(content_type, ProtocolType.NONE, api_type)


def get_service_and_details_omm(
    content_type: ContentType, session: "Session", service: str = "", api: str = ""
) -> Tuple[OptStr, StreamDetails]:
    if content_type is ContentType.NONE:
        raise ValueError(f"Cannot get service and details for OMM stream with content_type: {ContentType.NONE}")

    api_type = APIType.STREAMING_CUSTOM if api else api_type_by_content_type.get(content_type, APIType.STREAMING_CUSTOM)

    if not service:
        service = session.config.get(service_config_key_by_api_type.get(api_type))

    return service, StreamDetails(content_type, ProtocolType.OMM, api_type, api)


def get_service_and_details_rdp(
    content_type: ContentType, session: "Session", service: str = "", api: str = ""
) -> Tuple[OptStr, StreamDetails]:
    if content_type is ContentType.NONE:
        raise ValueError(f"Cannot get service and details for OMM stream with content_type: {ContentType.NONE}")

    api_type = APIType.STREAMING_CUSTOM if api else api_type_by_content_type.get(content_type, APIType.STREAMING_CUSTOM)

    if not service:
        service = session.config.get(service_config_key_by_api_type.get(api_type))

    return service, StreamDetails(content_type, ProtocolType.RDP, api_type, api)


def get_protocol_type_by_name(protocol_name: str) -> ProtocolType:
    protocol_type = protocol_type_by_name.get(protocol_name)

    if not protocol_type:
        raise ValueError(f"Can't find protocol type by name: {protocol_name}")

    return protocol_type


cxn_class_by_protocol_type: Dict[ProtocolType, Type[Union[OMMStreamConnection, RDPStreamConnection]]] = {
    ProtocolType.OMM: OMMStreamConnection,
    ProtocolType.OMM_OFF_CONTRIB: OffStreamContribConnection,
    ProtocolType.RDP: RDPStreamConnection,
}


def load_config(details: StreamDetails, session: "Session") -> "StreamCxnConfig":
    api_type = details.api_type

    if api_type is APIType.STREAMING_CUSTOM:
        api_config_key = details.api_config_key

        if not api_config_key:
            raise ValueError("For APIType.STREAMING_CUSTOM, api_config_key cannot be None")

        sess_config = session.config

        if not api_config_key.startswith("apis."):
            api_config_key = f"apis.{api_config_key}"

        if api_config_key.endswith(".path"):
            api_config_key = api_config_key[:-5]

        if not sess_config.get(api_config_key):
            raise ValueError(f"Path to url {api_config_key} does not exist in the config")

        end_word = api_config_key.rsplit(".", 1)[-1]
        if not end_word or end_word == "endpoints":
            raise ValueError(f"Not a valid format, use `apis.streaming.xxx.endpoints.xxx")

    else:
        api_config_key = get_default_config_path(api_type)

    config: "StreamCxnConfig" = get_cxn_config(api_config_key, session)
    logger = get_logger()
    log.is_debug(logger) and logger.debug(f"Loaded config for {api_type}, config key is {api_config_key}, {config}")
    release_cxn_cfg_provider(session)
    return config


def create_stream_cxn(details: StreamDetails, session: "Session") -> "StreamConnection":
    content_type = details.content_type
    protocol_type = details.protocol_type
    config = load_config(details, session)
    session_id = session.session_id
    connection_id = next(connection_id_iterator)
    name = f"{protocol_type.name}{content_type.name}_{session_id}.{connection_id}"
    cxn_class = cxn_class_by_protocol_type.get(protocol_type)
    cxn = cxn_class(connection_id=connection_id, name=name, session=session, config=config)
    get_logger().debug(f" + Created: \n\tcxn    : {cxn}\n\tconfig : {config}")
    return cxn


def create_offstream_contrib(
    session: "Session",
    name: str,
    api: OptStr = None,
    domain: OptStr = None,
    service: OptStr = None,
) -> "_OffStreamContrib":
    content_type = ContentType.STREAMING_OFF_CONTRIB
    api_type = APIType.STREAMING_CUSTOM

    if not api:
        api_type = api_type_by_content_type.get(content_type, APIType.STREAMING_CUSTOM)

    return _OffStreamContrib(
        stream_id=session._get_omm_stream_id(),
        session=session,
        name=name,
        details=StreamDetails(content_type, ProtocolType.OMM_OFF_CONTRIB, api_type, api),
        service=service,
        domain=domain,
    )


def create_dictionary_stream(
    content_type: ContentType,
    session: "Session",
    name: str,
    api: OptStr = None,
    domain: OptStr = None,
    service: OptStr = None,
    key: OptDict = None,
    extended_params: "ExtendedParams" = None,
) -> "PrvDictionaryStream":
    if content_type is ContentType.NONE and not api:
        content_type = ContentType.STREAMING_DICTIONARY

    api_type = api_type_by_content_type.get(content_type, APIType.STREAMING_CUSTOM)
    details = StreamDetails(content_type, ProtocolType.OMM, api_type, api)
    if not service:
        service = session.config.get(service_config_key_by_api_type.get(api_type))

    stream = PrvDictionaryStream(
        stream_id=session._get_omm_stream_id(),
        session=session,
        name=name,
        details=details,
        domain=domain,
        service=service,
        key=key,
        extended_params=extended_params,
    )
    logger = get_logger()
    log.is_debug(logger) and logger.debug(f" + Created dictionary stream: {stream.classname}")
    return stream
