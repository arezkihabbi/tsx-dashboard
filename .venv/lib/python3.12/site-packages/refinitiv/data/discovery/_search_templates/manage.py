"""Functionality specific to special SearchTemplates template access class

Takes care of public API parts and loading user templates from the config
"""
from typing import Union, List, TYPE_CHECKING

from humps import depascalize

from ..._configure import get_config
from .embedded import (
    RICCategoryTemplate,
    UnderlyingRICToOptionTemplate,
    UnderlyingRICToFutureTemplate,
    RICToIssuerTemplate,
    OrganisationPermIDToUPTemplate,
    FutureRICToFutureTemplate,
)
from .search import DiscoverySearchTemplate
from .namespaces import Namespace
from .utils import generate_docstring

if TYPE_CHECKING:
    from .base import TargetTemplate


def depascalize_view(value: str) -> str:
    """Convert search View value to upper snakecase

    We need to have separate function for that because some enum View values
    does not follow the rules of pascal case
    """
    if "STIRs" in value:
        value = value.replace("STIRs", "Stirs")

    return depascalize(value).upper()


def template_from_config_data(name: str, data: dict, config_prefix: str):
    namespace = Namespace(
        builtin=BuiltinNamespace(),
        user=UserNamespace(config_prefix=config_prefix),
        _=Namespace(
            **{  # TODO: locals can use global namespaces too
                name: template_from_config_data(name, sub, config_prefix)
                for name, sub in data.get("locals", {}).items()
            }
        ),
    )
    template = DiscoverySearchTemplate(
        name,
        placeholders_defaults={
            name: attrs["default"] for name, attrs in data.get("parameters", {}).items() if "default" in attrs
        },
        optional_placeholders={
            name for name, attrs in data.get("parameters", {}).items() if attrs.get("optional", False)
        },
        ns=namespace,
        **depascalize(data.get("request_body", {})),
    )

    method_args = {}
    # Some placeholders may be only in string, but not in "parameters"
    for param in sorted(template._placeholder_names):
        method_args[param] = data.get("parameters", {}).get(param, {})

    # That's why we can get them all in one cycle with pass-through parameters
    # that is located in "parameters" config session, but not in template string
    for param, desc in data.get("parameters", {}).items():
        if param not in template._placeholder_names:
            method_args[param] = desc

    template.__doc__ = generate_docstring(
        description=data.get("description", ""),
        methods={"search": {"description": "", "args": method_args}},
    )

    return template


class BuiltinNamespace(Namespace):
    def __setitem__(self, key: str, value: Union["Namespace", "TargetTemplate"]):
        raise NotImplementedError("Setting namespace key-value not supported for built-in namespace")

    def __getitem__(self, name: str):
        attr = getattr(SearchTemplates, name)
        if not isinstance(attr, DiscoverySearchTemplate):
            raise AttributeError(f"Embedded search template named {name} is not found")
        return attr


class UserNamespace(Namespace):
    _blacklisted_keys = {"request_body"}

    def __init__(self, config_prefix):
        super().__init__()

        self._CONFIG_PREFIX = config_prefix

    def __iter__(self):
        return get_config().get(self._CONFIG_PREFIX, {}).keys().__iter__()

    def __setitem__(self, key: str, value: Union["Namespace", "TargetTemplate"]):
        raise NotImplementedError("Setting namespace key-value not supported for user namespace")

    def __getitem__(self, name: str) -> Union[DiscoverySearchTemplate, "UserNamespace"]:
        if name in self._blacklisted_keys:
            raise KeyError(f"'{name}' is a reserved key")
        config = get_config()
        key = f"{self._CONFIG_PREFIX}.{name}"
        if key not in config:
            raise KeyError(f"Template or Namespace '{name}' is not found in the config")

        data = config[key] or {}
        if "request_body" not in data:
            return UserNamespace(key)

        data = config[key].as_attrdict()
        return template_from_config_data(name, data, self._CONFIG_PREFIX)

    def keys(self) -> List[str]:
        """Get list of available search template names"""
        return list(self)


class SearchTemplates(UserNamespace):
    """Easy access to search templates from the library config

    Check if search template with the name "Equity" is defined in the config:
    >>> templates = SearchTemplates()
    >>> "Equity" in templates
    True
    Get "Equity" search template:
    >>> templates["Equity"]
    Get list of available search template names:
    >>> templates.keys()
    ["Equity"]
    """

    RICCategory = RICCategoryTemplate()
    UnderlyingRICToOption = UnderlyingRICToOptionTemplate()
    UnderlyingRICToFuture = UnderlyingRICToFutureTemplate()
    RICToIssuer = RICToIssuerTemplate()
    FutureRICToFuture = FutureRICToFutureTemplate()
    OrganisationPermIDToUP = OrganisationPermIDToUPTemplate()

    def __init__(self):
        super().__init__(config_prefix="search.templates")

    def __setitem__(self, key: str, value: Union["Namespace", "TargetTemplate"]):
        raise NotImplementedError("Setting namespace key-value not supported for global namespace")
