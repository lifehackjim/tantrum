# -*- coding: utf-8 -*-
"""Exceptions and warnings for :mod:`tantrum.api_models`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pprint

from .. import exceptions


class ModuleError(exceptions.TantrumError):
    """Parent of all exceptions for :mod:`tantrum.api_models`."""

    pass


class ModuleWarning(exceptions.TantrumWarning):
    """Parent of all warnings for :mod:`tantrum.api_models`."""

    pass


class AttrUndefinedWarning(ModuleWarning):
    """Warning handler for a simple value being set on an undefined attribute."""

    def __init__(self, obj, attr, value):
        """Constructor.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                Object that warning was thrown from.
            attr (:obj:`str`):
                Simple attribute that was adhoc added.
            value (:obj:`int` or :obj:`str` or :obj:`bool`):
                Value of attr.

        """
        self.obj = obj
        """:obj:`tantrum.api_models.ApiModel`: Object that warning was thrown from."""
        self.attr = attr
        """:obj:`str`: Simple attribute that was adhoc added."""
        self.value = value
        """:obj:`int` or :obj:`str` or :obj:`bool`: Value of attr."""

        error = [
            "Adhoc added undefined simple attribute: "
            "{attr!r} of type {valtype!r} to {cls!r}"
        ]
        error = "\n".join(error)
        self.error = error.format(
            cls=obj.__class__.__name__, attr=attr, valtype=type(value).__name__
        )
        """:obj:`str`: Warning message that was thrown."""
        super(AttrUndefinedWarning, self).__init__(self.error)


class AttrUndefinedError(ModuleError):
    """Exception handler for a complex value being set on an undefined attribute."""

    def __init__(self, obj, attr, value):
        """Constructor.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                Object that exception was thrown from.
            attr (:obj:`str`):
                Complex attribute that was supplied.
            value (:obj:`dict` or :obj:`list`):
                Value of attr.

        """
        self.obj = obj
        """:obj:`tantrum.api_models.ApiModel`: Object that exception was thrown from."""
        self.attr = attr
        """:obj:`str`: Complex attribute that was supplied."""
        self.value = value
        """:obj:`dict` or :obj:`list`: Value of attr."""

        error = [
            "",
            "{def_attrs}",
            "Received attribute {attr!r} of type {valtype!r} on {cls!r}",
            "But attribute is not defined as a complex attribute.",
        ]
        error = "\n".join(error)
        self.error = error.format(
            cls=obj.__class__,
            attr=attr,
            valtype=type(value).__name__,
            def_attrs="\n".join(obj.api_attrs_desc()),
        )
        """:obj:`str`: Error message that was thrown."""
        super(AttrUndefinedError, self).__init__(self.error)


class AttrTypeError(ModuleError):
    """Exception handler for type mismatch on a defined attribute."""

    def __init__(self, obj, attr, value, be_type):
        """Constructor.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                Object that exception was thrown from.
            attr (:obj:`str`):
                Attribute that had a type mismatch.
            value (:obj:`object`):
                Value of attr.
            be_type (:class:`object`):
                Type that value should be, but is not.

        """
        self.obj = obj
        """:obj:`tantrum.api_models.ApiModel`: Object that exception was thrown from."""
        self.attr = attr
        """:obj:`str`: Attribute that had a type mismatch."""
        self.value = value
        """:obj:`object`: Value of attr."""
        self.be_type = be_type
        """:class:`object`: Type that value should be, but is not."""

        error = [
            "",
            "Received attribute {attr!r} of type {valtype!r} on {cls!r}",
            "Type for attribute {attr!r} must be: {be_type!r}",
        ]
        error = "\n".join(error)
        self.error = error.format(
            cls=obj.__class__.__name__,
            attr=attr,
            be_type=be_type,
            valtype=type(value).__name__,
        )
        """:obj:`str`: Error message that was thrown."""
        super(AttrTypeError, self).__init__(self.error)


class ListTypeError(ModuleError):
    """Exception handler for type mismatch on a list action."""

    def __init__(self, obj, attr, value, op):
        """Constructor.

        Args:
            obj (:obj:`tantrum.api_models.ApiList`):
                Object that exception was thrown from.
            attr (:obj:`str`):
                Attribute that had a type mismatch.
            value (:obj:`object`):
                Value of attr.
            op (:obj:`str`):
                Operation being performed with type mismatch.

        """
        self.obj = obj
        """:obj:`tantrum.api_models.ApiList`: Object that exception was thrown from."""
        self.attr = attr
        """:obj:`str`: Attribute that had a type mismatch."""
        self.value = value
        """:obj:`object`: Value of attr."""
        self.op = op
        """:obj:`str`: Operation being performed with type mismatch."""

        atmpl = "on attribute {a!r} ".format(a=attr) if attr else ""

        error = [
            "",
            "While performing operation {op!r} on {cls!r} on attribute {attr}",
            "Invalid type of list {valtype!r} with value:",
            "{value}",
            "Must be a list, tuple, or an instance of {cls!r}",
        ]
        error = "\n".join(error)
        self.error = error.format(
            cls=obj.__class__.__name__,
            attr=atmpl,
            value=pprint.pformat(value),
            valtype=type(value).__name__,
            op=op,
        )
        """:obj:`str`: Error message that was thrown."""
        super(ListTypeError, self).__init__(self.error)


class ListItemTypeError(ModuleError):
    """Exception handler for type mismatch when adding an item to a list."""

    def __init__(self, obj, item, items, attr, op, be_type):
        """Constructor.

        Args:
            obj (:obj:`tantrum.api_models.ApiList`):
                Object that exception was thrown from.
            item (:obj:`object`):
                Item being added in items that is the wrong type.
            items (:obj:`list`):
                All items being added to list.
            attr (:obj:`str`):
                Attribute that had a type mismatch.
            op (:obj:`str`):
                Operation being performed with type mismatch.
            be_type (:class:`object`):
                Type that item should be, but is not.

        """
        self.obj = obj
        """:obj:`tantrum.api_models.ApiList`: Object that exception was thrown from."""
        self.item = item
        """:obj:`object`: Item being added in items that is the wrong type."""
        self.items = items
        """:obj:`list`: Full list of items containing item passed to op."""
        self.attr = attr
        """:obj:`str`: Attribute that had a type mismatch."""
        self.op = op
        """:obj:`str`: Operation being performed with type mismatch."""
        self.be_type = be_type
        """:class:`object`: Type that item should be, but is not."""

        error = [
            "",
            "While perform operation {op!r} on {cls!r}{attr}",
            "On item in a {lsttype} with {lstcnt} items",
            "Invalid type on item: {valtype!r} with value: {item!r}",
            "Item must be of type: {be_type}",
        ]
        error = "\n".join(error)
        self.error = error.format(
            cls=obj.__class__.__name__,
            attr=" on attribute {a!r} ".format(a=attr) if attr else "",
            item=item,
            lsttype=type(items),
            lstcnt=0 if items is None else len(items),
            be_type=be_type,
            op=op,
            valtype=type(item).__name__,
        )
        """:obj:`str`: Error message that was thrown."""
        super(ListItemTypeError, self).__init__(self.error)


class GetSingleItemError(ModuleError):
    """Exception handler when no items found."""

    def __init__(self, obj, attr, value, regex_value, items):
        """Constructor.

        Args:
            obj (:obj:`tantrum.api_models.ApiList`):
                Object that exception was thrown from.
            attr (:obj:`str`):
                Attribute to search for value of in items.
            value (:obj:`object`):
                Value of attr that was being used to match against items.
            regex_value (:obj:`bool`):
                If regex matching was being used for value.
            items (:obj:`list`):
                All items in list object.

        """
        self.obj = obj
        """:obj:`tantrum.api_models.ApiList`: Object that exception was thrown from."""
        self.attr = attr
        """:obj:`str`: Attribute used to search for value of in items."""
        self.value = value
        """:obj:`object`: Value of attr that was being used to match against items."""
        self.regex_value = regex_value
        """:obj:`bool`: If regex matching was being used for value."""
        self.items = items
        """:obj:`list`: All items found in list object."""

        itemvals = [format(getattr(x, attr, None)) for x in obj]
        itemvals = "\n  ".join(itemvals or ["Empty list!"])

        error = [
            "",
            "All values for attribute {attr!r} type {attrtype} in {obj}:",
            "  {itemvals}",
            "",
            "Found {cnt} items while searching for:",
            " 1 item where {attr!r} {op} value {value!r} of type {vt}:",
        ]

        error = "\n".join(error)
        self.error = error.format(
            attr=attr,
            attrtype=obj.API_ITEM_CLS.api_attrs()[attr],
            obj=obj,
            itemvals=itemvals,
            value=value,
            vt=type(value),
            op="regex matches" if regex_value else "equals",
            cnt=len(items),
        )
        """:obj:`str`: Error message that was thrown."""
        super(GetSingleItemError, self).__init__(self.error)
