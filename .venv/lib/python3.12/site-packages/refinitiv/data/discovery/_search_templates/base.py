"""Define basic abstract classes for templates functionality

That is abstracted from the original goal - discovery search templates.
And can be used for any other Definition or any other callable.
"""
import logging
from functools import lru_cache
from threading import Lock
from typing import Optional, Dict, Any, Set, Iterable

from pandas import DataFrame

from ..._tools import StringTemplate

from .namespaces import Namespace


class SearchInterrupt(Exception):
    pass


class Target:
    """Abstract callable target with accessible list of keyword arguments names

    Base for building templates in TargetTemplate.
    You need to define your own targets that do some work. Like DiscoverySearchTarget.
    """

    def __init__(self):
        self.args_names: Set[str] = set()

    def __call__(self, **kwargs):
        # for override
        pass


def extract_used_templates_from_placeholders_and_namespace(
    names: Set[str], namespace: Namespace
) -> Dict[str, Set[str]]:
    """Get a full path to namespaces that was used in the set of template placeholders

    In the string template we can have placeholders like
    "builtins.utils.geo.Mines.location.lat". And it's impossible to decide just by
    looking on it what part of this string is namespaces chain (prefix), what is
    Template name, and what is chain of attributes of the Template call result (suffix).
    The goal of these functions is to find maximum namespaces + Template name chain
    based on given namespace.

    For example, if in namespace we have template with the namespace chain
    "builtins.utils.geo" and name "Mines", we will return "builtins.utils.geo.Mines".
    And what left of original string must be processed as a result attributes later.

    You must be sure that you are passing as a names arguments all names
    that MUST BE treated as a sub-template usage. In other case, exception will be raised.

    Parameters
    ----------

    names: Set[str]
        set of placeholder names, without suffixes like jinja filters, but with
        attributes of the expected sub-template output
    namespace: Namespace
        namespace object of your template

    Returns
    -------
    Set[str]
        Templates used, full paths, without attributes

    Raises
    ------
    ValueError
        If it's impossible to find template for one of your placeholders
    """

    # pretending we can't have template on the root on namespace here
    ns_prefixes = namespace.keys()

    def match_name(orig_name):
        """Check if orig_name or its prefix is presented in the namespace

        Function expects that orig_name already  starts with one of the root namespace
        prefixes. So it always matches at least to this prefix.
        """
        cur_name = orig_name
        attr_list = []
        while True:
            try:
                found = namespace.get(cur_name)
            except KeyError:
                raise ValueError(f"Unknown sub-template usage: {orig_name}")

            if found:
                break
            else:
                # cut the tail
                cur_name, suffix = cur_name.rsplit(".", maxsplit=1)
                attr_list.append(suffix)

        return cur_name, ".".join(reversed(attr_list))

    result = {}

    for name in names:
        prefix = name.split(".", maxsplit=1)[0]

        if prefix in ns_prefixes:
            matched, rest = match_name(name)
            if matched and matched not in ns_prefixes:
                if matched not in result:
                    result[matched] = set()
                result[matched].add(rest)

    return result


class TargetTemplate:
    """Abstract target search preset

    Initialized with default values for defined Target
    Any string value acts as template string. You can use placeholder variables,
    and those variables will be required to prepare search parameters through
    `._search_kwargs()` or to launch search through `.search()`.

    Placeholder variables syntax based on jinja2 with some changes:
    - Variables defined with #{varname} syntax
    - Instructions with {{}} symbols. Available instructions:
      - {{if}}<one value>{{else}}<other value>{{endif}}

    Attributes
    ----------

    name: str
        name of the template

    """

    _target_class = Target
    _cache_lock = Lock()

    def __init__(
        self,
        name=None,
        *,
        placeholders_defaults: Optional[Dict[str, Any]] = None,
        pass_through_defaults: Optional[Dict[str, Any]] = None,
        optional_placeholders: Iterable[str] = None,
        ns: "Namespace" = None,
        **search_defaults,
    ):
        """
        Parameters
        ----------
        name : str, optional
            name of the template
        placeholders_defaults: dict, optional
            Dict of string template placeholders default values.
        pass_through_defaults: dict, optional
            default values for the Target parameters
        optional_placeholders: Iterable[str], optional
            names of placeholders that are optional without default values
        ns: Namespace
            Namespace in which template will operate. Used for sub-templates.
        """

        self._ns = ns if ns is not None else Namespace()
        self._target: Target = self._target_class()
        # Names of the templates used, with full path from self.ns root
        self._subtemplates_used = {}

        """ List search keyword arguments we can use in this template """
        self._placeholders_defaults = {} if placeholders_defaults is None else placeholders_defaults
        self._optional_placeholders = set([] if optional_placeholders is None else optional_placeholders)
        """ Default template variables values for a templated defaults """
        if pass_through_defaults is None:
            pass_through_defaults = {}

        bad_pass_through_params = set(pass_through_defaults) - self._target.args_names
        if bad_pass_through_params:
            raise ValueError(
                "All the parameters described in 'parameters' section of search "
                "template configuration, must be either placeholders variables or "
                "parameters of the discovery search Definition. These parameters are "
                "neither of them: " + ", ".join(bad_pass_through_params)
            )

        self.name = name

        unknown_defaults = set(search_defaults) - self._target.args_names
        if unknown_defaults:
            raise ValueError(
                "These arguments are defined in template, but not in search Definition: " + ", ".join(unknown_defaults)
            )
        # Names of all placeholders inside string templates
        """Set of names for all placeholders in string templates"""
        self._placeholder_names: Set[str] = set()
        # Arguments to be passed to Definition as templates
        self._templated_defaults: Dict[str, StringTemplate] = {}
        # Arguments to be directly passed to Definition without any preprocessing
        self._pass_through_defaults: Dict[str, Any] = {}

        def is_subtemplate(placeholder_name: str):
            return any(placeholder_name.startswith(prefix) for prefix in self._ns.keys())

        for name, value in search_defaults.items():
            if not isinstance(value, str):
                self._pass_through_defaults[name] = value
                continue

            template = StringTemplate(value)
            template.validate()
            if template.placeholders():
                self._templated_defaults[name] = template
                for name in template.placeholders():
                    if not is_subtemplate(name):
                        if "." in name:
                            logging.info(
                                f"Placeholder {name} for template {self.name} contains "
                                f"dots, but has an invalid prefix."
                            )
                        self._placeholder_names.add(name)
            else:
                self._pass_through_defaults[name] = value

            self._subtemplates_used.update(
                extract_used_templates_from_placeholders_and_namespace(template.placeholders(), self._ns)
            )

        self._pass_through_defaults.update(pass_through_defaults)

        bad_tpl_var_names = self._get_full_placeholder_names() & self._target.args_names
        if bad_tpl_var_names:
            raise ValueError(
                "You can't use template arguments with the same name"
                " as search arguments. You have used: " + ", ".join(bad_tpl_var_names)
            )

    def _get_full_placeholder_names(self):
        placeholder_names = self._placeholder_names.copy()
        for st_path in self._subtemplates_used.keys():
            placeholder_names.update(self._ns.get(st_path)._get_full_placeholder_names())
        return placeholder_names

    def __repr__(self):
        return f"<TargetTemplate for {self._target_class.__name__} name='{self.name}'>"

    def _search_kwargs(self, **kwargs) -> dict:
        """Get dictionary of arguments for the Target"""

        undefined_placeholders = (
            self._get_full_placeholder_names()
            - set(kwargs)
            - set(self._placeholders_defaults)
            - self._optional_placeholders
        )

        assert all("." not in ph for ph in undefined_placeholders)

        if undefined_placeholders:
            raise KeyError(
                "Following keyword arguments must be defined, but they are not: " + ", ".join(undefined_placeholders)
            )

        unexpected_arguments = (
            set(kwargs)
            - self._get_full_placeholder_names()
            # templated defaults can't be redefined
            - (self._target.args_names - self._templated_defaults.keys())
        )

        if unexpected_arguments:
            raise KeyError(
                f"Unexpected arguments: {', '.join(unexpected_arguments)}."
                f"Possible arguments for template '{self.name}': "
                f"{', '.join(self._target.args_names)}"
            )

        old_kwargs = kwargs
        kwargs = kwargs.copy()
        # Applying template variables defaults
        for name, value in self._placeholders_defaults.items():
            if name not in kwargs:
                kwargs[name] = value

        def set_path_value(path, value):
            """Set value to kwargs dict of dicts by path with dots

            Expecting to always have at least one dot in path, because subtemplate
            always has a prefix.
            """
            parts = path.split(".")
            assert len(parts) > 1
            current = kwargs
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value

        def check_result(value, required_attributes):
            for attr in required_attributes:
                if attr not in value:
                    raise ValueError(f"{attr} is not in the result of search.")
            return value

        for subname, required_items in self._subtemplates_used.items():
            st = self._ns.get(subname)
            filtered_kwargs = {k: v for k, v in old_kwargs.items() if k in st._get_full_placeholder_names()}
            try:
                set_path_value(subname, check_result(st._search(**filtered_kwargs), required_items))
            except ValueError as e:
                raise SearchInterrupt(
                    f"Result of {st} search with parameters {filtered_kwargs} did not contain all required values"
                ) from e

        result = self._pass_through_defaults.copy()

        # Apply variables to templated defaults
        for name, template in self._templated_defaults.items():
            result[name] = template.substitute(**kwargs)

        # Apply other variables from kwargs
        for name, value in kwargs.items():
            if name not in self._get_full_placeholder_names() and name not in self._ns.keys():
                result[name] = value

        return result

    @lru_cache(None)
    def _search(self, **kwargs) -> Any:
        """Target call with given parameters"""
        try:
            return self._target(**self._search_kwargs(**kwargs))
        except SearchInterrupt:
            return DataFrame()

    def search(self, **kwargs) -> Any:
        """Public uncached call to search"""
        with self._cache_lock:
            result = self._search(**kwargs)
            self._search.cache_clear()
        return result
