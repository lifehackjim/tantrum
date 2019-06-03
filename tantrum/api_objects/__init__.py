# -*- coding: utf-8 -*-
"""Python objects for Tanium's API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import importlib
import six
import warnings

from . import exceptions
from .. import api_models
from .. import utils

if six.PY2:
    import pathlib2 as pathlib  # pragma: no cover
else:
    import pathlib

API_TYPES = ["soap"]
""":obj:`list` of :obj:`str`: All API object module types supported."""

PATTERN = "{api_type}_*.py"
""":obj:`str`: Glob pattern to find modules in :func:`get_versions`."""

DEFAULT_TYPE = "soap"
""":obj:`str`: Default :data:`API_TYPES` type to load in :func:`load`."""


class ApiObjects(object):
    """Encapsulation object for an API Object module."""

    def __init__(self, module_file, adhoc_warn=True):
        """Constructor.

        Args:
            module_file (:obj:`str`):
                API Object module file name in import string format.
            adhoc_warn (:obj:`bool`, optional):
                Enable warnings about adhoc added simple attributes to API Objects.

                Defaults to: True.

        """
        module_path = "{p}.{f}".format(p=__name__, f=module_file)
        self._module = importlib.import_module(module_path)
        """:mod:`tantrum.api_objects`: Imported API Objects module."""

        self._models = api_models
        """:mod:`tantrum.api_models`: API Models module."""

        for cls in self.cls_all:
            cls.API_OBJECTS = self
            setattr(self, cls.__name__, cls)

        self.control_adhoc_warnings(adhoc_warn)

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "type={!r}".format(self.module_type),
            "version={!r}".format(self.module_version),
        ]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    def control_adhoc_warnings(self, enable=False):
        """Enable or disable warnings about adhoc added simple attributes.

        Args:
            enable (:obj:`bool`, optional):
                Enable warnings.

                Defaults to: True.

        """
        action = "default" if enable else "ignore"
        warnings.simplefilter(action, api_models.exceptions.AttrUndefinedWarning)

    @property
    def ApiModel(self):
        """Get the ApiModel.

        Returns:
            :class:`tantrum.api_models.ApiModel`

        """
        return self.module.ApiModel

    @property
    def ApiItem(self):
        """Get the ApiItem.

        Returns:
            :class:`tantrum.api_models.ApiItem`

        """
        return self.module.ApiItem

    @property
    def ApiList(self):
        """Get the ApiList.

        Returns:
            :class:`tantrum.api_models.ApiList`

        """
        return self.module.ApiList

    @property
    def module(self):
        """Get the API objects module.

        Returns:
            :obj:`object`

        """
        return self._module

    @property
    def module_type(self):
        """Get the API type.

        Returns:
            :obj:`str`

        """
        return self.module.TYPE

    @property
    def module_version(self):
        """Get the API version.

        Returns:
            :obj:`str`

        """
        return self.module.__version__

    @property
    def module_dt(self):
        """Get the date time format string.

        Returns:
            :obj:`str`

        """
        return self.module.API_DT

    def module_dt_format(self, dt):
        """Format a datetime string using :attr:`module_dt`.

        Args:
            dt (:obj:`str`):
                String to format.

        Returns:
            :obj:`datetime.datetime`

        """
        return datetime.datetime.strptime(dt, self.module_dt)

    @property
    def module_version_dict(self):
        """Get the API version.

        Returns:
            :obj:`dict`

        """
        return self.module.VERSION

    @property
    def cls_item(self):
        """Get all of the ApiItem classes.

        Returns:
            :obj:`list` of :class:`tantrum.api_models.ApiItem`

        """
        return self.ApiItem.__subclasses__()

    @property
    def cls_list(self):
        """Get all of the ApiItem classes.

        Returns:
            :obj:`list` of :class:`tantrum.api_models.ApiList`

        """
        return self.ApiList.__subclasses__()

    @property
    def cls_all(self):
        """Get all of the ApiItem and ApiList classes.

        Returns:
            :obj:`list` of :class:`tantrum.api_models.ApiModel`

        """
        return self.cls_list + self.cls_item

    @property
    def cls_name_map_item(self):
        """Get a map of API key name to class for all ApiItem classes.

        Returns:
            :obj:`dict`

        """
        name_map = {}
        for c in self.cls_item:
            if c.API_NAME in name_map:
                other = name_map[c.API_NAME]
                error = "{cls} with API name {name!r} already mapped as {other}"
                error = error.format(cls=c, name=c.API_NAME, other=other)
                raise exceptions.ModuleError(error)
            name_map[c.API_NAME] = c
        return name_map

    @property
    def cls_name_map_list(self):
        """Get a map of API key name to class for all ApiList classes.

        Returns:
            :obj:`dict`

        """
        name_map = {}
        for c in self.cls_list:
            if c.API_NAME in name_map:
                other = name_map[c.API_NAME]
                error = "{cls} with API name {name!r} already mapped as {other}"
                error = error.format(cls=c, name=c.API_NAME, other=other)
                raise exceptions.ModuleError(error)
            name_map[c.API_NAME] = c
        return name_map

    @property
    def cls_name_map_all(self):
        """Get a map of API key name to class for all ApiItem and ApiList classes.

        Returns:
            :obj:`dict`

        """
        name_map = {}
        for c in self.cls_all:
            if c.API_NAME in name_map:
                other = name_map[c.API_NAME]
                error = "{cls} with API name {name!r} already mapped as {other}"
                error = error.format(cls=c, name=c.API_NAME, other=other)
                raise exceptions.ModuleError(error)
            name_map[c.API_NAME] = c
        return name_map

    def cls_item_by_name(self, name):
        """Get an ApiItem class by API name.

        Args:
            name (:obj:`str`):
                Name of object used in API calls.

        Returns:
            :class:`tantrum.api_models.ApiItem`

        """
        name_map = self.cls_name_map_item
        if name not in name_map:
            raise exceptions.UnknownApiNameError(
                name=name, name_map=name_map, module=self.module
            )
        return name_map[name]

    def cls_list_by_name(self, name):
        """Get an ApiList class by API name.

        Args:
            name (:obj:`str`):
                Name of object used in API calls.

        Returns:
            :class:`tantrum.api_models.ApiList`

        """
        name_map = self.cls_name_map_list
        if name not in name_map:
            raise exceptions.UnknownApiNameError(
                name=name, name_map=name_map, module=self.module
            )
        return name_map[name]

    def cls_by_name(self, name):
        """Get an ApiItem or ApiList by API name.

        Args:
            name (:obj:`str`):
                Name of object used in API calls.

        Returns:
            :class:`tantrum.api_models.ApiModel`

        """
        name_map = self.cls_name_map_all
        if name not in name_map:
            raise exceptions.UnknownApiNameError(
                name=name, name_map=name_map, module=self.module
            )
        return name_map[name]

    @classmethod
    def load(cls, api_type=DEFAULT_TYPE, veq="", vmax="", vmin="", vshrink=True):
        """Import an API module for version and type.

        Args:
            api_type (:obj:`str`, optional):
                Type of object module to load, must be one of :data:`API_TYPES`.

                Defaults to: :data:`DEFAULT_TYPE`.
            veq (:obj:`str`, optional):
                Exact version that API object module file must match.

                Defaults to: "".
            vmin (:obj:`str`, optional):
                Minimum version that API object module file must match.

                Defaults to: "".
            vmax (:obj:`str`, optional):
                Maximum version that API object module file must match.

                Defaults to: "".
            vshrink (:obj:`bool` or :obj:`int`, optional):
                If True, shrink API object module file version down to match the
                same length as veq, vmax, and vmin.

                If False, do not shrink API object module file version at all.

                If int, shrink API object module file version, veq, vmax, and vmin
                down to this length.

                Defaults to: True.

        Raises:
            :exc:`exceptions.ModuleError`:
                If api_type not in :data:`API_TYPES`.

        Returns:
            :obj:`ApiObjects`

        """
        return load(api_type=api_type, veq=veq, vmax=vmax, vmin=vmin, vshrink=vshrink)


def get_versions(api_type=DEFAULT_TYPE):
    """Search for API object module files of api_type.

    Args:
        api_type (:obj:`str`, optional):
            Type of object module to load, must be one of :data:`API_TYPES`.

            Defaults to: :data:`DEFAULT_TYPE`.

    Raises:
        :exc:`exceptions.NoVersionFoundError`:
              If no API module files matching :data:`PATTERN` are found.

    Returns:
        :obj:`list` of :obj:`dict`

    """
    path = pathlib.Path(__file__).absolute().parent
    pattern = PATTERN.format(api_type=api_type)
    matches = [p for p in path.glob(pattern)]

    if not matches:
        error = "Unable to find any object modules matching pattern {r!r} in {p!r}"
        error = error.format(p=format(path), r=pattern)
        raise exceptions.NoVersionFoundError(error)

    versions = []
    for match in matches:
        name = match.stem
        vparts = name.split("_")
        vtype = vparts.pop(0)
        vparts = utils.versions.split_ver(vparts)
        vstr = utils.versions.join_ver(vparts)
        versions.append(
            {
                "ver_str": vstr,
                "ver_parts": vparts,
                "api_type": vtype,
                "module_file": name,
                "module_path": match,
            }
        )

    versions = sorted(versions, key=lambda x: x["ver_parts"], reverse=True)
    return versions


def find_version(api_type=DEFAULT_TYPE, veq="", vmax="", vmin="", vshrink=True):
    """Find a API module files that match version and type.

    Args:
        api_type (:obj:`str`, optional):
            Type of object module to find, must be one of :data:`API_TYPES`.

            Defaults to: :data:`DEFAULT_TYPE`.
        veq (:obj:`str`, optional):
            Exact version that API object module file must match.

            Defaults to: "".
        vmin (:obj:`str`, optional):
            Minimum version that API object module file must match.

            Defaults to: "".
        vmax (:obj:`str`, optional):
            Maximum version that API object module file must match.

            Defaults to: "".
        vshrink (:obj:`bool`, optional):
            If True, shrink API object module file version down to match the
            same length as veq, vmax, and vmin.

            If False, do not shrink API object module file version at all.

            If int, shrink API object module file version, veq, vmax, and vmin
            down to this length.

            Defaults to: True.

    Raises:
        :exc:`exceptions.NoVersionFoundError`:
              If no API module files match api_type, veq, vmax, and vmin.

    Returns:
        :obj:`dict`

    """
    versions = get_versions(api_type=api_type)
    for version in versions:
        if utils.versions.version_check(
            version=version["ver_parts"], veq=veq, vmax=vmax, vmin=vmin, vshrink=vshrink
        ):
            return version

    error = [
        "",
        "Unable to find any {t!r} object modules where version is:",
        "  Equal to: {veq!r}",
        "  At least: {vmin!r}",
        "  At Most: {vmax!r}",
        "  File pattern matches: {p!r}",
        "",
        "Valid versions for type {t!r}:{vers}",
    ]
    vers = [v["ver_str"] for v in versions]
    error = "\n".join(error).format(
        t=api_type,
        p=PATTERN.format(api_type=api_type),
        veq=veq or "any",
        vmin=vmin or "any",
        vmax=vmax or "any",
        vers="\n  - " + "\n  - ".join(vers),
    )
    raise exceptions.NoVersionFoundError(error)


def load(api_type=DEFAULT_TYPE, veq="", vmax="", vmin="", vshrink=True):
    """Import an API module for version and type.

    Args:
        api_type (:obj:`str`, optional):
            Type of object module to load, must be one of :data:`API_TYPES`.

            Defaults to: :data:`DEFAULT_TYPE`.
        veq (:obj:`str`, optional):
            Exact version of object module of type to load.

            Defaults to: "".
        vmin (:obj:`str`, optional):
            Minimum version of object module of type to load.

            Defaults to: "".
        vmax (:obj:`str`, optional):
            Maximum version of object module of type to load.

            Defaults to: "".
        vshrink (:obj:`bool` or :obj:`int`, optional):
            If True, shrink API object module file version down to match the
            same length as veq, vmax, and vmin.

            If False, do not shrink API object module file version at all.

            If int, shrink API object module file version, veq, vmax, and vmin
            down to this length.

            Defaults to: True.

    Raises:
        :exc:`exceptions.ModuleError`:
             If api_type not in :data:`API_TYPES`.

    Returns:
        :obj:`ApiObjects`

    """
    api_type = api_type.lower()
    if api_type not in API_TYPES:
        error = "type {t!r} must be one of {a}"
        error = error.format(t=api_type, a=API_TYPES)
        raise exceptions.ModuleError(error)

    version = find_version(
        api_type=api_type, veq=veq, vmin=vmin, vmax=vmax, vshrink=vshrink
    )
    ret = ApiObjects(module_file=version["module_file"])
    return ret
