import abc
from typing import Iterable, List, Callable

from ._parsed_data import ParsedData
from ..._tools import cached_property


class BaseValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, data: ParsedData) -> bool:
        # for override
        pass


class ContentValidator(BaseValidator):
    @classmethod
    def content_data_has_no_error(cls, data: ParsedData) -> bool:
        content_data = data.content_data
        if "ErrorCode" in content_data:
            data.error_codes = content_data.get("ErrorCode")
            data.error_messages = content_data.get("ErrorMessage")
            return False

        return True

    @classmethod
    def content_data_is_not_none(cls, data: ParsedData) -> bool:
        if data.content_data is None:
            data.error_codes = 1
            data.error_messages = "Content data is None"
            return False

        return True

    @classmethod
    def content_data_status_is_not_error(cls, data: ParsedData) -> bool:
        content_data = data.content_data
        if content_data.get("status") == "Error":
            data.error_codes = content_data.get("code", -1)
            data.error_messages = content_data.get("message")
            return False

        return True

    @classmethod
    def status_is_not_error(cls, data: ParsedData) -> bool:
        if data.status == "Error":
            content_data = data.content_data
            data.error_codes = content_data.get("code")
            data.error_messages = content_data.get("message")
            return False

        return True

    @cached_property
    def validators(self) -> List[Callable[[ParsedData], bool]]:
        return [self.content_data_is_not_none, self.content_data_status_is_not_error]

    def validate(self, data: ParsedData) -> bool:
        return all(validate(data) for validate in self.validators)


class ContentTypeValidator(BaseValidator):
    def __init__(self, allowed_content_types=None):
        if allowed_content_types is None:
            allowed_content_types = {"application/json"}
        self._allowed_content_types = allowed_content_types

    def validate(self, data: ParsedData) -> bool:
        # Checking only first part (type/subtype) of media_type
        # See https://httpwg.org/specs/rfc7231.html#media.type
        content_type = data.raw_response.headers.get("content-type", "").split(";")[0].strip()
        is_success = content_type in self._allowed_content_types

        if not is_success:
            data.error_codes = -1
            data.error_messages = (
                f"Unexpected content-type in response,\n"
                f"Expected: {self._allowed_content_types}\n"
                f"Actual: {content_type}"
            )

        return is_success


class ValidatorContainer:
    def __init__(
        self,
        validators: Iterable = None,
        content_validator: ContentValidator = None,
        content_type_validator: ContentTypeValidator = None,
        use_default_validators=True,
    ):
        content_validator = content_validator or ContentValidator()
        content_type_validator = content_type_validator or ContentTypeValidator()

        self.validators: List[BaseValidator] = list(validators) if validators else []
        if content_type_validator and use_default_validators:
            self.validators.append(content_type_validator)
        if content_validator and use_default_validators:
            self.validators.append(content_validator)

    def validate(self, data: ParsedData) -> bool:
        return all(validator.validate(data) for validator in self.validators)
