import json
import os
import os.path

from ._actions import Actions
from ._errors import PackageNotFoundException
from ._tools import (
    get_date_from_filename,
    get_the_newest_file,
    get_init_archives,
    get_filesets_with_delta_files,
    get_filesets_with_the_newest_init_file_and_delta_files,
    sorted_files,
)
from ...._core.log_reporter import _LogReporter
from ...._core.session import get_valid_session
from ....delivery.cfs._tools import path_join, remove_one_ext
from ...._tools import get_correct_filename
from ....delivery.cfs._unpacker import _Unpacker
from ....delivery import cfs


class FileManager(_LogReporter):
    def __init__(
        self,
        logger,
        actions: Actions,
        package_name,
        bucket,
        path,
        session=None,
        auto_retry=0,
        auto_extract=False,
    ):
        super().__init__(logger=logger)
        self._package_name = package_name
        self._bucket = bucket
        self._path = path
        self._auto_extract = auto_extract
        self._auto_retry_count = auto_retry
        self._actions = actions
        self._unpacker = _Unpacker(logger)
        self.session = session

    def update_files(self):
        _packages_def = cfs.packages.Definition(
            package_name=self._package_name,
            bucket_name=self._bucket,
        )
        _packages = _packages_def.get_data(session=self.session)
        session = get_valid_session(self.session)
        self.init_logger(session.logger())

        if not _packages.data.packages:
            message = f"package (name={self._package_name}, bucket={self._bucket}) not found"
            self._actions.add(
                "PACKAGE NOT FOUND",
                bucket=self._bucket,
                package=self._package_name,
            )
            self._info(f"package bucket='{self._bucket}', package_name='{self._package_name}' not found")
            raise PackageNotFoundException(message)

        _package_id = _packages.data.packages[0].package_id

        self._actions.update()
        downloaded = self._actions.get_downloaded()

        init_files = get_init_archives(downloaded) if downloaded else None
        init_file = get_the_newest_file(init_files) if init_files else None

        init_file_date = get_date_from_filename(init_file) if init_file else None

        # if init_file_date is None, the modified_since parameter will be skipped
        _file_sets_def = cfs.file_sets.Definition(
            bucket=self._bucket,
            package_id=_package_id,
            modified_since=init_file_date,
        )
        _file_sets = _file_sets_def.get_data(session=self.session)
        _file_sets = [file_set for file_set in _file_sets.data.file_sets]

        if not init_file:
            # if no init files are loaded,
            # get the latest init and delta files with the same or newer date
            _file_sets = get_filesets_with_the_newest_init_file_and_delta_files(_file_sets)

        else:
            # if init file already downloaded, get deltas with same or newer date
            _file_sets = get_filesets_with_delta_files(_file_sets)

        # download files
        has_files_for_download = False
        for file_set in _file_sets:
            for file in file_set:
                filename_ext = get_correct_filename(file.filename)
                if filename_ext not in downloaded:
                    has_files_for_download = True
                    self.__retry_download_file(file.id, filename_ext)
        if not has_files_for_download:
            self._info("no new files for download")

    def __retry_download_file(self, file_id: str, filename_ext: str):
        count_of_try = self._auto_retry_count + 1

        while count_of_try:
            try:
                self._info(f"download file {filename_ext} to {self._path}")
                fd = cfs.file_downloader.Definition({"id": file_id, "filename": filename_ext}).retrieve(
                    session=self.session
                )
                fd.download(self._path)
                self._actions.downloaded(path=self._path, filename=filename_ext)

                if self._auto_extract:
                    fd.extract(self._path)
                    extracted_filename = remove_one_ext(filename_ext)
                    self._actions.extracted(path=self._path, filename=extracted_filename)
                    self._info(f"extract file {filename_ext} to {self._path}")

                break
            except Exception as e:
                details = self._actions.add(
                    "DOWNLOAD CRASHED",
                    path=self._path,
                    filename=filename_ext,
                    error=str(e),
                )
                self._info(f"download crashed {details}")
                count_of_try -= 1

    def extract_file(self, filename):
        self._unpacker.unpack(filename, self._path)
        self._actions.extracted(filename=filename, path=self._path)
        self._info(f"extract file '{filename}' to '{self._path}'")

    def read_file(self, filename):
        data = []
        filepath = path_join(self._path, filename)
        if not os.path.exists(filepath):
            message = f"cannot update database, because previously downloaded file is missing: {filepath}"
            self._actions.add("ERROR", message=message)
            self._error(f"error: {message}")
            raise FileNotFoundError(message)
        with open(filepath) as f:
            for line_n, line in enumerate(f):
                try:
                    data.append(json.loads(line))
                except Exception as e:
                    error_details = self._actions.add("ERROR", message=str(e), line_number=line_n, filename=filename)
                    self._info(f"error: {error_details}")
                    continue

        return data

    def read_files_for_update(self) -> list:
        self._actions.update()
        files_to_update, extracted = self._actions.get_not_updated_and_extracted()

        if not files_to_update:
            return []

        data = []
        files_to_update = sorted_files(files_to_update)
        for filename in files_to_update:
            if filename not in extracted:
                self.extract_file(filename)

            file_attrs = {"DateTime": get_date_from_filename(filename)}
            data.append((filename, self.read_file(filename), file_attrs))

        return data

    def cleanup_files(self):
        # example: filenames = {"log.txt"}
        filenames = set()
        self._actions.update()
        filenames.update(self._actions.get_downloaded())
        filenames.update(self._actions.get_extracted())

        handlers = self._actions._file_logger.handlers
        for handler in handlers:
            handler.close()

        if filenames:
            filenames.update({"log.txt"})

        for filename in filenames:
            path = path_join(self._path, filename)

            try:
                os.remove(path)
            except PermissionError:
                if filename == "log.txt":
                    with open(path, "w"):
                        # only create a new file
                        pass
                    self._info(f"WARNING: Cannot remove {path}. The log has been cleared.")
                self._info(f"WARNING: Cannot remove {path}")
