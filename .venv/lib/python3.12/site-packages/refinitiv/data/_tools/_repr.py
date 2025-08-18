from typing import Any


def create_repr(
    obj: object,
    middle_path: str = "",
    class_name: str = "Definition",
    content: Any = None,
) -> str:
    module_path = obj.__module__
    new_path = get_new_path(module_path, middle_path, class_name)
    obj_id = hex(id(obj))
    s = f"<{new_path} object at {obj_id}>"

    if content:
        s = s.replace(">", f" {content}>")

    return s


def get_new_path(module_path: str, middle: str = "", class_name: str = "") -> str:
    """
    Examples
    --------
    >>> module_path = "refinitiv.data.pricing.stream"
    >>> class_name = "Definition"
    >>> start = "refinitiv.data"
    >>> middle = "stream"
    >>> new_path = ".".join([start, middle, class_name])
    >>> new_path
    ... "refinitiv.data.stream.Definition"

    >>> middle = "content"
    >>> new_path
    ... "refinitiv.data.content.Definition"
    """
    start, *_ = module_path.split("._", maxsplit=1)

    if middle:
        new_path = ".".join([start, middle, class_name])
    else:
        new_path = ".".join([start, class_name])
    return new_path
