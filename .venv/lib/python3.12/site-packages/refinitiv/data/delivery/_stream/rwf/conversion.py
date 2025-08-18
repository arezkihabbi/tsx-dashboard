from ema import ElementList, ReqMsg, ENAME_VIEW_DATA, ENAME_VIEW_TYPE, VT_FIELD_ID_LIST

from .ema import IntArray


def json_marketprice_msg_to_ema(msg, rdm_dict):
    streaming = msg.get("Streaming", True)
    service_name = msg["Key"].get("Service", "ELEKTRON_DD")
    name = msg["Key"]["Name"]

    ema_msg = ReqMsg().name(name).service_name(service_name).interest_after_refresh(streaming)

    if msg.get("View"):
        # WARNING: Non-existent fields will be skipped
        field_ids = [rdm_dict[item] for item in msg["View"] if item in rdm_dict]
        view_data = IntArray(field_ids).complete()
        ema_msg.payload(
            ElementList().add_uint(ENAME_VIEW_TYPE, VT_FIELD_ID_LIST).add_array(ENAME_VIEW_DATA, view_data).complete()
        )
    return ema_msg
