# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`tantrum.utils`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.PackageError):
    """Parent of all exceptions for :mod:`tantrum.utils`."""

    pass


class ModuleWarning(exceptions.PackageWarning):
    """Parent of all warnings for :mod:`tantrum.utils`."""

    pass


class VersionMismatchError(ModuleError):
    """Exception handler when matching a version."""

    pass
