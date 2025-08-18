from ..._object_definition import ObjectDefinition
from .....delivery._data._data_provider import RequestFactory
from .....delivery.endpoint_request import RequestMethod


class CrossCurrencyCurvesDefinitionsRequestFactory(RequestFactory):
    def get_request_method(self, *, method=None, **kwargs):
        return method or RequestMethod.POST

    def get_body_parameters(self, *args, request_items: ObjectDefinition, **kwargs):
        if isinstance(request_items, ObjectDefinition):
            result = request_items.get_dict()
            return result
        return {}

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if extended_params:
            result = dict(body_parameters)
            result.update(extended_params)
            return result
        return body_parameters
