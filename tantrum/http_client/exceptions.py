# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`tantrum.http_client`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.TantrumError):
    """Parent of all exceptions for :mod:`tantrum.http_client`."""

    pass


class ModuleWarning(exceptions.TantrumWarning):
    """Parent of all warnings for :mod:`tantrum.http_client`."""

    pass
