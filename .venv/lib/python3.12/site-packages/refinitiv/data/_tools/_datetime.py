import re
from datetime import timedelta, datetime, date

import dateutil.parser
from dateutil import tz

ownership_expr = re.compile("[-]?[0-9]+[MDQ]{1}[A]?")


def convert_to_datetime(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, timedelta):
        utc = tz.gettz("UTC")
        return datetime.now(tz.tzlocal()).astimezone(utc) + value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    return dateutil.parser.parse(value)


class Converter:
    def convert(self, value):
        return convert_to_datetime(value)


class Formatter:
    def to_str(self, date_time_value):
        return date_time_value.isoformat(timespec="microseconds")


class CFSFormatter:
    def to_str(self, date_time_value):
        return date_time_value.strftime("%Y-%m-%dT%H:%M:%SZ")


class OwnershipFormatter:
    def to_str(self, date_time_value):
        return date_time_value.strftime("%Y%m%d")


class FundamentalAndReferenceFormatter:
    def to_str(self, date_time):
        s = date_time.isoformat()
        return s.split("T")[0]


class IPADateTimeFormatter:
    def to_str(self, date_time_value):
        return date_time_value.strftime("%Y-%m-%dT%H:%M:%SZ")


class IPADateFormatter:
    def to_str(self, date_time_value):
        return date_time_value.strftime("%Y-%m-%d")


# yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g. 2021-01-01t00:00:00z)


class NanosecondsFormatter:
    NANOSECOND_LENGTH = 9

    def to_str(self, date_time):
        s = date_time.isoformat(timespec="microseconds")
        # s => '2021-08-03T10:33:35.554103+00:00000Z'
        s, *_ = s.split("+", maxsplit=1)
        # s => '2021-08-03T10:33:35.554103'
        s, microseconds = s.split(".", maxsplit=1)
        # microseconds => '554103'
        diff = self.NANOSECOND_LENGTH - len(microseconds)
        # nanoseconds => '554103000'
        nanoseconds = f"{microseconds}{diff * '0'}"
        # return => '2021-08-03T10:33:35.554103000Z'
        return f"{s}.{nanoseconds}Z"


class DateTimeAdapter:
    def __init__(self, converter_, formatter_):
        self.converter = converter_
        self.formatter = formatter_

    def convert(self, value):
        return self.converter.convert(value)

    def get_str(self, value):
        return self.formatter.to_str(self.convert(value))

    def get_localize(self, value):
        if value is not None:
            dt = self.converter.convert(value)
            return dt.replace(tzinfo=tz.gettz("UTC"))


class OwnerShipDateTimeAdapter(DateTimeAdapter):
    def get_str(self, value):
        if isinstance(value, str) and ownership_expr.match(value):
            return value
        return self.formatter.to_str(self.convert(value))


_nanoseconds_formatter = NanosecondsFormatter()
_date_formatter = FundamentalAndReferenceFormatter()
_ipa_datetime_formatter = IPADateTimeFormatter()
_ipa_date_formatter = IPADateFormatter()
_converter = Converter()

_z_ends_date_time_adapter = DateTimeAdapter(_converter, _nanoseconds_formatter)
_t_ends_date_time_adapter = DateTimeAdapter(_converter, _date_formatter)
hp_datetime_adapter = _z_ends_date_time_adapter
filling_search_datetime_adapter = _z_ends_date_time_adapter
fr_datetime_adapter = _t_ends_date_time_adapter
add_periods_datetime_adapter = _t_ends_date_time_adapter
tds_datetime_adapter = _z_ends_date_time_adapter
custom_inst_datetime_adapter = _z_ends_date_time_adapter
cfs_datetime_adapter = DateTimeAdapter(_converter, CFSFormatter())
ownership_datetime_adapter = OwnerShipDateTimeAdapter(_converter, OwnershipFormatter())
ipa_datetime_adapter = DateTimeAdapter(_converter, _ipa_datetime_formatter)
ipa_date_adapter = DateTimeAdapter(_converter, _ipa_date_formatter)


def to_iso_format(value):
    return convert_to_datetime(value).isoformat()
