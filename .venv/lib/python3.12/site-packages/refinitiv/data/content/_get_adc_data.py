from logging import Logger

from . import fundamental_and_reference
from ._content_data import Data
from .._tools import DEBUG


def get_adc_data(params: dict, logger: "Logger") -> Data:
    """
    Gets data from ADC endpoint.

    Parameters
    ----------
    params : dict
        API request parameters.
    logger : Logger
        Session logger.

    Returns
    -------
    response : Data
        API response data.

    """
    fields = params.get("fields", "")
    universe = params["universe"]
    logger.info(f"Requesting {fields} for {universe}")
    response = fundamental_and_reference.Definition(**params).get_data()
    DEBUG and logger.debug(f"ADC --->\n{response.data.df.to_string()}\n")

    request_messages = response.raw.request
    statuses = response.raw.status_code

    if not isinstance(response.raw.request, list):
        request_messages = [response.raw.request]
        statuses = [response.raw.status_code]

    for request, status in zip(request_messages, statuses):
        path = request.url.path
        current_universe = path.rsplit("/", 1)[-1]
        if current_universe not in universe:
            current_universe = universe
        logger.info(f"Request to {path} with {fields} for {current_universe}\nstatus code: {status}\n")

    return response.data
