# -*- coding: utf-8 -*-
"""tantrum versioning utilities module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

from . import exceptions


def version_recomp(v1, v2, vshrink=True):
    """Recompile version strings into lists.

    Args:
        v1 (:obj:`str` or :obj:`list`):
            Version that is being compared against v2.

            Will be shrunk down to the same dotted length as v2 if vshrink is True.

            Will be split into list using period.
        v2 (:obj:`str` or :obj:`list`):
            Version that v1 is being compared against.

            Will be split into list using period.
        vshrink (:obj:`bool` or :obj:`int`, optional):
            If True, shrink v1 down to match the same length as v2.

            If False, do not shrink v1 at all.

            If int, shrink both v1 and v2 down to this length.

            Defaults to: True.

    Notes:
        If any non-integers found in v1 or v2, they will be returned as joined
        strings using periods.

        Default python string comparison leads to a less-than-perfect comparison
        for ints mixed with strs.

    Returns:
        (:obj:`list` of :obj:`str`, :obj:`list` of :obj:`str`) or
        (:obj:`str`, :obj:`str`)

    """
    v1, v2 = split_ver(v1), split_ver(v2)
    v2_len = len(v2)
    if isinstance(vshrink, bool):
        if vshrink:
            v1 = v1[:v2_len]
    elif isinstance(vshrink, int):
        v1 = v1[:vshrink]
        v2 = v2[:vshrink]
    if any(not isinstance(x, int) for x in v1 + v2):
        v1, v2 = join_ver(v1), join_ver(v2)
    return v1, v2


def version_eq(v1, v2, vshrink=True):
    """Check if v1 is equal to v2.

    Args:
        v1 (:obj:`str` or :obj:`list`):
            Version that is being compared against v2.

            Will be shrunk down to the same dotted length as v2 if vshrink is True.
        v2 (:obj:`str` or :obj:`list`):
            Version that v1 is being compared against.
        vshrink (:obj:`bool` or :obj:`int`, optional):
            If True, shrink v1 down to match the same length as v2.

            If False, do not shrink v1 at all.

            If int, shrink both v1 and v2 down to this length.

            Defaults to: True.

    Returns:
        :obj:`bool`

    """
    v1, v2 = version_recomp(v1=v1, v2=v2, vshrink=vshrink)
    return v1 == v2


def version_min(v1, v2, vshrink=True):
    """Check if v1 is greater than or equal to v2.

    Args:
        v1 (:obj:`str` or :obj:`list`):
            Version that is being compared against v2.

            Will be shrunk down to the same dotted length as v2 if vshrink is True.
        v2 (:obj:`str` or :obj:`list`):
            Version that v1 is being compared against.
        vshrink (:obj:`bool` or :obj:`int`, optional):
            If True, shrink v1 down to match the same length as v2.

            If False, do not shrink v1 at all.

            If int, shrink both v1 and v2 down to this length.

            Defaults to: True.

    Returns:
        :obj:`bool`

    """
    v1, v2 = version_recomp(v1=v1, v2=v2, vshrink=vshrink)
    return v1 >= v2


def version_max(v1, v2, vshrink=True):
    """Check if v1 is less than or equal to v2.

    Args:
        v1 (:obj:`str` or :obj:`list`):
            Version that is being compared against veq, vmax, and vmin.

            Will be be shrunk down to the same dotted length as veq, vmax, and vmin
            if vshrink is True.
        v2 (:obj:`str` or :obj:`list`):
            Version that v1 is being compared against.
        vshrink (:obj:`bool` or :obj:`int`, optional):
            If True, shrink v1 down to match the same length as v2.

            If False, do not shrink v1 at all.

            If int, shrink both v1 and v2 down to this length.

            Defaults to: True.

    Returns:
        :obj:`bool`

    """
    v1, v2 = version_recomp(v1=v1, v2=v2, vshrink=vshrink)
    return v1 <= v2


def version_check(version, veq="", vmax="", vmin="", vshrink=True):
    """Check if version meets veq, vmax, and vmin.

    Args:
        version (:obj:`str` or :obj:`list`):
            Version that is being compared against veq, vmax, and vmin.

            Will be be shrunk down to the same dotted length as veq, vmax, and vmin
            if vshrink is True.
        veq (:obj:`str`, optional):
            Exact version that version must match.

            No comparison performed if empty.

            Defaults to: "".
        vmin (:obj:`str`, optional):
            Minimum version that version must match.

            No comparison performed if empty.

            Defaults to: "".
        vmax (:obj:`str`, optional):
            Maximum version that version must match.

            No comparison performed if empty.

            Defaults to: "".
        vshrink (:obj:`bool` or :obj:`int`, optional):
            If True, shrink version down to match the same length as
            veq, vmax, and vmin.

            If False, do not shrink version at all.

            If int, shrink version, veq, vmax, and vmin down to this length.

            Defaults to: True.

    Returns:
        :obj:`bool`

    """
    if veq and not version_eq(v1=version, v2=veq, vshrink=vshrink):
        return False
    if vmax and not version_max(v1=version, v2=vmax, vshrink=vshrink):
        return False
    if vmin and not version_min(v1=version, v2=vmin, vshrink=vshrink):
        return False
    return True


def version_check_obj_req(version, src, obj):
    """Check if veq, vmax, and vmin from a classes get_version_req meets version.

    Args:
        version (:obj:`str` or :obj:`list`):
            Version that is being compared against veq, vmax, and vmin keys
            in the dict returned from the get_version_req class of obj.

            Will be be shrunk down to the same dotted length as veq, vmax, and vmin
            if vshrink is True.

        src (:obj:`str`):
            Where version came from, used in exception message.
        obj (:obj:`object`):
            Object or class that has get_version_req class method.

    Raises:
        :exc:`tantrum.utils.exceptions.VersionMismatchError`:
              If any of veq, vmax, vmin keys in dict returned by get_version_req
              do not match version.

    """
    version_req = obj.get_version_req()
    vmin = version_req.get("vmin", "")
    vmax = version_req.get("vmax", "")
    veq = version_req.get("veq", "")
    if not version_check(version=version, veq=veq, vmax=vmax, vmin=vmin):
        reqs = ", ".join(
            [
                "a minimum of {!r}".format(vmin or None),
                "a maximum of {!r}".format(vmax or None),
                "and equal to {!r}".format(veq or None),
            ]
        )
        error = "\n  ".join(
            [
                "",
                "{o} failed a version requirement!",
                "Version must be {reqs}",
                "{src!r} is version {v!r}",
            ]
        )
        error = error.format(o=obj, reqs=reqs, v=version, src=src)
        raise exceptions.VersionMismatchError(error)


def split_ver(v):
    """Split v into a list of integers.

    Args:
        v (:obj:`str` or :obj:`list` of :obj:`int` or :obj:`int`):
            Version string to split using periods.

    Returns:
        :obj:`list` of :obj:`int` or :obj:`str`

    """
    v = v.split(".") if isinstance(v, six.string_types) else v
    return [
        int(x) if isinstance(x, six.string_types) and x.isdigit() else x
        for x in v
        if x not in ["", None]
    ]


def join_ver(v):
    """Join v into a dot string.

    Args:
        v (:obj:`str` or :obj:`list` of :obj:`int` or :obj:`int`):
            Version string to join using periods.

    Returns:
        :obj:`str`

    """
    return ".".join([format(x) for x in v]) if isinstance(v, list) else v
