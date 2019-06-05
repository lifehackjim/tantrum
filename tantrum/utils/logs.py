# -*- coding: utf-8 -*-
"""tantrum logging module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import inspect
import logging
import logging.handlers
import time
import six
import sys

from . import exceptions
from . import tools
from .. import __package__ as PACKAGE_ROOT


LOG = logging.getLogger(PACKAGE_ROOT)
""":obj:`logging.Logger`: Package logger."""

LOG.setLevel(logging.DEBUG)

LOG_FILE = "{pkg}.log".format(pkg=PACKAGE_ROOT)
""":obj:`str`: Log filename for :func:`add_file` and :func:`remove_file`."""

LOG_CON_FMT = "%(levelname)-8s [%(name)s:%(funcName)s()] %(message)s"
""":obj:`str`: Logging format for :func:`add_stderr` and :func:`add_stdout`."""

LOG_PATH_FMT = (
    "[%(asctime)s] PID:%(process)s %(levelname)-8s [%(name)s:%(funcName)s()] "
    "%(message)s"
)
""":obj:`str`: Logging format for :func:`add_file`."""

LVL_DICT = logging._levelNames if six.PY2 else logging._nameToLevel
LVL_DICT = {k: v for k, v in LVL_DICT.items() if isinstance(k, six.string_types)}
""":obj:`dict`: Logging level names to ints, python version dependent."""

LVL_STR = ", ".join(list(LVL_DICT) + ["OFF"])
""":obj:`str`: CSV str of logging level names."""


def is_enabled(lvl="debug", obj=LOG):
    """Determine if a logger or handler is enabled for a log level.

    Args:
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to check if obj is enabled for.

            Defaults to: "debug".
        obj (:obj:`logging.Logger` or :obj:`logging.Handler`, optional):
            Object to check if enabled for lvl.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`bool`

    """
    return obj.isEnabledFor(level_int(lvl=lvl))


def is_disabled(obj=LOG):
    """Determine if a logger or handler is disabled.

    Args:
        obj (:obj:`logging.Logger` or :obj:`logging.Handler`, optional):
            Object to check if disabled.

            Defaults to: :data:`LOG`.

    Notes:
        Will traverse up the logger tree to see if any parents are disabled.

    Returns:
        :obj:`bool`

    """
    parent_disabled = is_disabled(obj=obj.parent) if obj.parent else False
    return any([obj.disabled, parent_disabled])


def use_gmt():
    """Set the logging system to use GMT for time strings."""
    logging.Formatter.converter = time.gmtime


def use_localtime():
    """Set the logging system to use local time for time strings."""
    logging.Formatter.converter = time.localtime


def set_level(lvl="info", obj=LOG):
    """Set a logger or handler to a log level.

    Args:
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to set obj to.

            Defaults to: "info".
        obj (:obj:`logging.Logger` or :obj:`logging.Handler`, optional):
            Object to set lvl on.

            Defaults to: :data:`LOG`.

    Notes:
        If lvl is "OFF" the disabled attr on obj will be set to True.

    Returns:
        :obj:`bool`

    """
    lvl = "info" if lvl is None else lvl
    if isinstance(lvl, six.string_types) and lvl.upper() == "OFF":
        obj.disabled = True
    else:
        obj.disabled = False
        obj.setLevel(level_int(lvl=lvl))


def get_obj_log(obj, lvl="debug"):
    """Get a logger object for an object.

    Args:
        obj (:obj:`object`):
            Object to get a logger for using the objects class module and name.
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to set logger created for obj to initially.

            Defaults to: "debug".

    Returns:
        :obj:`logging.Logger`

    """
    cls = obj if inspect.isclass(obj) else obj.__class__
    name = "{}.{}".format(cls.__module__, cls.__name__)
    return get_log(name=name, lvl=lvl)


def get_log(name, lvl="debug"):
    """Get a logger object.

    Args:
        name (:obj:`str`):
            Path of logger to get/create.
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to set logger created using name initially.

            Defaults to: "debug".

    Returns:
        :obj:`logging.Logger`

    """
    obj = logging.getLogger(name)
    set_level(lvl, obj)
    return obj


def level_name(lvl):
    """Get a logging level in str format.

    Args:
        lvl (:obj:`str` or :obj:`int`):
            Level to get str format of.

    Raises:
        :exc:`tantrum.utils.exceptions.ModuleError`:
            If int is not in values of :data:`LVL_DICT` or if str is not in keys of
            :data:`LVL_DICT`.

    Returns:
        :obj:`str`

    """
    if isinstance(lvl, six.string_types) and lvl.upper() in LVL_DICT:
        return lvl.upper()
    if isinstance(lvl, int) and lvl in LVL_DICT.values():
        return logging.getLevelName(lvl)
    error = "Invalid logging level {lvl!r}, must be one of {lvls}"
    error = error.format(lvl=lvl, lvls=list(LVL_DICT.values()))
    raise exceptions.ModuleError(error)


def level_int(lvl):
    """Get a logging level in int format.

    Args:
        lvl (:obj:`str` or :obj:`int`):
            Level to get int format of.

    Raises:
        :exc:`tantrum.utils.exceptions.ModuleError`:
            If int is not in values of :data:`LVL_DICT` or if str is not in keys of
            :data:`LVL_DICT`.

    Returns:
        :obj:`int`

    """
    if isinstance(lvl, int) and lvl in LVL_DICT.values():
        return lvl
    if isinstance(lvl, six.string_types) and lvl.upper() in LVL_DICT:
        return LVL_DICT[lvl.upper()]
    error = "Invalid logging level {lvl!r}, must be one of {lvls}"
    error = error.format(lvl=lvl, lvls=list(LVL_DICT.keys()))
    raise exceptions.ModuleError(error)


def log_str(obj):
    """Get a str format of a logger object showing level and attached handlers.

    Args:
        obj (:obj:`logging.Logger`):
            Logger object to get str format of.

    Returns:
        :obj:`str`

    """
    handlers = get_output_handlers(obj=obj)
    handlers = [handler_str(obj=h) for h in handlers]
    hstr = ("\n  " + "\n  ".join(handlers)) if handlers else "NO OUTPUT HANDLERS"
    lvl = level_name(lvl=obj.level)
    m = "Logger(name='{o}', level='{lvl}', disabled={d}, handlers: {h})"
    return m.format(o=obj.name, lvl=lvl, d=is_disabled(obj=obj), h=hstr)


def handler_str(obj):
    """Get a str format of a handler object showing level.

    Args:
        obj (:obj:`logging.Handler`):
            Handler object to get str format of.

    Returns:
        :obj:`str`

    """
    cls = obj.__class__.__name__
    lvl = level_name(lvl=obj.level)
    m = "{cls}(name='{name}', level='{lvl}')"
    return m.format(lvl=lvl, name=obj.name, cls=cls)


def add_stdout(lvl="info", fmt=LOG_CON_FMT, obj=LOG):
    """Add a STDOUT handler to a logger object.

    Args:
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to set on handler.

            Defaults to: "info".
        fmt (:obj:`str`, optional):
            Formatting string to use for logging.

            Defaults to: :data:`LOG_CON_FMT`.
        obj (:obj:`logging.Logger`, optional):
            Logger object to add handler to.

            Defaults to: :data:`LOG`.

    Notes:
        Will remove handler from obj if exists before adding.

    Returns:
        :obj:`logging.StreamHandler`

    """
    remove_stdout(obj=obj)
    name = "{name}_stdout".format(name=obj.name)
    log_fmt = logging.Formatter(fmt)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(log_fmt)
    set_level(lvl=lvl, obj=handler)
    handler.name = name
    obj.addHandler(handler)
    lvl = level_name(lvl=lvl)
    log = log_str(obj=obj)
    m = "Started logging to STDOUT at level {lvl!r} on {log}"
    m = m.format(lvl=lvl, log=log)
    LOG.debug(m)
    return handler


def add_stderr(lvl="info", fmt=LOG_CON_FMT, obj=LOG):
    """Add a STDERR handler to a logger object.

    Args:
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to set on handler.

            Defaults to: "info".
        fmt (:obj:`str`, optional):
            Formatting string to use for logging.

            Defaults to: :data:`LOG_CON_FMT`.
        obj (:obj:`logging.Logger`, optional):
            Logger object to add handler to.

            Defaults to: :data:`LOG`.

    Notes:
        Will remove handler from obj if exists before adding.

    Returns:
        :obj:`logging.StreamHandler`

    """
    remove_stderr(obj=obj)
    name = "{name}_stderr".format(name=obj.name)
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(logging.Formatter(fmt))
    set_level(lvl=lvl, obj=handler)
    handler.name = name
    obj.addHandler(handler)
    lvl = level_name(lvl=lvl)
    log = log_str(obj=obj)
    m = "Started logging to STDERR at level {lvl!r} on {log}"
    m = m.format(lvl=lvl, log=log)
    LOG.debug(m)
    return handler


def add_file(
    lvl="debug",
    path=None,
    path_sub="logs",
    path_file=LOG_FILE,
    max_mb=10,
    max_num=5,
    fmt=LOG_PATH_FMT,
    obj=LOG,
):
    """Add a rotating log file handler to a logger object.

    Args:
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to set on handler.

            Defaults to: "debug".
        path (:obj:`str` or :obj:`pathlib.Path`, optional):
            Storage directory to use.

            If empty, resolve path via :func:`tantrum.utils.tools.get_storage_dir`.

            Defaults to: None.
        path_sub (:obj:`str`, optional):
            Sub directory under path that should contain path_file.

            Defaults to: "logs"
        path_file (:obj:`str`, optional):
            Filename to write logs to under path / path_sub.

            Defaults to: :attr:`LOG_FILE`
        max_mb (:obj:`int`, optional):
            Rotate log file when it reaches this many MB.

            Defaults to: 10.
        max_num (:obj:`int`, optional):
            Only keep up to this number of rotated logs.

            Defaults to: 5.
        fmt (:obj:`str`, optional):
            Formatting string to use for logging.

            Defaults to: :data:`LOG_PATH_FMT`.
        obj (:obj:`logging.Logger`, optional):
            Logger object to add handler to.

            Defaults to: :data:`LOG`.

    Notes:
        Will remove handler from obj if exists before adding.

    Returns:
        :obj:`logging.handlers.RotatingFileHandler`

    """
    remove_file(path=path, path_sub=path_sub, path_file=path_file, obj=obj)

    path = tools.get_storage_dir(path=path, path_sub=path_sub, mkdir=True)
    path = path / path_file

    max_bytes = max_mb * 1024 * 1024
    handler = logging.handlers.RotatingFileHandler(
        filename=format(path), maxBytes=max_bytes, backupCount=max_num
    )
    handler.setFormatter(logging.Formatter(fmt))
    set_level(lvl=lvl, obj=handler)
    handler.name = format(path)
    obj.addHandler(handler)
    lvl = level_name(lvl=lvl)
    log = log_str(obj=obj)
    m = (
        "Started logging to file: '{path}' at level {lvl!r} "
        "rotating {cnt} logs every {mb} MB on {log}"
    )
    m = m.format(path=format(path), lvl=lvl, cnt=max_num, mb=max_mb, log=log)
    LOG.debug(m)
    return handler


def remove_stdout(obj=LOG):
    """Remove a STDOUT handler from a logger object.

    Args:
        obj (:obj:`logging.Logger`, optional):
            Logger object to remove handler from.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`logging.Handler`

    """
    handler = find_handler_by_name(name="{}_stdout".format(obj.name), obj=obj)
    if handler:
        log = log_str(obj=obj)
        m = "Stopped logging to STDOUT on {log}"
        m = m.format(log=log)
        LOG.debug(m)
        remove_handler(handler=handler, obj=obj)
    return handler


def remove_stderr(obj=LOG):
    """Remove a STDERR handler from a logger object.

    Args:
        obj (:obj:`logging.Logger`, optional):
            Logger object to remove handler from.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`logging.Handler`

    """
    handler = find_handler_by_name(name="{}_stderr".format(obj.name), obj=obj)
    if handler:
        log = log_str(obj=obj)
        m = "Stopped logging to STDERR on logger {log}"
        m = m.format(log=log)
        LOG.debug(m)
        remove_handler(handler=handler, obj=obj)
    return handler


def remove_file(path=None, path_sub="logs", path_file=LOG_FILE, obj=LOG):
    """Remove a STDERR handler from a logger object.

    Args:
        path (:obj:`str` or :obj:`pathlib.Path`, optional):
            Storage directory to use.

            If empty, resolve path via :func:`tantrum.utils.tools.get_storage_dir`.

            Defaults to: None.
        path_sub (:obj:`str`, optional):
            Sub directory under path that should contain path_file.

            Defaults to: "logs"
        path_file (:obj:`str`, optional):
            Filename to write logs to under path / path_sub.

            Defaults to: :attr:`LOG_FILE`
        obj (:obj:`logging.Logger`, optional):
            Logger object to remove handler from.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`logging.handlers.RotatingFileHandler`

    """
    path = tools.get_storage_dir(path=path, path_sub=path_sub, mkdir=False)
    path = path / path_file

    handler = find_handler_by_name(name=format(path), obj=obj)
    if handler:
        log = log_str(obj=obj)
        m = "Stopped logging to file: '{path}' on {log}"
        m = m.format(path=format(path), log=log)
        LOG.debug(m)
        try:
            handler.stream.close()
        except Exception:  # nosec # pragma: no cover
            pass
        try:
            handler.close()
        except Exception:  # nosec
            pass
        remove_handler(handler=handler, obj=obj)
    return handler


def add_null(obj=LOG):
    """Add a Null handler to a logger object.

    Args:
        obj (:obj:`logging.Logger`, optional):
            Logger object to add handler to.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`logging.NullHandler`

    """
    remove_null()
    handler = logging.NullHandler()
    handler.name = "null_handler"
    obj.addHandler(handler)
    return handler


def remove_null(obj=LOG):
    """Remove a Null handler from a logger object.

    Args:
        obj (:obj:`logging.Logger`, optional):
            Logger object to remove handler from.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`logging.NullHandler`

    """
    handler = find_handler_by_name(name="null_handler", obj=obj)
    remove_handler(obj=obj, handler=handler)
    return handler


def remove_handler(handler, obj=LOG):
    """Remove a handler from a logger.

    Args:
        handler (:obj:`logging.Handler`):
            Handler object to add to logger object.
        obj (:obj:`logging.Logger`, optional):
            Logger object to remove handler from.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`logging.Handler`

    """
    obj.removeHandler(handler)
    return handler


def find_handler_by_name(name, obj=LOG):
    """Find handler object that is attached to a logger.

    Args:
        name (:obj:`str`):
            Name of handler object to find.
        obj (:obj:`logging.Logger`, optional):
            Logger object to find handler in.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`logging.Handler` or None

    """
    matches = [x for x in obj.handlers if x.name == name]
    return matches[0] if matches else None


def get_output_handlers(lvl=None, obj=LOG):
    """Find handlers attached to a logger that show output at a given level.

    Args:
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to check if handler outputs at.

            Defaults to: None.
        obj (:obj:`logging.Logger`, optional):
            Logger object to find output handlers in.

            Defaults to: :data:`LOG`.

    Notes:
        If lvl is None logging levels of handlers will not be checked and
        the return will be handlers that are not :obj:`logging.NullHandler`.

    Returns:
        :obj:`list` of :obj:`logging.Handler`

    """
    ret = [h for h in obj.handlers if not isinstance(h, logging.NullHandler)]
    if obj.parent:
        ret += get_output_handlers(obj=obj.parent, lvl=lvl)
    if lvl:
        ret = [x for x in ret if x.level and x.level <= level_int(lvl=lvl)]
    return ret


def will_print_at(lvl="debug", obj=LOG):
    """Check if a logger will show output at a given level.

    Args:
        lvl (:obj:`str` or :obj:`int`, optional):
            Level to check if obj has any handlers that will output logs at.

            Defaults to: "debug".
        obj (:obj:`logging.Logger`, optional):
            Logger to check if disabled and for handlers that output at lvl.

            Defaults to: :data:`LOG`.

    Returns:
        :obj:`bool`

    """
    has_handler = get_output_handlers(obj=obj, lvl=lvl)
    enabled = is_enabled(lvl=lvl, obj=obj)
    disabled = is_disabled(obj=obj)
    if not has_handler or disabled or not enabled:
        return False
    return True


add_null()
# Add a null handler by default to silence logging system warnings
use_gmt()
# Use GMT by default for logging system
