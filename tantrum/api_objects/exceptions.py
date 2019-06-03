# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`tantrum.api_objects`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.TantrumError):
    """Parent of all exceptions for :mod:`tantrum.api_objects`."""

    pass


class ModuleWarning(exceptions.TantrumWarning):
    """Parent of all warnings for :mod:`tantrum.api_objects`."""

    pass


class NoVersionFoundError(ModuleError):
    """Exception handler when finding a version of an API object module."""

    pass


class UnknownApiNameError(ModuleError):
    """Exception handler when unable to find an API name for an API object."""

    def __init__(self, name, name_map, module):
        """Constructor.

        Args:
            name (:obj:`str`):
                API name being searched for.
            name_map (:obj:`dict`):
                Map of all API names to API objects.
            module (:obj:`object`):
                Source API module of name_map.

        """
        self.name = name
        """:obj:`str`: API name being searched for."""
        self.name_map = name_map
        """:obj:`dict`: Map of all API names to API objects."""
        self.module = module
        """:obj:`object`: Source API module of name_map."""

        error = [
            "API names of all API objects:{valid_names}",
            "API module: {module}",
            "Unable to find a matching API class for API name {name!r}",
        ]
        error = "\n".join(error)
        self.error = error.format(
            name=name,
            module=module,
            valid_names="\n  - " + "\n  - ".join(sorted(list(name_map.keys()))),
        )
        """:obj:`str`: Error message that was thrown."""
        super(UnknownApiNameError, self).__init__(self.error)
