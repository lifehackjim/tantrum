# -*- coding: utf-8 -*-
"""Parent exceptions and warnings for the tantrum package."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class PackageError(Exception):
    """Parent exception for all :mod:`tantrum` errors."""

    pass


class PackageWarning(Warning):
    """Parent warning for all :mod:`tantrum` warnings."""

    pass
