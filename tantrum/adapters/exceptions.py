# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`tantrum.adapters`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import exceptions


class ModuleError(exceptions.TantrumError):
    """Parent of all exceptions for :mod:`tantrum.adapters`.

    Thrown by:
      * :func:`tantrum.adapters.load_type`
      * :func:`tantrum.adapters.load`

    """

    pass


class ModuleWarning(exceptions.TantrumWarning):
    """Parent of all warnings for :mod:`tantrum.adapters`.

    Thrown by:

    """

    pass


class InvalidTypeError(ModuleError):
    """Thrown when an object of an invalid type is supplied.

    Thrown by:
      * :func:`tantrum.adapters.Adapter.api_get_audit_logs`
      * :func:`tantrum.adapters.check_object_type`

    """

    pass


class EmptyAttributeError(ModuleError):
    """Thrown when an object is supplied that does not have required attributes set.

    Thrown by:
      * :func:`tantrum.adapters.check_object_attrs`

    """

    pass


class TypeMismatchError(ModuleError):
    """Thrown when an API module type does not match an adapters type.

    Thrown by:
      * :func:`tantrum.adapters.check_adapter_types`

    """

    pass


class SessionNotFoundWarning(ModuleWarning):
    """Thrown when a session XML tag can not be found in a response body.

    Thrown by:
      * :func:`tantrum.adapters.Soap.send`

    """

    pass
