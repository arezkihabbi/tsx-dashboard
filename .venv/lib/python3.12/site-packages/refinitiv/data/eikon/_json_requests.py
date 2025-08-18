import json
import time

from httpx import ConnectError
from .._tools._common import get_response_reason
from ..delivery._data._request import Request

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

import sys
from ._tools import is_string_type, get_default_session
from ..errors import RDError


def send_json_request(entity, payload, ID="123", debug=False, raw_response=False):
    """
    Returns the JSON response.
    This legacy can be used for advanced usage or early access to new features.

    Parameters
    ----------
    entity: string
        A string containing a service name

    payload: string, dict
        A string containing a JSON request

    debug: boolean, optional
        When set to True, the json request and response are printed.
        Default: False

    Returns
    -------
    string
        The JSON response as a string

    Raises
    ------
    ElektronError

        If daemon is disconnected

    requests.Timeout
        If request times out

    Exception
        If request fails (HTTP code other than 200)

    ElektronError
        If daemon is disconnected
    """
    _session = get_default_session()
    if _session:
        logger = _session.logger()
        logger.debug("entity: {}".format(entity))
        logger.debug("payload: {}".format(payload))

        if not is_string_type(entity):
            error_msg = "entity must be a string identifying an UDF endpoint"
            logger.error(error_msg)
            raise ValueError(error_msg)
        try:
            if is_string_type(payload):
                data = json.loads(payload)
            elif type(payload) is dict:
                data = payload
            else:
                error_msg = "payload must be a string or a dictionary"
                logger.error(error_msg)
                raise ValueError(error_msg)
        except JSONDecodeError as e:
            error_msg = "payload must be json well formed.\n"
            error_msg += str(e)
            logger.error(error_msg)
            raise e

        try:
            # build the request
            udf_request = {"Entity": {"E": entity, "W": data}, "ID": ID}
            logger.debug("Request to {} :{}".format(_session._get_udf_url(), udf_request))
            request = Request(
                method="POST",
                url=_session._get_udf_url(),
                headers={"Content-Type": "application/json"},
                # "x-tr-applicationid": _session.app_key},
                json=udf_request,
            )
            response = _session.http_request(request)

            try:
                logger.debug("HTTP Response code: {}".format(response.status_code))
                logger.debug("HTTP Response: {}".format(response.text))
            except UnicodeEncodeError:
                logger.error("HTTP Response: cannot decode error message")

            if response.status_code == 200:
                result = {}
                try:
                    result = response.json()
                    logger.debug("Response size: {}".format(sys.getsizeof(json.dumps(result))))
                except JSONDecodeError:
                    logger.error(f"Failed to decode response to json: {response.text}")

                # Manage specifically DataGrid async mode
                if entity.startswith("DataGrid") and entity.endswith("Async"):
                    ticket = _check_ticket_async(result)
                    while ticket:
                        ticket_request = {
                            "Entity": {
                                "E": entity,
                                "W": {"requests": [{"ticket": ticket}]},
                            }
                        }
                        logger.debug("Send ticket request:{}".format(ticket_request))
                        request = Request(
                            method="POST",
                            url=_session._get_udf_url(),
                            headers={"Content-Type": "application/json"},
                            json=ticket_request,
                        )
                        response = _session.http_request(request)

                        result = response.json()
                        logger.debug("Response size: {}".format(sys.getsizeof(json.dumps(result))))
                        ticket = _check_ticket_async(result)

                if not raw_response:
                    check_server_error(result)
                return response
            else:
                raise_for_status(response)

        except ConnectError as connectionError:
            error_msg = "Eikon Proxy not installed or not running. Please read the documentation to know how to install and run the proxy"
            logger.error(error_msg)
            raise RDError(401, error_msg) from connectionError


def _check_ticket_async(server_response):
    """
    Check server response.

    Check is the server response contains a ticket.

    :param server_response: request's response
    :type server_response: requests.Response
    :return: ticket value if response contains a ticket, None otherwise
    """
    logger = get_default_session().logger()
    # ticket response should contains only one key
    if len(server_response) == 1:
        for key, value in server_response.items():
            ticket = value[0]
            if ticket and ticket.get("estimatedDuration"):
                ticket_duration = int(ticket["estimatedDuration"])
                ticket_duration = min(ticket_duration, 15000)
                ticket_value = ticket["ticket"]
                message = "Receive ticket from {}, wait for {} second".format(key, ticket_duration / 1000.0)
                if ticket_duration > 1000:
                    message = message + "s"
                logger.info(message)
                time.sleep(ticket_duration / 1000.0)
                return ticket_value
    return None


def check_server_error(server_response, session=None):
    """
    Check server response.

    Check is the server response contains an HTPP error or a server error.

    :param server_response: request's response
    :type server_response: requests.Response
    :return: nothing

    :raises: Exception('HTTP error : <_message>) if response contains HTTP response
              ex: '<500 Server error>'
          or Exception('Server error (<error code>) : <server_response>') if UDF returns an error
              ex: {u'ErrorCode': 500, u'ErrorMessage': u'Requested datapoint was not found: News_Headlines', u'Id': u''}

    """
    if session:
        logger = session.logger()
    else:
        logger = get_default_session().logger()

    # check HTTP response (server response is an object that can contain ErrorCode attribute)
    if hasattr(server_response, "ErrorCode"):
        logger.error(getattr(server_response, "ErrorMessage"))
        raise RDError(server_response["ErrorCode"], getattr(server_response, "ErrorMessage"))

    # check UDF response (server response is JSON and it can contain ErrorCode + ErrorMessage keys)
    if isinstance(server_response, dict) and "ErrorCode" in server_response and "ErrorMessage" in server_response:
        error_message = server_response["ErrorMessage"]
        logger.error(error_message)
        raise RDError(server_response["ErrorCode"], error_message)

    # check DataGrid response (server response is JSON or text and it can contain error + optionally transactionId keys)
    if "error" in server_response:
        if "transactionId" in server_response:
            error_message = f"{server_response['error']} (transactionId:{server_response['transactionId']}"
        else:
            error_message = f"{server_response['error']} (no transactionId)"
        logger.error(error_message)
        raise RDError(400, error_message)


def raise_for_status(response):
    """Raises stored :class:`HTTPError`, if one occurred."""

    error_msg = ""
    if isinstance(response, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = get_response_reason(response).decode("utf-8")
        except UnicodeDecodeError:
            reason = get_response_reason(response).decode("iso-8859-1")
    else:
        reason = get_response_reason(response)

    logger = get_default_session().logger()

    if 400 <= response.status_code < 500:
        error_msg = "Client Error: %s - %s" % (reason, response.text)
    elif 500 <= response.status_code < 600:
        error_msg = "Server Error: %s - %s" % (reason, response.text)

    if error_msg:
        logger.error("Error code {} | {}".format(response.status_code, error_msg))
        raise RDError(response.status_code, error_msg)
