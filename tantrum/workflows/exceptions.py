# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`tantrum.workflows`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.PackageError):
    """Parent of all exceptions for :mod:`tantrum.workflows`."""

    pass


class ModuleWarning(exceptions.PackageWarning):
    """Parent of all warnings for :mod:`tantrum.workflows`."""

    pass
