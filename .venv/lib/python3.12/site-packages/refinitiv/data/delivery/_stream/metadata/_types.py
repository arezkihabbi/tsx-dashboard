from enum import Enum, auto


class FieldType(Enum):
    """
    FieldType is retrieved from RWFFld dictionary (Elements["TYPE"]).
    The data type of the field for the Marketfeed format.

    [-1, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10]
    """

    NONE = -1
    TIME_SECONDS = 0
    INTEGER = 1
    INTEGER64 = 2
    DATE = 3
    PRICE = 4
    ALPHANUMERIC = 5
    ENUMERATED = 6
    TIME = 7
    BINARY = 8
    LONG_ALPHANUMERIC = 9  # not found in RWFFld dictionary 4.20.39
    OPAQUE_TYPE = 10  # not found in RWFFld dictionary 4.20.39


class RWFDataType(Enum):
    """
    RWFDataType is retrieved from  RWFFld dictionary (Elements["RWFTYPE"]).
    Combined with Elements["RWFLEN"], RSSLDataType can be identified.

    {3, 4, 8, 9, 10, 14, 15, 16, 17, 19, 133, 136, 137, 138}
    """

    RWF_UNKNOWN = 0  # not found in RWFFld dictionary 4.20.39
    RWF_INT64 = 3
    RWF_UINT64 = 4
    RWF_FLOAT = 5  # not found in RWFFld dictionary 4.20.39
    RWF_DOUBLE = 6  # not found in RWFFld dictionary 4.20.39
    RWF_REAL64 = 8
    RWF_DATE = 9
    RWF_TIME_SECONDS = 10
    RWF_DATETIME = 11  # not found in RWFFld dictionary 4.20.39
    RWF_QOS = 12  # not found in RWFFld dictionary 4.20.39
    RWF_STATUS = 13  # not found in RWFFld dictionary 4.20.39
    RWF_ENUMERATED = 14
    RWF_ARRAY = 15
    RWF_BUFFER = 16
    RWF_ASCII_STRING = 17
    RWF_UTF8_STRING = 18  # not found in RWFFld dictionary 4.20.39
    RWF_RMTES_STRING = 19
    RWF_OPAQUE = 130  # ~buffer, not found in RWFFld dictionary 4.20.39
    RWF_XML = 131  # not found in RWFFld dictionary 4.20.39
    RWF_FIELD_LIST = 132  # not found in RWFFld dictionary 4.20.39
    RWF_ELEMENT_LIST = 133
    RWF_ANSI_PAGE = 134  # not supported by json protocol, not found in RWFFld dictionary 4.20.39
    RWF_FILTER_LIST = 135  # not found in RWFFld dictionary 4.20.39
    RWF_VECTOR = 136
    RWF_MAP = 137
    RWF_SERIES = 138
    RWF_MESSAGE = 141  # not found in RWFFld dictionary 4.20.39


class RSSLDataType(Enum):
    """
    RSSLDataType can be identified with RWFType and RWFLen
    """

    RSSL_DT_INT = auto()
    RSSL_DT_INT_1 = auto()
    RSSL_DT_INT_2 = auto()
    RSSL_DT_INT_4 = auto()
    RSSL_DT_INT_8 = auto()
    RSSL_DT_UINT = auto()
    RSSL_DT_UINT_1 = auto()
    RSSL_DT_UINT_2 = auto()
    RSSL_DT_UINT_4 = auto()
    RSSL_DT_UINT_8 = auto()
    RSSL_DT_FLOAT = auto()
    RSSL_DT_FLOAT_4 = auto()
    RSSL_DT_DOUBLE = auto()
    RSSL_DT_DOUBLE_8 = auto()
    RSSL_DT_REAL = auto()
    RSSL_DT_DATE = auto()
    RSSL_DT_DATE_4 = auto()
    RSSL_DT_TIME = auto()
    RSSL_DT_TIME_3 = auto()
    RSSL_DT_TIME_5 = auto()
    RSSL_DT_TIME_7 = auto()
    RSSL_DT_TIME_8 = auto()
    RSSL_DT_DATETIME = auto()
    RSSL_DT_DATETIME_7 = auto()
    RSSL_DT_DATETIME_9 = auto()
    RSSL_DT_DATETIME_11 = auto()
    RSSL_DT_DATETIME_12 = auto()
    RSSL_DT_QOS = auto()
    RSSL_DT_STATE = auto()
    RSSL_DT_ENUM = auto()
    RSSL_DT_BUFFER = auto()
    RSSL_DT_ASCII_STRING = auto()
    RSSL_DT_UTF8_STRING = auto()
    RSSL_DT_RMTES_STRING = auto()


# Mapping table between RWF data type and RSSL data type
#
#               0						1					2					3				4					5				6	7					8					9					10	11						12*/
# (0) 			0,						0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0
# (1) 			0,						0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0
# (2) 			0,						0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0
# INT 			RSSL_DT_INT,			RSSL_DT_INT_1,		RSSL_DT_INT_2,		0,				RSSL_DT_INT_4,		0,				0,	0,					RSSL_DT_INT_8,		0,					0,	0,						0
# UINT 			RSSL_DT_UINT,			RSSL_DT_UINT_1,		RSSL_DT_UINT_2,		0,				RSSL_DT_UINT_4,		0,				0,	0,					RSSL_DT_UINT_8,		0,					0,	0,						0
# FLOAT 		RSSL_DT_FLOAT,			0,					0,					0,				RSSL_DT_FLOAT_4,	0,				0,	0,					0,					0,					0,	0,						0
# DOUBLE 		RSSL_DT_DOUBLE,			0,					0,					0,				0,					0,				0,	0,					RSSL_DT_DOUBLE_8,	0,					0,	0,						0
# (7) 			0,						0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0
# REAL 			RSSL_DT_REAL,			0,					0,					0,				0,					0,				0,	0,					0, 					0,					0,	0,						0
# DATE          RSSL_DT_DATE,			0,					0,					0,				RSSL_DT_DATE_4,		0,				0,	0,					0, 					0,					0,	0,						0
# TIME_SECONDS	RSSL_DT_TIME,			0,					0,					RSSL_DT_TIME_3,	0,					RSSL_DT_TIME_5,	0,	RSSL_DT_TIME_7, 	RSSL_DT_TIME_8,		0,					0,	0,						0
# DATETIME 		RSSL_DT_DATETIME,		0,					0,					0,				0,					0,				0,	RSSL_DT_DATETIME_7,	0,					RSSL_DT_DATETIME_9,	0,	RSSL_DT_DATETIME_11,	RSSL_DT_DATETIME_12
# QOS 			RSSL_DT_QOS,			0,					0,					0,				0,					0,				0,	0, 					0,					0,					0,	0,						0
# STATE 		RSSL_DT_STATE,			0,					0,					0,				0,					0,				0,	0, 					0,					0,					0,	0,						0
# ENUM 			RSSL_DT_ENUM,			0,					0,					0,				0,					0,				0,	0, 					0,					0,					0,	0,						0
# (ARRAY) 		0,						0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0
# BUFFER 		RSSL_DT_BUFFER,			0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0
# ASCII 		RSSL_DT_ASCII_STRING,	0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0
# UTF8 			RSSL_DT_UTF8_STRING,	0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0
# RMTES 		RSSL_DT_RMTES_STRING,	0,					0,					0,				0,					0,				0,	0,					0,					0,					0,	0,						0

RWF_data_types = [
    {},
    {},
    {},
    {
        0: RSSLDataType.RSSL_DT_INT,
        1: RSSLDataType.RSSL_DT_INT_1,
        2: RSSLDataType.RSSL_DT_INT_2,
        4: RSSLDataType.RSSL_DT_INT_4,
        8: RSSLDataType.RSSL_DT_INT_8,
    },
    {
        0: RSSLDataType.RSSL_DT_UINT,
        1: RSSLDataType.RSSL_DT_UINT_1,
        2: RSSLDataType.RSSL_DT_UINT_2,
        4: RSSLDataType.RSSL_DT_UINT_4,
        8: RSSLDataType.RSSL_DT_UINT_8,
    },
    {0: RSSLDataType.RSSL_DT_FLOAT, 4: RSSLDataType.RSSL_DT_FLOAT_4},
    {0: RSSLDataType.RSSL_DT_DOUBLE, 8: RSSLDataType.RSSL_DT_DOUBLE_8},
    {},
    {0: RSSLDataType.RSSL_DT_REAL},
    {0: RSSLDataType.RSSL_DT_DATE, 4: RSSLDataType.RSSL_DT_DATE_4},
    {
        0: RSSLDataType.RSSL_DT_TIME,
        3: RSSLDataType.RSSL_DT_TIME_3,
        5: RSSLDataType.RSSL_DT_TIME_5,
        7: RSSLDataType.RSSL_DT_TIME_7,
        8: RSSLDataType.RSSL_DT_TIME_8,
    },
    {
        0: RSSLDataType.RSSL_DT_DATETIME,
        7: RSSLDataType.RSSL_DT_DATETIME_7,
        9: RSSLDataType.RSSL_DT_DATETIME_9,
        11: RSSLDataType.RSSL_DT_DATETIME_11,
        12: RSSLDataType.RSSL_DT_DATETIME_12,
    },
    {0: RSSLDataType.RSSL_DT_QOS},
    {0: RSSLDataType.RSSL_DT_STATE},
    {0: RSSLDataType.RSSL_DT_ENUM},
    {},
    {0: RSSLDataType.RSSL_DT_BUFFER},
    {0: RSSLDataType.RSSL_DT_ASCII_STRING},
    {0: RSSLDataType.RSSL_DT_UTF8_STRING},
    {0: RSSLDataType.RSSL_DT_RMTES_STRING},
]
