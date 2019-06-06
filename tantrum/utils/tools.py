# -*- coding: utf-8 -*-
"""tantrum tools module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
from datetime import datetime, timedelta
import os
import six

from .. import __package__ as PACKAGE_ROOT

if six.PY2:
    import pathlib2 as pathlib  # pragma: no cover
else:
    import pathlib

STORAGE_DIR = "{pkg}_local".format(pkg=PACKAGE_ROOT)
""":obj:`str`: Default sub-directory to use for :attr:`STORAGE_PATH`."""

STORAGE_PATH = format(pathlib.Path("~") / STORAGE_DIR)
""":obj:`str`: Default path to use for :func:`get_storage_dir` if path is None.

Will use OS Environment variable "TANTRUM_STORAGE_PATH" if set.
"""


def get_env(key, default):
    """Get an environment variables value.

    Args:
        key (:obj:`str`):
            Name of OS environment variable value to get.
        default (:obj:`str`):
            Default value to return if key is not set or is empty.

    Returns:
        :obj:`str`

    """
    return os.environ.get(key, default) or default


def get_storage_dir(path=None, path_sub="", mkdir=False):
    """Get the directory for tantrum to use for storing local state.

    Args:
        path (:obj:`str` or :obj:`pathlib.Path`, optional):
            Path to use as base storage directory.

            If None, will use OS environment variable "TANTRUM_STORAGE_PATH" if set.

            If None and "TANTRUM_STORAGE_PATH" is not set,
            will use :data:`STORAGE_PATH`.

            Defaults to: None.
        path_sub (:obj:`str` or :obj:`pathlib.Path`, optional):
            Subdirectory to get under path.

            Defaults to: "".
        mkdir (:obj:`bool`, optional):
            Create path and path / sub with perms 0700.

            Defaults to: False.

    Returns:
        :obj:`pathlib.Path`

    """
    path = path or get_env(key="TANTRUM_STORAGE_DIR", default=STORAGE_PATH)
    path = pathlib.Path(path).expanduser().absolute() / path_sub
    if mkdir:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
    return path


def str_to_intfloat(s):
    """Convert str to int or float.

    Args:
        s (:obj:`str`):
            String to convert to float if it has a period or int if not.

    Returns:
        :obj:`int` or :obj:`float`

    """
    if isinstance(s, six.string_types):
        if "." in s and s.replace(".", "").isdigit():
            return float(s)
        if s.isdigit():
            return int(s)
    return s


def secs_ago(secs):
    """Get a datetime object from N seconds ago.

    Args:
        secs (:obj:`int` or :obj:`float`):
            Number of seconds ago to get datetime object of.

    Returns:
        :obj:`datetime.datetime`

    """
    # secs = 0 if secs is None else secs
    # now = datetime.utcnow()
    # delta = datetime.timedelta(seconds=secs)
    now = datetime.utcnow()
    secs = str_to_intfloat(secs)
    return now if secs is None else now - timedelta(seconds=secs)


def secs_age(dt):
    """Get the number of seconds ago of a datetime object.

    Args:
        dt (:obj:`datetime.datetime`):
            Datetime object to calculate age in seconds of.

    Returns:
        :obj:`int`

    """
    # delta = 0 if dt is None else datetime.utcnow() - dt
    return 0 if not dt else (datetime.utcnow() - dt).seconds


def b64_encode(s):
    """Encode s as base64 using :func:`base64.b64encode`.

    Args:
        s (:obj:`str`):
            Text to base64 encode.

    Returns:
        :obj:`str`

    """
    s = format("" if s is None else s) if not isinstance(s, six.string_types) else s
    s = six.ensure_binary(s)
    s = base64.b64encode(s)
    return six.ensure_str(s)


def b64_decode(s):
    """Decode text as base64 using :func:`base64.b64decode`.

    Args:
        s (:obj:`str`):
            Text to base64 decode.

    Returns:
        :obj:`str`

    """
    s = six.ensure_binary(s)
    s = base64.b64decode(s)
    return six.ensure_str(s)


def trim_txt(txt, limit=10000):
    """Trim a str if it is over n characters.

    Args:
        txt (:obj:`str`):
            String to trim.
        limit (:obj:`int`, optional):
            Number of characters to trim txt to.

            Defaults to: 10000.

    Returns:
        :obj:`str`

    """
    trim_line = "\n... trimmed over {limit} characters".format(limit=limit)
    txt = txt[:limit] + trim_line if len(txt) > limit else txt
    return txt


def get_dict_path(obj, path):
    """Traverse a dict using a / seperated string.

    Args:
        obj (:obj:`dict`):
            Dictionary to traverse using path.
        path (:obj:`str`):
            Nested dictionary keys seperated by / to traverse in obj.

    Raises:
        :exc:`ValueError`:
            If a part of a path can not be found.

    Returns:
        :obj:`object`

    """
    value = obj
    parts = path.strip("/").split("/")
    for idx, key in enumerate(parts):
        try:
            value = value[key]
        except Exception:
            current_parts = parts[:idx]
            current_path = "/".join(current_parts)
            if isinstance(value, dict):
                valid_keys = list(value.keys())
            else:
                value_type = type(value).__name__
                valid_keys = "NONE: key {k!r} is {t}, not dict."
                valid_keys = valid_keys.format(k=current_parts[-1], t=value_type)
            error = [
                "Unable to find key {k!r} in path {p!r}",
                "Valid keys at {c!r}:",
                "{v!r}",
            ]
            error = "\n  ".join(error)
            error = error.format(k=key, p=path, c=current_path, v=valid_keys)
            raise ValueError(error)
    return value


class Timer(object):
    """Context manager to get a human readable elapsed timespan."""

    def __init__(self):
        """Constructor."""
        self.start = datetime.utcnow()
        """:obj:`datetime.datetime`: Start of timespan."""
        self.end = None
        """:obj:`datetime.datetime`: End of timespan."""

    def __call__(self):
        """Return the current time.

        Returns:
            :obj:`datetime.datetime`

        """
        return datetime.utcnow()

    def __enter__(self):
        """Set the start time.

        Returns:
            :obj:`datetime.datetime`

        """
        self.start = datetime.utcnow()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Set :attr:`end` to now."""
        self.end = self()

    def __str__(self):
        """Get elapsed details.

        Returns:
            :obj:`str`

        """
        m = "delta: {t.elapsed_delta}, int: {t.elapsed_int}, str: {t.elapsed}"
        return m.format(t=self)

    def __repr__(self):
        """Get elapsed details.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    @property
    def elapsed_delta(self):
        """Get elapsed time since :attr:`start`.

        Returns:
            :obj:`datetime.timedelta`

        """
        return (self.end or datetime.utcnow()) - self.start

    @property
    def elapsed_int(self):
        """Get elapsed seconds since :attr:`start`.

        Returns:
            :obj:`int`

        """
        return self.elapsed_delta.seconds

    @property
    def elapsed(self, ms=True, short=True):
        """Get elapsed seconds since :attr:`start` in human readable format.

        ms (:obj:`bool`, optional):
            Represent milliseconds separately instead of as fractional seconds.

            Defaults to: True.
        short (:obj:`bool`, optional):
            Return shortened version of minutes, seconds, millseconds.

            Defaults to: True.

        Returns:
            :obj:`str`

        """
        return self.elapsed_delta


def calc_percent(part, whole):
    """Utility method for getting percentage of part out of whole

    Args:
        part (:obj:`int` or :obj:`float`)
        whole (:obj:`int` or :obj:`float`)

    Returns:
        :obj:`float`

    """
    if 0 in [part, whole]:
        return float(0)
    return 100 * (float(part) / float(whole))


def calc_percent_of(percent, whole):
    """Utility method for getting percentage of whole

    Args:
        percent (:obj:`int` or :obj:`float`)
        whole (:obj:`int` or :obj:`float`)

    Returns:
        :obj:`float`

    """
    return (percent * whole) / 100.0


def def_none(v, d):
    """Use a default value of ``d`` if ``v`` is None."""
    return d if v is None else v
