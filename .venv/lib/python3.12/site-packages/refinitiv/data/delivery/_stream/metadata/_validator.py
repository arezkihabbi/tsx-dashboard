import datetime
import time
import warnings
from typing import Any, Union, TYPE_CHECKING, Dict, Callable

from dateutil import parser

from refinitiv.data.delivery._stream._validator_exceptions import ValidationException, ValidationsException
from ._types import FieldType, RWFDataType

if TYPE_CHECKING:
    from ._field_description import FieldDescription
    from ._dictionary import Dictionary

INVALID_VALUE_ERROR_LOG_PATTERN = "Invalid value {0} for field {1}. Field type is {2}. {3}"
STRING_CUT_OFF_LOG_PATTERN = (
    "{0} value has been cut off to {1}, original value is {2}, the expected field's length is {3}"
)
INVALID_ENUM_ERROR_LOG_PATTERN = "Invalid enum value {0} for field {1}: {2}"

ONE_DAY_SECS = 86400


class Validator:
    @staticmethod
    def get_validated_fields_values(dic: "Dictionary", fields: dict) -> dict:
        validated_fields_values = {}
        errors = {}
        for key, value in fields.items():
            field_desc = dic.get_field(key)
            validated = value

            if field_desc is None:
                errors[key] = f"Field {key} cannot be found in metadata"
                continue

            field_desc_name = field_desc.name
            if field_desc_name in validated_fields_values:
                errors[key] = f"Field {key} already exists in the fields as {field_desc_name}"
                continue

            rwf_type = field_desc.rwf_type
            rwf_len = field_desc.rwf_len
            value_str = str(value)

            if field_desc.type == FieldType.ENUMERATED:
                try:
                    validated = Validator.validate_enum_value(dic, field_desc, value)
                except ValidationException as e:
                    errors[key] = e.value

            elif rwf_type in {RWFDataType.RWF_RMTES_STRING, RWFDataType.RWF_BUFFER} and len(value_str) > rwf_len:
                validated = value_str[:rwf_len]

            else:
                validate_value = mapping.get(rwf_type)

                if not validate_value:
                    errors[key] = INVALID_VALUE_ERROR_LOG_PATTERN.format(
                        value, field_desc_name, rwf_type, "This type is not supported"
                    )
                    continue

                try:
                    validated = validate_value(field_desc, value)
                except ValidationException as e:
                    errors[key] = e.value

            validated_fields_values[field_desc_name] = validated

        if errors:
            raise ValidationsException(errors, validated_fields_values)

        return validated_fields_values

    @staticmethod
    def check_enum_field_value(dic: "Dictionary", field_desc: "FieldDescription", value: Union[str, int]):
        error = None
        key = field_desc.name
        if isinstance(value, str):
            enum_value = dic.get_enum_value(key, value)
            if enum_value is None:
                if value.isdigit():
                    enum_value = dic.get_enum_display(key, int(value))
                    if enum_value is None:
                        error = "invalid enumerated field value"

                else:
                    error = "invalid enumerated field display"

        elif isinstance(value, int):
            enum_value = dic.get_enum_display(key, value)
            if enum_value is None:
                error = "invalid enumerated field display/value"

        else:
            error = "invalid enumerated field display/value"

        if error:
            raise ValidationException(INVALID_ENUM_ERROR_LOG_PATTERN.format(value, field_desc.name, error))

    @staticmethod
    def validate_enum_value(dic: "Dictionary", field_desc: "FieldDescription", value: Union[str, int]):
        Validator.check_enum_field_value(dic, field_desc, value)

        if isinstance(value, str) and not value.isdigit():
            validated_value = dic.get_enum_value(field_desc.name, value)
        else:
            validated_value = int(value)

        return validated_value

    @staticmethod
    def validate_string_value(field_desc: "FieldDescription", value: Any) -> str:
        validated_value = value
        if not isinstance(value, str):
            validated_value = str(value)
            if len(validated_value) > field_desc.rwf_len:
                validated_value = value[: field_desc.rwf_len]

            if not validated_value.isascii():
                non_ascii_str = ""
                for c in validated_value:
                    if ord(c) >= 128:
                        non_ascii_str = non_ascii_str + c

                if non_ascii_str:
                    raise ValidationException(
                        INVALID_VALUE_ERROR_LOG_PATTERN.format(
                            validated_value,
                            field_desc.name,
                            "ASCII string",
                            f"It includes non ASCII characters '{non_ascii_str}'",
                        )
                    )

        return validated_value

    @staticmethod
    def validate_int_value(field_desc: "FieldDescription", value: Union[int, str]) -> int:
        error = None
        validated_value = value

        if isinstance(value, str):
            try:
                validated_value = int(value)
            except Exception as e:
                error = str(e)

        elif not isinstance(value, int):
            error = "It must be integer."

        if error:
            raise ValidationException(INVALID_VALUE_ERROR_LOG_PATTERN.format(value, field_desc.name, "INT64", error))

        return validated_value

    @staticmethod
    def validate_uint_value(field_desc: "FieldDescription", value: Union[int, str]) -> int:
        validated_value = Validator.validate_int_value(field_desc, value)

        if validated_value < 0:
            raise ValidationException(
                INVALID_VALUE_ERROR_LOG_PATTERN.format(
                    validated_value, field_desc.name, "UINT64", "It must be positive integer or 0."
                )
            )

        return validated_value

    @staticmethod
    def validate_real_value(field_desc: "FieldDescription", value: Union[int, float, str]) -> Union[int, float]:
        if isinstance(value, float) or isinstance(value, int):
            return value

        elif isinstance(value, str):
            for type_value in [int, float]:
                try:
                    value = type_value(value)
                    return value
                except ValueError:
                    pass

            raise ValidationException(
                INVALID_VALUE_ERROR_LOG_PATTERN.format(
                    value, field_desc.name, "REAL64", f"field value {value} is not valid for REAL64"
                )
            )

    @staticmethod
    def validate_time_seconds_value(field_desc: "FieldDescription", value: Union[int, datetime.time, str]) -> str:
        valid = True
        error = None

        time_format = "hh:mm:ss.mmm"
        _timespec = "seconds"
        if field_desc.rwf_len == 8:
            _timespec = "milliseconds"

        if isinstance(value, int):
            if value < 0:
                valid = False
                error = f"{field_desc.name} as an integer must be positive."

            elif value >= ONE_DAY_SECS:
                warnings.warn(
                    f"For TIME field {field_desc.name}, the number means seconds of a day, {value} exceeds 86399"
                )

            else:
                _time = time.localtime(value)
                value = datetime.time(_time.tm_hour, _time.tm_min, _time.tm_sec).isoformat(timespec=_timespec)

        elif isinstance(value, datetime.time):
            value = value.isoformat(timespec=_timespec)

        elif isinstance(value, str):
            try:
                date_value = parser.parse(value)
                value = date_value.time().isoformat(_timespec)
            except parser.ParserError as e:
                valid = False
                error = str(e)

        else:
            valid = False

        if not valid:
            raise ValidationException(
                INVALID_VALUE_ERROR_LOG_PATTERN.format(
                    value, field_desc.name, f"TIME[{time_format[:field_desc.rwf_len]}]", error
                )
            )

        return value

    @staticmethod
    def validate_date_value(field_desc: "FieldDescription", value: Union[datetime.date, str, int, float]) -> str:
        valid = True
        error = None

        if isinstance(value, datetime.date):
            # convert field value from datetime.date to str.
            value = value.isoformat()

        elif isinstance(value, str):
            try:
                date_value = parser.parse(value)
                value = datetime.date(date_value.year, date_value.month, date_value.day).isoformat()
            except parser.ParserError as e:
                valid = False
                error = str(e)

        elif isinstance(value, float) or isinstance(value, int):
            _time = time.localtime(value)
            value = datetime.date(_time.tm_year, _time.tm_mon, _time.tm_mday)

        else:
            valid = False

        if not valid:
            raise ValidationException(INVALID_VALUE_ERROR_LOG_PATTERN.format(value, field_desc.name, "DATE", error))

        return value


mapping: Dict[RWFDataType, Callable[["FieldDescription", Any], Any]] = {
    RWFDataType.RWF_ASCII_STRING: Validator.validate_string_value,
    RWFDataType.RWF_INT64: Validator.validate_int_value,
    RWFDataType.RWF_UINT64: Validator.validate_uint_value,
    RWFDataType.RWF_REAL64: Validator.validate_real_value,
    RWFDataType.RWF_TIME_SECONDS: Validator.validate_time_seconds_value,
    RWFDataType.RWF_DATE: Validator.validate_date_value,
}

validator = Validator()
