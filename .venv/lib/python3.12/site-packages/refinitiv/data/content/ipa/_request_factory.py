from typing import Union, Any

import numpy as np
import pandas as pd

from ._enums import Axis
from ..._tools import ArgsParser, merge_dict_to_dict
from ...delivery._data._data_provider import RequestFactory
from ...delivery.endpoint_request import RequestMethod

types_by_axis = {
    Axis.DATE: "datetime64",
    "startDate": "datetime64",
    "endDate": "datetime64",
    Axis.DELTA: float,
    Axis.EXPIRY: float,
    Axis.MONEYNESS: float,
    Axis.STRIKE: float,
    Axis.TENOR: float,
    "discountFactor": float,
    "ratePercent": float,
}


def get_type_by_axis(axis):
    axis_values_type = types_by_axis.get(axis)

    if not axis_values_type:
        raise ValueError(f"Cannot find axis's values type for axis {axis}.")

    return axis_values_type


def parse_value(value: Any) -> Union[float, int, np.datetime64]:
    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            pass
        else:
            return value

        try:
            value = pd.to_datetime(value).to_numpy()
        except ValueError:
            try:
                value = pd.to_datetime(value, dayfirst=True).to_numpy()
            except ValueError:
                pass
        else:
            return value

        try:
            value = float(value)
        except ValueError:
            raise ValueError(f"not valid format: {value}")

    return value


value_arg_parser = ArgsParser(parse_value)
x_arg_parser = value_arg_parser
y_arg_parser = value_arg_parser


def parse_universe(universe):
    retval = []

    if not isinstance(universe, list):
        universe = [universe]

    # convert universe's objects into json
    for i, item in enumerate(universe):
        extended_params = None
        if not hasattr(item, "get_dict"):
            kwargs = item._kwargs
            item = kwargs.get("universe")
            extended_params = kwargs.get("extended_params")
        item_dict = item.get_dict()
        if extended_params:
            item_dict.update(extended_params)
        retval.append(item_dict)

    return retval


def parse_outputs(outputs):
    retval = []

    if not isinstance(outputs, list):
        outputs = [outputs]

    for item in outputs:
        if hasattr(item, "value"):
            item = item.value

        retval.append(item)

    return retval


universe_arg_parser = ArgsParser(parse_universe)
outputs_arg_parser = ArgsParser(parse_outputs)


class CurvesAndSurfacesRequestFactory(RequestFactory):
    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if not extended_params:
            return body_parameters

        if kwargs.get("__plural__") is True:
            body_parameters.update(extended_params)
            return body_parameters

        universes = body_parameters.get("universe", [{}])
        universes[0] = merge_dict_to_dict(universes[0], extended_params)
        return body_parameters

    def get_request_method(self, *, method=None, **kwargs):
        return method or RequestMethod.POST

    def get_body_parameters(self, *args, universe=None, outputs=None, **kwargs):
        body_parameters = {}

        # universe
        universe = universe_arg_parser.get_list(universe)
        body_parameters["universe"] = universe

        # outputs
        if outputs:
            outputs = outputs_arg_parser.get_list(outputs)
            body_parameters["outputs"] = outputs

        return body_parameters
