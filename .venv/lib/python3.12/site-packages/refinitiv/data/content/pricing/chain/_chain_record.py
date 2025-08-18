import collections
from typing import List, Union, Dict, Tuple

from ...._types import OptInt, OptStr

REF_COUNT_FIELD_NAME = "REF_COUNT"
RECORD_TYPE_FIELD_NAME = "RECORDTYPE"
RDN_DISPLAY_FIELD_NAME = "RDNDISPLAY"
PREF_DISPLAY_FIELD_NAME = "PREF_DISP"
PREV_DISPLAY_FIELD_NAME = "PREV_DISP"
PREF_LINK_FIELD_NAME = "PREF_LINK"
DISPLAY_NAME_FIELD_NAME = "DSPLY_NAME"
INVALID_DISPLAY_TEMPLATE_VALUES = ["@@@", 0]

NCharsConfig = collections.namedtuple(
    "NCharsConfig",
    [
        "name",
        "link_field_name_template",
        "start_no_link_field_name",
        "end_no_link_field_name",
        "prev_field_name",
        "next_field_name",
    ],
)

config_10_chars = NCharsConfig(
    name="10_chars",
    link_field_name_template="LINK_{:d}",
    start_no_link_field_name=1,
    end_no_link_field_name=14,
    prev_field_name="PREV_LR",
    next_field_name="NEXT_LR",
)

config_17_chars = NCharsConfig(
    name="17_chars",
    link_field_name_template="LONGLINK{:d}",
    start_no_link_field_name=1,
    end_no_link_field_name=14,
    prev_field_name="LONGPREVLR",
    next_field_name="LONGNEXTLR",
)

config_32_chars = NCharsConfig(
    name="32_chars",
    link_field_name_template="BR_LINK{:d}",
    start_no_link_field_name=1,
    end_no_link_field_name=14,
    prev_field_name="BR_PREVLR",
    next_field_name="BR_NEXTLR",
)


class InvalidChainRecordException(Exception):
    pass


class ChainRecord(object):
    def __init__(self, config: NCharsConfig, fields: dict) -> None:
        self._config: NCharsConfig = config
        self._fields = fields
        self.num_constituents: OptInt = None
        self.link_field_by_index: Dict[int, str] = {}
        self.prev_chain_record_name: OptStr = None
        self.next_chain_record_name: OptStr = None
        self.record_type: OptInt = None
        self.rdn_display: OptInt = None
        self.pref_display: OptInt = None
        self.prev_display: OptInt = None
        self.pref_link: OptStr = None
        self.display_name: OptStr = None

    def __repr__(self) -> str:
        return (
            f"ChainRecord("
            f"num_constituents={self.num_constituents}, "
            f"link_field_by_index={self.link_field_by_index}, "
            f"prev_chain_record_name={self.prev_chain_record_name}, "
            f"next_chain_record_name={self.next_chain_record_name}, "
            f"record_type={self.record_type}, "
            f"rdn_display={self.rdn_display}, "
            f"pref_display={self.pref_display}, "
            f"prev_display={self.prev_display}, "
            f"pref_link={self.pref_link}, "
            f"display_name={self.display_name})"
        )

    @property
    def constituents(self) -> List[str]:
        return [constituent for _, constituent in sorted(self.link_field_by_index.items())]

    @property
    def display_template(self) -> int:
        if is_valid_disp_tmpl(self.pref_display):
            return self.pref_display
        elif is_valid_disp_tmpl(self.prev_display):
            return self.prev_display
        else:
            return self.rdn_display

    def update(self, fields) -> Dict[int, Tuple[str, str]]:
        get = fields.get

        old_num_constituents = None
        new_num_constituents = None

        if REF_COUNT_FIELD_NAME in fields:
            old_num_constituents = self.num_constituents
            self.num_constituents = get(REF_COUNT_FIELD_NAME)
            new_num_constituents = self.num_constituents

        self.record_type = get(RECORD_TYPE_FIELD_NAME, self.record_type)
        self.rdn_display = get(RDN_DISPLAY_FIELD_NAME, self.rdn_display)
        self.pref_display = get(PREF_DISPLAY_FIELD_NAME, self.pref_display)
        self.prev_display = get(PREV_DISPLAY_FIELD_NAME, self.prev_display)
        self.pref_link = get(PREF_LINK_FIELD_NAME, self.pref_link)
        self.display_name = get(DISPLAY_NAME_FIELD_NAME, self.display_name)

        if old_num_constituents and new_num_constituents:
            num_constituents = new_num_constituents
            if old_num_constituents > new_num_constituents:
                num_constituents = old_num_constituents

        else:
            num_constituents = self.num_constituents

        cfg = self._config

        index_to_old_and_new_constituent: Dict[int, Tuple[str, str]] = {}
        start = cfg.start_no_link_field_name
        stop = num_constituents + 1
        for i in range(start, stop):
            link_field_name = cfg.link_field_name_template.format(i)

            if link_field_name in fields:
                old_constituent = self.link_field_by_index.get(i, None)
                self.link_field_by_index[i] = get(link_field_name)
                new_constituent = self.link_field_by_index[i]
                i = i - cfg.start_no_link_field_name
                index_to_old_and_new_constituent[i] = (old_constituent, new_constituent)

        self.prev_chain_record_name = get(cfg.prev_field_name, self.prev_chain_record_name)
        self.next_chain_record_name = get(cfg.next_field_name, self.next_chain_record_name)

        return index_to_old_and_new_constituent


def _can_create(fields: dict, config: NCharsConfig) -> bool:
    if REF_COUNT_FIELD_NAME not in fields:
        return False

    start = config.start_no_link_field_name
    stop = config.end_no_link_field_name + 1
    for i in range(start, stop):
        if config.link_field_name_template.format(i) not in fields:
            return False

    prev_not_in_fields = config.prev_field_name not in fields
    next_not_in_fields = config.next_field_name not in fields
    if prev_not_in_fields and next_not_in_fields:
        return False

    return True


def can_create_chain_record(fields: dict) -> bool:
    if _can_create(fields, config_17_chars):
        is_valid = True
    elif _can_create(fields, config_10_chars):
        is_valid = True
    elif _can_create(fields, config_32_chars):
        is_valid = True
    else:
        is_valid = False

    return is_valid


def _create_chain_record(fields: dict, config: NCharsConfig) -> ChainRecord:
    chain_record: ChainRecord = ChainRecord(config, fields)
    get = fields.get
    chain_record.record_type = get(RECORD_TYPE_FIELD_NAME)
    chain_record.rdn_display = get(RDN_DISPLAY_FIELD_NAME)
    chain_record.pref_display = get(PREF_DISPLAY_FIELD_NAME)
    chain_record.prev_display = get(PREV_DISPLAY_FIELD_NAME)
    chain_record.pref_link = get(PREF_LINK_FIELD_NAME)
    chain_record.display_name = get(DISPLAY_NAME_FIELD_NAME)

    try:
        chain_record.num_constituents = fields[REF_COUNT_FIELD_NAME] or 0
        if chain_record.num_constituents:
            start = config.start_no_link_field_name
            stop = chain_record.num_constituents + 1
            for i in range(start, stop):
                link_field_name = config.link_field_name_template.format(i)
                chain_record.link_field_by_index[i] = fields[link_field_name]

    except KeyError:
        raise InvalidChainRecordException(f"ERROR!!! Invalid chain record template of {config}")

    chain_record.prev_chain_record_name = get(config.prev_field_name)
    chain_record.next_chain_record_name = get(config.next_field_name)
    return chain_record


def create_chain_record(fields: dict) -> ChainRecord:
    if _can_create(fields, config_17_chars):
        chain_record = _create_chain_record(fields, config_17_chars)
    elif _can_create(fields, config_10_chars):
        chain_record = _create_chain_record(fields, config_10_chars)
    elif _can_create(fields, config_32_chars):
        chain_record = _create_chain_record(fields, config_32_chars)
    else:
        raise ValueError(f"Cannot create chain record from fields={fields}")

    return chain_record


def is_valid_disp_tmpl(disp_tmpl: Union[str, int]) -> bool:
    if isinstance(disp_tmpl, int):
        is_valid = disp_tmpl not in INVALID_DISPLAY_TEMPLATE_VALUES

    elif isinstance(disp_tmpl, str):
        is_valid = disp_tmpl not in INVALID_DISPLAY_TEMPLATE_VALUES
        is_valid = is_valid and disp_tmpl.strip() != ""

    else:
        is_valid = bool(disp_tmpl)

    return is_valid
