import datetime
import json
import logging
import os

from ....delivery.cfs._tools import remove_one_ext
from .... import _log as log
from ...._tools import cached_property


def parse_log_file(logpath: str) -> dict:
    details_by_log_action = {}
    try:
        with open(logpath) as f:
            for line in f:
                log_line = json.loads(line)
                log_action = log_line.get("action")

                if log_action == "CLEANUP":
                    details_by_log_action["UPDATE"] = []
                    continue

                if not log_action:
                    continue

                log_details = log_line.get("details")
                details = details_by_log_action.setdefault(log_action, [])

                if log_action == "CREATE TABLE":
                    detail_item = log_details.get("table-name")
                else:
                    detail_item = log_details.get("filename")

                details.append(detail_item)

    except Exception:
        pass

    return details_by_log_action


def get_file_logger(id_, logpath_):
    file_logger = log.root_logger().getChild(f"{id_}.file")
    handler = logging.FileHandler(logpath_, "a")
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    file_logger.addHandler(handler)
    file_logger.setLevel(logging.DEBUG)
    file_logger.propagate = False
    return file_logger


class Actions:
    def __init__(self, id_, logpath):
        self.id = id_
        self.logpath = logpath
        self._details_by_action = None

    @property
    def details_by_action(self):
        if self._details_by_action is None:
            self._details_by_action = parse_log_file(self.logpath)
        return self._details_by_action

    @cached_property
    def _file_logger(self):
        return get_file_logger(self.id, self.logpath)

    def _log(self, action_name, details):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        s = json.dumps({"date": date, "action": action_name, "details": details})
        self._file_logger.info(s)

    def add(self, action_name, **details):
        self._log(action_name, details)
        return details

    def downloaded(self, **details):
        self._log("DOWNLOAD", details)
        return details

    def extracted(self, **details):
        self._log("EXTRACT", details)
        return details

    def table_created(self, **details):
        self._log("CREATE TABLE", details)
        return details

    def updated(self, **details):
        self._log("UPDATE", details)
        return details

    def cleaned_up_db(self, **details):
        self._log("CLEANUP", details)
        return details

    def _get(self, action_name):
        return set(self.details_by_action.get(action_name, []))

    def get_downloaded(self):
        return self._get("DOWNLOAD")

    def get_extracted(self):
        return self._get("EXTRACT")

    def get_created_tables(self):
        return self._get("CREATE TABLE")

    def get_not_updated_and_extracted(self):
        downloaded = set(remove_one_ext(filename) for filename in self.get_downloaded())
        updated = self._get("UPDATE")
        not_updated = downloaded - updated
        return not_updated, self._get("EXTRACT")

    def cleanup(self):
        try:
            os.remove(self.logpath)
        except PermissionError:
            log.root_logger().warning(f"Cannot remove {self.logpath}, file will be cleared.")
            with open(self.logpath, "w") as f:
                f.write("")
            log.root_logger().warning(f"{self.logpath} cleared.")
        except FileNotFoundError:
            # do nothing
            pass

    def dispose(self):
        log.dispose_logger(self._file_logger)
        self.cleanup()

    def update(self):
        self._details_by_action = None
