from dataclasses import dataclass

from ._image import Image, ResizedImage
from ..._content_data_provider import ContentDataProvider
from ...._tools import ParamItem, extend_params, get_correct_filename
from ....delivery._data._data_provider import RequestFactory
from ....delivery._data._endpoint_data import EndpointData
from ....delivery._data._parsed_data import ParsedData
from ....delivery._data._response_factory import ResponseFactory, TypeResponse
from ....delivery._data._validators import ContentTypeValidator, ContentValidator, ValidatorContainer


@dataclass
class ImageData(EndpointData):
    @property
    def image(self) -> "Image":
        if "image" in self.raw:
            return ResizedImage(self.raw)
        return Image(self.raw)


query_params = [
    ParamItem("width"),
    ParamItem("height"),
]


class ImagesRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    @property
    def query_params_config(self):
        return query_params

    def get_header_parameters(self, session=None, header_parameters=None, width=None, height=None, **kwargs):
        headers = super().get_header_parameters(session, **kwargs)
        accept = "application/json"
        if width or height:
            accept = "image/jpeg"

        headers["accept"] = accept
        return headers

    def get_path_parameters(self, session=None, *, image_id=None, **kwargs):
        return {"imageId": image_id}

    def get_url(self, *args, **kwargs):
        return f"{super().get_url(*args, **kwargs)}/{{imageId}}"


def replace_from_end(s: str, old: str, new: str, count: int) -> str:
    return s[::-1].replace(old, new, count)[::-1]


def get_extension_by_image_content_type(content_type: str) -> str:
    # content_type: 'image/svg+xml'
    extension = content_type.split("/")[1]
    # extension -> 'svg+xml'
    if "+" in extension:
        extension = extension.split("+")[0]
        # extension -> 'svg'
    return extension


def get_image_filename(image_id: str, content_type: str) -> str:
    extension = get_extension_by_image_content_type(content_type)
    filename = f"{image_id}.{extension}"
    return get_correct_filename(filename, "_")


class ImagesResponseFactory(ResponseFactory):
    def create_data_success(self, raw: dict, image_id=None, headers=None, content=None, **kwargs):
        content_type = dict(headers).get("content-type")
        if content_type.startswith("image/"):
            raw = {
                "image": content,
                "filename": get_image_filename(image_id, content_type),
            }

        return self.data_class(raw=raw, _kwargs=kwargs)

    def create_success(self, parsed_data: "ParsedData", **kwargs) -> TypeResponse:
        raw_response = parsed_data.raw_response
        headers = raw_response.headers
        content = raw_response.content
        return super().create_success(parsed_data, headers=headers, content=content, **kwargs)


class ImagesContentValidator(ContentValidator):
    @property
    def validators(self):
        return [self.content_data_is_not_none]


news_images_data_provider = ContentDataProvider(
    request=ImagesRequestFactory(),
    response=ImagesResponseFactory(data_class=ImageData),
    validator=ValidatorContainer(
        content_validator=ImagesContentValidator(),
        content_type_validator=ContentTypeValidator({"application/json", "image/jpeg"}),
    ),
)
