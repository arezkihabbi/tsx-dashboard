from ...._tools import extend_params
from ....delivery._data._request_factory import RequestFactory


class StoryRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    def get_path_parameters(self, session=None, *, story_id=None, **kwargs):
        return {"storyId": story_id}

    def get_header_parameters(self, session=None, **kwargs):
        headers = super().get_header_parameters(session, **kwargs)
        headers["accept"] = "application/json"
        return headers

    def get_url(self, *args, **kwargs):
        return super().get_url(*args, **kwargs) + "/{storyId}"
