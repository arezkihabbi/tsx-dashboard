from ....delivery._data import RequestMethod
from ....delivery._data._data_provider import RequestFactory


class DateScheduleRequestFactory(RequestFactory):
    def get_request_method(self, *, method=None, **kwargs):
        return method or RequestMethod.POST

    def get_body_parameters(self, *args, universe, **kwargs):
        return universe.get_dict()

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if extended_params:
            body_parameters.update(extended_params)
        return body_parameters


class DatesAndCalendarsRequestFactory(RequestFactory):
    def get_request_method(self, *, method=None, **kwargs):
        return method or RequestMethod.POST

    def get_body_parameters(self, *args, universe, **kwargs):
        body_parameters = []
        for request_item in universe:
            body_parameters.append(request_item.get_dict())
        return body_parameters

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if extended_params:
            if isinstance(extended_params, list):
                for idx, extended_param_item in enumerate(extended_params):
                    if extended_param_item:
                        body_parameters[idx].update(extended_param_item)
            else:
                for item in body_parameters:
                    item.update(extended_params)
        return body_parameters
