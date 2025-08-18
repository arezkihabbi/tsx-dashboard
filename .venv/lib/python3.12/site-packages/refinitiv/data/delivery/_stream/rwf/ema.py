import os
from typing import Optional
import warnings
import re

import ema
from ema import LoginReq, OmmArray, ReqMsg, Map, ElementList, MapEntry


class IntArray(OmmArray):
    def __init__(self, values, fixed_width=2):
        super().__init__()
        self.fixed_width(fixed_width)
        for value in values:
            self.add_int(value)


# Regular expression pattern for matching ip address
IP_PATTERN = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$")


def generate_login_msg(login_msg: dict) -> dict:
    login_msg_kwargs = dict(
        application_id=login_msg["Key"]["Elements"]["ApplicationId"],
        position=login_msg["Key"]["Elements"]["Position"],
    )
    if login_msg["Key"].get("NameType"):
        login_msg_kwargs["name_type"] = name_type_map.get(login_msg["Key"]["NameType"])
        if login_msg_kwargs["name_type"] == ema.USER_AUTH_TOKEN:
            login_msg_kwargs["name"] = login_msg["Key"]["Elements"]["AuthenticationToken"]

    if "name" not in login_msg_kwargs:
        login_msg_kwargs["name"] = login_msg["Key"]["Name"]

    return login_msg_kwargs


def ema_login_message(application_id, position, name, name_type=ema.USER_NAME) -> ReqMsg:
    return LoginReq().name(name).name_type(name_type).position(position).application_id(application_id).get_message()


severity_map = {
    "verbose": ema.LoggerSeverity.Verbose.value,
    "success": ema.LoggerSeverity.Success.value,
    "warning": ema.LoggerSeverity.Warning.value,
    "error": ema.LoggerSeverity.Error.value,
    "silent": ema.LoggerSeverity.NoLogMsg.value,
}

# TODO: Find out other possible name types in json
name_type_map = {
    "AuthnToken": ema.USER_AUTH_TOKEN,
}


def logger_severity_from_env():
    logger_severity_string = os.getenv("EMA_LOGGER_SEVERITY", "silent").lower()
    if logger_severity_string not in severity_map:
        return ema.LoggerSeverity.NoLogMsg.value
    else:
        return severity_map[logger_severity_string]


def create_programmatic_cfg(
    *,
    field_dict_path: Optional[str] = None,
    enumtype_path: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
):
    config_map = Map()
    inner_map = Map()
    element_list = ElementList()

    element_list.add_ascii("DefaultConsumer", "Cons_Token")
    inner_map.add_key_ascii(
        "Cons_Token",
        MapEntry.Add,
        ElementList()
        .add_ascii("Channel", "Chan_Token")
        .add_ascii("Logger", "Logger_1")
        .add_ascii("Dictionary", "Dictionary_1")
        .add_uint("XmlTraceToStdout", 0)
        .complete(),
    ).complete()

    element_list.add_map("ConsumerList", inner_map)

    element_list.complete()
    inner_map.clear()

    config_map.add_key_ascii("ConsumerGroup", MapEntry.Add, element_list)
    element_list.clear()

    if IP_PATTERN.match(host):
        channel_type = ema.RSSL_CONN_TYPE_SOCKET
    else:
        channel_type = ema.RSSL_CONN_TYPE_ENCRYPTED

    channel_element_list = (
        ElementList()
        .add_enum("ChannelType", channel_type.value)
        .add_enum("CompressionType", ema.RSSL_COMP_NONE.value)
        .add_uint("ConnectionPingTimeout", 1000)
        .add_uint("EnableSessionManagement", 0)
        # .add_uint("GuaranteedOutputBuffers", 5000)
        .add_uint("EncryptedProtocolType", ema.RSSL_CONN_TYPE_SOCKET.value)
    )

    if host is not None:
        channel_element_list.add_ascii("Host", host)
    if port is not None:
        channel_element_list.add_uint("Port", port)

    inner_map.add_key_ascii("Chan_Token", MapEntry.Add, channel_element_list.complete()).complete()

    element_list.add_map("ChannelList", inner_map)

    element_list.complete()
    inner_map.clear()

    config_map.add_key_ascii("ChannelGroup", ema.MapEntry.Add, element_list)
    element_list.clear()

    inner_map.add_key_ascii(
        "Logger_1",
        ema.MapEntry.Add,
        ema.ElementList()
        .add_enum("LoggerType", ema.LoggerType.Stdout.value)
        .add_enum("LoggerSeverity", logger_severity_from_env())
        .complete(),
    ).complete()

    element_list.add_map("LoggerList", inner_map)

    element_list.complete()
    inner_map.clear()

    config_map.add_key_ascii("LoggerGroup", ema.MapEntry.Add, element_list)
    element_list.clear()

    if field_dict_path and enumtype_path:
        dict_elist = (
            ema.ElementList()
            .add_enum("DictionaryType", ema.DictionaryType.File.value)
            .add_ascii("RdmFieldDictionaryFileName", field_dict_path)
            .add_ascii("EnumTypeDefFileName", enumtype_path)
            .complete()
        )
    else:
        if bool(field_dict_path) ^ bool(enumtype_path):
            warnings.warn(
                "Both field_dict_path and enumtype_path need to be defined in the "
                "config file to enable file-based dictionaries."
            )

        dict_elist = ema.ElementList().add_enum("DictionaryType", ema.DictionaryType.Channel.value).complete()

    inner_map.add_key_ascii("Dictionary_1", ema.MapEntry.Add, dict_elist).complete()

    element_list.add_map("DictionaryList", inner_map)

    element_list.complete()

    config_map.add_key_ascii("DictionaryGroup", ema.MapEntry.Add, element_list)
    element_list.clear()

    config_map.complete()

    return config_map
