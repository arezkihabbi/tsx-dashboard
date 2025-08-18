import string
from functools import lru_cache
from typing import Set, Tuple

from jinja2 import Environment, nodes

from .._tools import cached_property


class OldStyleStringTemplate(string.Template):
    """string.Template with extended validation capabilities

    This template must be used directly or as a base for templates in refinitiv.data
    JSON configuration file.
    Default delimiter is '#'. Variable syntax: '#var' or '#{var}'.
    """

    delimiter = "#"
    braceidpattern = r"(?a:[_a-z][_.|a-z0-9]*)"

    def names(self) -> Set[str]:
        """Get names of substitution variables in pattern"""
        return {
            match_tuple[1] or match_tuple[2]  # named or braced
            for match_tuple in self.pattern.findall(self.template)
            if match_tuple[1] or match_tuple[2]
        }


class StringTemplate:
    """Jinja-based string template"""

    def __init__(self, source):
        self.env = Environment(
            block_start_string="{{",
            block_end_string="}}",
            variable_start_string="#{",
            variable_end_string="}",
        )

        self.env.filters["in"] = lambda inp: ", ".join(map(repr, inp))
        self.source = source

    @property
    def template(self):
        return self.source

    @staticmethod
    @lru_cache(128)
    def get_vars_from_node(node: nodes.Node) -> Set[str]:
        vars_set = set()
        iter_list = [(node,)]
        while iter_list:
            _node, *_attrs = iter_list.pop(0)
            if isinstance(_node, nodes.Getattr):
                _attrs = (_node.attr, *_attrs)
            elif isinstance(_node, nodes.Name):
                vars_set.add(".".join(map(str, (_node.name, *_attrs))))
            iter_list.extend((i, *_attrs) for i in _node.iter_child_nodes())
        return vars_set

    def placeholders(self):
        return self.get_vars_from_node(self._parsed)

    @cached_property
    def _parsed(self):
        return self.env.parse(self.source)

    def validate(self):
        self._parsed

    def substitute(self, **kwargs):
        return self.env.from_string(self.source).render(**kwargs)


class InvalidPlaceholderError(ValueError):
    """Exception to display syntax errors in string templates"""

    def __init__(
        self,
        index: int,
        template_text: str,
        limit: int = 80,
        padding: int = 0,
        prefix: str = "",
    ):
        """
        Parameters
        ----------
        index : int
            index of wrong placeholder start, get it from regex match
        template_text
            original text template
        limit : int
            maximum length of error message
        padding : int
            padding around place where invalid placeholder starts in error message text
        prefix : int
            prefix before error message, for additional information
        """
        self.limit = limit
        self.padding = padding
        self.index = index
        self.template_text = template_text
        self.prefix = prefix

    def __str__(self):
        line_index, col_index = index_to_line_and_col(self.index, self.template_text)
        target_line = self.template_text.splitlines()[line_index]
        target_line, shift = shorten_string_to_include_position(target_line, self.limit, col_index, self.padding)
        return "\n".join(
            [
                f"{self.prefix}Invalid placeholder in the template string: "
                f"line {line_index + 1}, col {col_index + 1}:",
                target_line,
                "-" * (col_index - shift) + "^",
            ]
        )


def index_to_line_and_col(index: int, target_string: str) -> Tuple[int, int]:
    """Convert position index in multiline string to line and column

    Parameters
    ----------
    index : int
        index of symbol in target string
    target_string : str
        target string

    Returns
    -------
    Tuple of line index and column index of given symbol, starting from zero
    """
    lines = target_string[:index].splitlines(keepends=True)

    if not lines:
        return 0, 0

    col_index = index - len("".join(lines[:-1]))
    line_index = len(lines) - 1
    return line_index, col_index


def shorten_string_to_include_position(line: str, limit: int, pos: int, padding: int = 0) -> Tuple[str, int]:
    """Shorten string to given limit to include given position

    Can be used when we need to display position in a string when screen width is
    limited.

    Parameters
    ----------
    line : str
        target string
    limit : int
        maximum length of resulting string
    pos : int
        position in string that must be included in shortened string, starting from 0
    padding
        number of symbols left and right of pos that also must be included

    Returns
    -------
    Tuple of shortened string and number of symbols removed from the start
    """
    cur_right = pos + padding
    if padding >= len(line):
        raise ValueError("padding must be less than the length of line")
    if len(line) <= limit:
        return line, 0
    if cur_right < limit:
        return line[:limit], 0
    left = max(cur_right - limit + 1, 0)
    return line[left : cur_right + 1], left
