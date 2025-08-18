import re

from ...._tools import Converter

datetime_converter = Converter()
regexp_filename_obj = re.compile(r".*([Dd]elta|[Ii]nit).*(\d{4}-\d{2}-\d{2}).*(\.jsonl.gz|\.jsonl)$")
regexp_init_archives = re.compile(r".*(-[Ii]nit-).*\d{4}-\d{2}-\d{2}.*(.gz)$")
regexp_delta_files = re.compile(r".*(Jsonl-[Dd]elta-).*\d{4}-\d{2}-\d{2}.*")
regexp_init_file = re.compile(r".*(Jsonl-[Ii]nit-).*\d{4}-\d{2}-\d{2}.*")
regexp_jsonl_fileset = re.compile(r".*(-Jsonl-).*\d{4}-\d{2}-\d{2}.*")
regexp_filename_date = re.compile(r".*(\d{4}-\d{2}-\d{2}).*")


def is_correct_filename(filename):
    return regexp_filename_obj.match(filename) is not None


def is_init_file(filename):
    return regexp_init_file.match(filename) is not None


def get_date_from_filename(filename):
    result = re.search(r"\d{4}-\d{2}-\d{2}", filename)
    return result.group(0)


def get_datetime_from_filename(filename):
    date = get_date_from_filename(filename)
    result = datetime_converter.convert(date)
    return result


def get_the_newest_file(filenames):
    sorted_filenames = sorted(filenames, key=lambda a: get_datetime_from_filename(a))
    if not sorted_filenames:
        return None
    result = sorted_filenames[-1]
    return result


def get_init_archives(filenames):
    # return init archives with correct name
    return filter(lambda a: regexp_init_archives.match(a), filenames)


def get_filesets_with_delta_files(file_sets):
    # return init archives with correct name
    result = [file_set for file_set in file_sets if regexp_delta_files.match(file_set["name"])]
    return result


def get_filesets_with_the_newest_init_file_and_delta_files(file_sets):
    file_sets = [file_set for file_set in file_sets if regexp_jsonl_fileset.match(file_set["name"])]
    init_filesets = filter(lambda a: "init" in a["name"].lower(), file_sets)
    init_dates = [get_date_from_filename(i["name"]) for i in init_filesets]
    init_dates.sort()
    if not init_dates:
        return []
    init_date = datetime_converter.convert(init_dates[-1])
    result = filter(
        lambda a: init_date <= datetime_converter.convert(get_date_from_filename(a["name"])),
        file_sets,
    )
    return result


def sorted_files(files):
    if not files:
        return []

    result = sorted(files)
    last_item = result[-1]

    if "init" in last_item or "Init" in last_item:
        result.insert(0, result.pop(-1))

    return result


def join_path_to_field(*args):
    if len(args) == 1:
        return args[0]

    return ".".join(filter(lambda a: bool(a), args))
