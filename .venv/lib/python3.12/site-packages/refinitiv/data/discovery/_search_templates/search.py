"""Templates functionality, specific for discovery search"""

import pandas as pd
from humps import pascalize

from refinitiv.data._tools import inspect_parameters_without_self
from refinitiv.data.content import search
from .base import Target, TargetTemplate


class DefinitionGetDataTarget(Target):
    """Template Target class that can be used with any definition to create templates"""

    definition = None

    def __init__(self):
        super().__init__()
        self.args_names = set(inspect_parameters_without_self(self.definition))

    def __call__(self, **kwargs):
        return self.definition(**kwargs).get_data().data.df


class DiscoverySearchTarget(DefinitionGetDataTarget):
    """Template Target class specific for discovery search"""

    definition = search.Definition


class DiscoverySearchTemplate(TargetTemplate):
    """Discovery search preset class"""

    _target_class = DiscoverySearchTarget

    def __repr__(self):
        return f"<DiscoverySearchTemplate '{self.name}'>"

    # redefining search only to add return type annotation
    def search(self, **kwargs) -> pd.DataFrame:
        """Please, use help() on a template object itself to get method documentation"""
        # ^ we need this docstring because we can't easily generate docstring for
        # the method, but can change __doc__ for the class instance
        return super().search(**kwargs)

    def _export(self) -> dict:
        """Get dictionary that can be used in config to duplicate this template

        Or use it as a base for another search template.
        Exported without documentation.

        Experimental, does not work with all subfeatures and may never be
        """
        request_body = pascalize(self._pass_through_defaults)
        request_body.update({pascalize(k): v.template for k, v in self._templated_defaults.items()})

        if "View" in request_body and isinstance(request_body["View"], search.Views):
            request_body["View"] = request_body["View"].value

        result = {"request_body": request_body}

        if self._placeholders_defaults:
            result["parameters"] = {name: {"default": value} for name, value in self._placeholders_defaults.items()}

        return result
