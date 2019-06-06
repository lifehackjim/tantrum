# -*- coding: utf-8 -*-
"""Models for Python objects in Tanium's API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
import json
import operator
import re
import six
import warnings

from . import exceptions

float_types = (float,)
""":obj:`tuple` of :obj:`type`: Float types."""

integer_types = six.integer_types
""":obj:`tuple` of :obj:`type`: Integer types."""

string_types = six.string_types
""":obj:`tuple` of :obj:`type`: String types."""

simple_types = tuple(list(integer_types) + list(string_types) + list(float_types))
""":obj:`tuple` of :obj:`type`: All types that should be considered simple types."""


class ApiModel(object):
    """Base class for all models in the API."""

    API_NAME = None
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = None
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = None
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = None
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = None
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = None
    """:obj:`list` or :obj:`str`: Added to :attr:`API_STR` in str."""

    T_ATTR_REPR = "{attr}={value!r}"
    """:obj:`str`: Template for simple attrs in str and all attr in repr."""

    T_ATTR_STR = "{attr}={value}"
    """:obj:`str`: Template for complex attrs in str."""

    T_ATTR_JOIN = ", "
    """:obj:`str`: String used to join attr vals in str and repr."""

    T_CLS_STR = "{obj.__class__.__name__}({attrs})"
    """:obj:`str`: Template for class name and attrs in str."""

    T_CLS_REPR = "{obj.__class__.__name__}({attrs})"
    """:obj:`str`: Template for class name and attrs in repr."""

    T_ATTR_DESC = "  - {api_type} attribute {attr!r} of type {attr_type!r}"
    """:obj:`str`: Template for attr line in :meth:`api_attrs_desc`."""

    T_DESC = "Defined attributes:"
    """:obj:`str`: Template for first line in :meth:`api_attrs_desc`."""

    API_STR = [
        "id",
        "name",
        "display_name",
        "value",
        "type",
        "public_flag",
        "hidden_flag",
        "question",
        "query_text",
        "question_text",
        "expiration",
        "saved_question",
        "from_canonical_text",
    ]
    """:obj:`list` of :obj:`str`: Attrs to display in str or to put first in repr."""

    def __copy__(self):
        """Support shallow copy for self.

        Returns:
            :obj:`ApiItem`

        """
        return self.__class__(**self.__dict__)

    def __deepcopy__(self, memo):
        """Support deep copy for self.

        Returns:
            :obj:`ApiItem`

        """
        self_dict = self.serialize(wrap_name=False)
        new_dict = copy.deepcopy(self_dict, memo)
        return self.__class__(**new_dict)

    def __eq__(self, value):
        """Support for self == value.

        Args:
            value (:obj:`dict` or :obj:`list` or :obj:`ApiModel` or :obj:`object`):
                Value for comparison.

        Notes:
            * If value is a dict, it will be turned into an ApiModel.
            * If this object is an ApiList and value is a list, it will be turned
              into an ApiList.
            * If value is turned into or already is an ApiModel, it will be serialized
              into a dict/list.
            * Finally, actual comparison of value is done against this object
              serialized into a dict/list.

        Returns:
            :obj:`bool`

        """
        sargs = {"wrap_name": False, "wrap_item_attr": False}
        this = self.serialize(**sargs)

        if isinstance(value, dict):
            value = self.__class__(**value)
        elif isinstance(value, list) and isinstance(self, ApiList):
            value = self.__class__(*value)

        if isinstance(value, ApiModel):
            value = value.serialize(**sargs)

        return this == value

    def __ne__(self, value):
        """Support for self != value.

        Args:
            value (:obj:`dict` or :obj:`list` or :obj:`ApiModel` or :obj:`object`):
                Value for comparison.

        Returns:
            :obj:`bool`

        """
        return not self == value

    @classmethod
    def api_attrs(cls):
        """Get simple and complex attributes combined.

        Returns:
            :obj:`dict`

        """
        return dict(list(cls.API_SIMPLE.items()) + list(cls.API_COMPLEX.items()))

    @classmethod
    def api_attrs_repr(cls):
        """Get attributes for repr formatting.

        Notes:
            Will return attrs without dupes in order of priority to show on
            format string from :attr:`API_STR`, :attr:`API_STR_ADD`,
            and :meth:`api_attrs`.

        Returns:
            :obj:`list` of :obj:`str`

        """
        api_attrs = cls.api_attrs()
        show_attrs = cls.API_STR + cls.API_STR_ADD + list(api_attrs)
        attrs = []
        for attr in show_attrs:
            if attr not in attrs and (attr in api_attrs or hasattr(cls, attr)):
                attrs.append(attr)
        return attrs or list(api_attrs)

    @classmethod
    def api_attrs_str(cls):
        """Get attributes for str formatting.

        Notes:
            Will return attrs without dupes in order of priority to show on
            format string from :attr:`API_STR` and :attr:`API_STR_ADD`.

            If no attrs from :attr:`API_STR` and :attr:`API_STR_ADD` exist
            in :meth:`api_attrs`, return all attrs from :meth:`api_attrs`.

        Returns:
            :obj:`list` of :obj:`str`

        """
        api_attrs = cls.api_attrs()
        show_attrs = cls.API_STR + cls.API_STR_ADD
        attrs = []
        for attr in show_attrs:
            if attr not in attrs and (attr in api_attrs or hasattr(cls, attr)):
                attrs.append(attr)
        return attrs or list(api_attrs)

    @classmethod
    def api_attrs_desc(cls):
        """Get description of attrs from :attr:`API_SIMPLE` and :attr:`API_COMPLEX`.

        Notes:
            Used by exceptions to add defined attributes to error messages.

        Returns:
            :obj:`list` of :obj:`str`

        """
        tmpl = cls.T_ATTR_DESC.format
        lines = []
        lines.append(cls.T_DESC)
        for attr, attr_type in cls.API_SIMPLE.items():
            desc = tmpl(api_type="simple", attr=attr, attr_type=attr_type)
            lines.append(desc)
        for attr, attr_type in cls.API_COMPLEX.items():
            desc = tmpl(api_type="complex", attr=attr, attr_type=attr_type)
            lines.append(desc)
        return lines

    @classmethod
    def api_coerce_int(cls, value):
        """Try to coerce value into :obj:`int` if possible.

        Args:
            value (:obj:`object`):
                Object to coerce into int.

        Returns:
            :obj:`int` or :obj:`object` if unchanged.

        """
        try:
            return int(value)
        except Exception:
            return None if value == "" else value
            # REST GetResultData can return "max_available_age" of ""

    @classmethod
    def api_coerce_float(cls, value):
        """Try to coerce value into :obj:`float` if possible.

        Args:
            value (:obj:`object`):
                Object to coerce into float.

        Returns:
            :obj:`float` or :obj:`object` if unchanged.

        """
        try:
            return float(value)
        except Exception:
            return value

    @classmethod
    def api_coerce_list(cls, value):
        """Coerce value into :obj:`list` if it is not already.

        Args:
            value (:obj:`object`):
                Object to coerce into list. If value is None, will return empty list.

        Returns:
            :obj:`list` or :obj:`object` if unchanged.

        """
        if value is None:
            return []
        if not isinstance(value, (list, tuple)):
            return [value]
        return value

    @classmethod
    def api_coerce_simple(cls, value, be_type):
        """Try to coerce a value into a simple type.

        Args:
            value (:obj:`object`):
                Value that should be coerced.
            be_type (:class:`object`):
                Type that value should be coerced to.

        Returns:
            :obj:`float` or :obj:`int` or :obj:`str` or :obj:`object` if unchanged.

        """
        if be_type == float_types and not isinstance(value, float_types):
            return cls.api_coerce_float(value=value)
        elif be_type == integer_types:
            if isinstance(value, bool) or not isinstance(value, integer_types):
                return cls.api_coerce_int(value=value)
        elif be_type == string_types and isinstance(value, simple_types):
            return format(value)
        return value

    @classmethod
    def api_coerce_complex(cls, value, be_type):
        """Try to coerce a value into a complex type.

        Args:
            value (:obj:`object`):
                Value that should be coerced.
            be_type (:class:`object`):
                Type that value should be coerced to.

        Returns:
            :obj:`ApiItem` or :obj:`ApiList` or :obj:`object` if unchanged.

        """
        if not isinstance(value, be_type):
            if isinstance(value, dict):
                return be_type(**value)
            elif isinstance(value, (list, tuple)):
                return be_type(*value)
        return value

    def api_coerce_value(self, attr, value):
        """Perform type checking of value.

        Will coerce value into expected type if needed and possible.

        Args:
            attr (:obj:`str`):
                Attribute that is being set with value on obj.
            value (:obj:`object`):
                Value of attr being checked.

        Raises:
            :exc:`tantrum.api_models.exceptions.AttrTypeError`:
                If value is not the expected type after all of this magic.
            :exc:`tantrum.api_models.exceptions.AttrUndefinedError`:
                If value type is not :data:`simple_types` and attr is not in
                :attr:`api_attrs`.
            :exc:`tantrum.api_models.exceptions.AttrUndefinedWarning`:
                If value type is :data:`simple_types` and attr not in
                :attr:`api_attrs`.

        Notes:
            No checking or coercion is done if:
                * value is None
                * attr starts with "_"
                * attr is all upper case

        Returns:
            :obj:`object`

        """
        if value is None or attr.startswith("_") or attr.isupper():
            return value

        if attr not in self.api_attrs():
            if isinstance(value, bool) or isinstance(value, integer_types):
                self.API_SIMPLE[attr] = integer_types
            elif isinstance(value, float_types):
                self.API_SIMPLE[attr] = float_types
            elif isinstance(value, string_types):
                self.API_SIMPLE[attr] = string_types
            else:
                raise exceptions.AttrUndefinedError(obj=self, attr=attr, value=value)
            warnings.warn(
                exceptions.AttrUndefinedWarning(obj=self, attr=attr, value=value)
            )

        be_type = self.api_attrs()[attr]

        if attr in self.API_SIMPLE:
            value = self.api_coerce_simple(value=value, be_type=be_type)
        if attr in self.API_COMPLEX:
            value = self.api_coerce_complex(value=value, be_type=be_type)

        if isinstance(value, be_type) or value is None:
            return value
        raise exceptions.AttrTypeError(
            obj=self, value=value, attr=attr, be_type=be_type
        )

    def serialize_json(self):
        ser = self.serialize()
        return json.dumps(ser, indent=2)


class ApiItem(ApiModel):
    """Model for a complex item in the API."""

    API_LIST_API_NAME = None
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""

    API_LIST_CLS = None
    """:class:`ApiList`: List class that holds this item class."""

    def __init__(self, **kwargs):
        """Constructor.

        Args:
            **kwargs:
                Set and checked using :meth:`ApiModel.api_attrs`.

        """
        for attr in self.api_attrs():
            setattr(self, attr, kwargs.pop(attr, None))
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __len__(self):
        """Return number of :meth:`ApiModel.api_attrs` that are not None.

        Returns:
            :obj:`int`

        """
        api_attrs = self.api_attrs()
        set_attrs = [k for k in api_attrs if getattr(self, k, None) is not None]
        return len(set_attrs)

    def __str__(self):
        """Show object info using :meth:`ApiModel.api_attrs_str`.

        Returns:
            :obj:`str`

        """
        show_attrs = self.api_attrs_str()
        attrs = []
        for attr in show_attrs:
            value = getattr(self, attr, None)
            tmpl = self.T_ATTR_STR if attr in self.API_COMPLEX else self.T_ATTR_REPR
            attrs.append(tmpl.format(attr=attr, value=value))

        attrs = self.T_ATTR_JOIN.join(attrs)
        return self.T_CLS_STR.format(obj=self, attrs=attrs)

    def __repr__(self):
        """Show object info using :meth:`ApiModel.api_attrs_repr`.

        Returns:
            :obj:`str`

        """
        show_attrs = self.api_attrs_repr()
        attrs = []
        for attr in show_attrs:
            value = getattr(self, attr, None)
            tmpl = self.T_ATTR_REPR
            attrs.append(tmpl.format(attr=attr, value=value))
        attrs = self.T_ATTR_JOIN.join(attrs)
        return self.T_CLS_REPR.format(obj=self, attrs=attrs)

    def __setattr__(self, attr, value):
        """Enforce type using :meth:`ApiModel.api_coerce_value`."""
        value = self.api_coerce_value(attr=attr, value=value)
        super(ApiItem, self).__setattr__(attr, value)

    def serialize(
        self,
        empty=False,
        list_attrs=False,
        exclude_attrs=None,
        only_attrs=None,
        wrap_name=True,
        wrap_item_attr=True,
    ):
        """Serialize this object into a dict.

        Args:
            empty (:obj:`bool`, optional):
                Include attrs that have a value of None when serializing.

                Defaults to: False.
            list_attrs (:obj:`bool`, optional):
                Include simple attrs of :obj:`ApiList` when serializing.

                Defaults to: False.
            exclude_attrs (:obj:`list` of :obj:`str`, optional):
                Exclude these attrs when serializing.

                Defaults to: None.
            only_attrs (:obj:`list` of :obj:`str`, optional):
                Include only these attrs when serializing.

                Defaults to: None.
            wrap_name (:obj:`bool`, optional):
                Wrap return in a dict with key of :attr:`ApiModel.API_NAME` and
                value of return.

                Defaults to: True.
            wrap_item_attr (:obj:`bool`, optional):
                Wrap return in a dict with key of :attr:`ApiList.API_ITEM_ATTR`
                and value of return.

                Only used when serializing items of type :obj:`ApiList`.

                Defaults to: True.

        Notes:
            All child objects will get wrap_name=False.

        Returns:
            :obj:`dict`

        """
        exclude_attrs = self.api_coerce_list(value=exclude_attrs)
        only_attrs = self.api_coerce_list(value=only_attrs)
        ret = {}
        sargs = {
            "empty": empty,
            "exclude_attrs": exclude_attrs,
            "only_attrs": only_attrs,
            "list_attrs": list_attrs,
            "wrap_name": False,
            "wrap_item_attr": wrap_item_attr,
        }
        for attr in self.api_attrs():
            if attr in exclude_attrs or (only_attrs and attr not in only_attrs):
                continue
            value = getattr(self, attr, None)
            is_model = isinstance(value, ApiModel)
            value = value.serialize(**sargs) if is_model else value
            include = (value is None and empty) or value is not None
            ret.update({attr: value} if include else {})
        if wrap_name:
            ret = {self.API_NAME: ret}
        return ret


class ApiList(ApiModel):
    """Model for an array in the API."""

    API_ITEM_ATTR = None
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = None
    """:class:`ApiItem`: Item class this list class holds."""

    LIST = None
    """:obj:`list` of :attr:`API_ITEM_CLS`: List container for this class."""

    T_CLS_STR = "{obj.__class__.__name__}({attrs}) with {count} {item_cls} objects"
    """:obj:`str`: Template for class name and attrs in str."""

    def __init__(self, *args, **kwargs):
        """Constructor.

        Args:
            *args:
                Items of type :attr:`API_ITEM_CLS`:
                    Will be added to :attr:`LIST`.
            **kwargs:
                attr from :attr:`API_ITEM_ATTR` (:obj:`list`):
                    List of :attr:`API_ITEM_CLS` to add to :attr:`LIST`.
                rest of kwargs:
                    Set on this object with type checking using.

        """
        super(ApiList, self).__setattr__("LIST", [])

        # support obj(item1, item2, **kwargs)
        items = list(args)

        # support obj(item_attr=value)
        if self.API_ITEM_ATTR in kwargs:
            value = kwargs.pop(self.API_ITEM_ATTR)
            # support obj(self.API_ITEM_ATTR=(item1, item2))
            if isinstance(value, tuple):
                value = list(value)
            # support obj(self.API_ITEM_ATTR=None)
            if value is None:
                value = []
            # support obj(self.API_ITEM_ATTR=item1)
            if not isinstance(value, list):
                value = [value]
            # finally, support obj(self.API_ITEM_ATTR=[item1, item2])
            items += value

        self.LIST = items

        for attr in self.api_attrs():
            setattr(self, attr, kwargs.pop(attr, None))
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __str__(self):
        """Show object info using :meth:`ApiModel.api_attrs_str`.

        Returns:
            :obj:`str`

        """
        show_attrs = self.api_attrs_str()
        attrs = []
        for attr in show_attrs:
            value = getattr(self, attr, None)
            tmpl = self.T_ATTR_STR if attr in self.API_COMPLEX else self.T_ATTR_REPR
            attrs.append(tmpl.format(attr=attr, value=value))

        attrs = self.T_ATTR_JOIN.join(attrs)
        return self.T_CLS_STR.format(
            obj=self, attrs=attrs, count=len(self), item_cls=self.api_item_cls_str()
        )

    def __repr__(self):
        """Show object info using :meth:`ApiModel.api_attrs_repr`.

        Returns:
            :obj:`str`

        """
        show_attrs = self.api_attrs_repr()
        attrs = []
        tmpl = self.T_ATTR_REPR
        for attr in show_attrs:
            value = getattr(self, attr, None)
            attrs.append(tmpl.format(attr=attr, value=value))
        value = [format(i) for i in self]
        attrs.append(tmpl.format(attr=self.API_ITEM_ATTR, value=value))
        attrs = self.T_ATTR_JOIN.join(attrs)
        return self.T_CLS_REPR.format(obj=self, attrs=attrs)

    def __len__(self):
        """Return length of list container :attr:`LIST`.

        Returns:
            :obj:`int`

        """
        return len(self.LIST)

    def __contains__(self, value):
        """Support in operand.

        Args:
            value (:obj:`object`):
                Check if this value in :attr:`LIST`.

        Notes:
            Will call :meth:`api_coerce_item` to check value is of type defined in
            :attr:`API_ITEM_CLS`, but will return False if value is of wrong type
            and can not be coerced.

        Returns:
            :obj:`bool`:

        """
        try:
            value = self.api_coerce_item(item=value, items=None, attr=None, op="in")
        except Exception:
            return False
        return value in self.LIST

    def __add__(self, value):
        """Support + operand.

        Args:
            value (:obj:`ApiList` or :obj:`list` or :obj:`tuple`):
                ApiList of this same type or a python list type to combine
                with this object.

        Notes:
            This will use :meth:`api_coerce_items` to perform type checking
            on each item in value.

        Returns:
            :obj:`ApiList`:
                A new instance with list items from this object combined with
                list items from value.

        """
        api_attrs = self.api_attrs()

        val_items = self.api_coerce_items(attr=None, value=value, op="+=")
        mod_items = val_items + self.LIST
        attrs = {k: getattr(self, k, None) for k, v in api_attrs.items()}
        return self.__class__(*mod_items, **attrs)

    def __iadd__(self, value):
        """Support += operand.

        Args:
            value (:obj:`ApiList` or :obj:`list` or :obj:`tuple`):
                ApiList of this same type or a python list type to combine
                with this object.

        Notes:
            This will use :meth:`api_coerce_items` to perform type checking
            on each item in value.

        Returns:
            :obj:`ApiList`:
                This object with list items from value appended.

        """
        mod_items = self.api_coerce_items(attr=None, value=value, op="+=")
        self.LIST += mod_items
        return self

    def __getitem__(self, value):
        """Support indexing of list container.

        Args:
            value (:obj:`int`):
                Index of item to retrieve from :attr:`LIST`.

        Returns:
            :attr:`API_ITEM_CLS`:
                The type of object this list contains.

        """
        return self.LIST[value]

    def __setattr__(self, attr, value):
        """Enforce type checking for attr and value.

        Args:
            attr (:obj:`str`):
                Attribute to set on this object.
            value (:obj:`object`):
                Value to perform type checking on using
                :func:`ApiModel.api_coerce_value`.

        Notes:
            If attr is either "LIST" or :attr:`API_ITEM_ATTR`, will use
            :meth:`api_coerce_items` to perform type checking on each item in value.

            If attr is same as :attr:`API_ITEM_ATTR`, the attr will
            be changed to "LIST".

        """
        if attr in [self.API_ITEM_ATTR, "LIST"]:
            value = self.api_coerce_items(attr=attr, value=value, op="=")
            attr = "LIST"
        else:
            value = self.api_coerce_value(attr=attr, value=value)
        super(ApiList, self).__setattr__(attr, value)

    def api_coerce_items(self, attr, value, op):
        """Check that value is a list type and that all items value are the proper type.

        Args:
            attr (:obj:`str`):
                Attribute being set on this object.
            value (:obj:`ApiList` or :obj:`list` or :obj:`tuple`):
                The list object holding items that should have type checking.
            op (:obj:`str`):
                Operation being performed that called this method.

                Used in exception messages.

        Raises:
            :exc:`tantrum.api_models.exceptions.ListTypeError`:
                If value is not a :obj:`list` or :obj:`tuple` or an :obj:`ApiList`
                that is the same type as this objects class.

        Notes:
            Will call :meth:`api_coerce_items_hook` before checking each item
            in value, which can be overridden by subclasses to modify value.

            Will call :meth:`api_coerce_item` to check each item in value
            is of type defined in :attr:`API_ITEM_CLS`.

        Returns:
            :obj:`list`:
                The list of items with their values checked and coerced.

        """
        if value is None:
            return []
        is_list = isinstance(value, (list, tuple))
        is_same = isinstance(value, self.__class__)
        if not any([is_list, is_same]):
            raise exceptions.ListTypeError(obj=self, attr=attr, value=value, op=op)
        value = self.api_coerce_items_hook(attr=attr, value=value, op=op)
        return [
            self.api_coerce_item(item=i, items=value, attr=attr, op=op) for i in value
        ]

    def api_coerce_items_hook(self, attr, value, op):
        """Check hook that allows subclasses to modify list items.

        Args:
            attr (:obj:`str`):
                Attribute being set on this object.
            value (:obj:`ApiList` or :obj:`list` or :obj:`tuple`):
                The list object holding items.
            op (:obj:`str`):
                Operation being performed that called this method.

        Notes:
            By default, this does nothing but return value unchanged.

        Returns:
            :obj:`list`:
                The list of items modified or as is.

        """
        return value

    def api_coerce_item(self, item, items, attr, op):
        """Perform type checking of a list item.

        Args:
            item (:obj:`object`):
                Item that is being checked.
            items (:obj:`ApiList` or :obj:`list` or :obj:`tuple`):
                The list object that item came from.
            op (:obj:`str`):
                Operation being performed that called this method.

                Used in exception messages.

        Notes:
            Will coerce item into expected type if needed and possible.

        Raises:
            :exc:`tantrum.api_models.exceptions.ListItemTypeError`:
                If item does not match the type from :obj:`API_ITEM_CLS`
                and it can not be coerced into the expected type.

        Returns:
            :obj:`object`

        """
        be_type = self.API_ITEM_CLS

        if be_type is None:
            return item

        if self.api_item_cls_is_complex():
            if isinstance(item, dict):
                return be_type(**item)
            elif isinstance(item, (list, tuple)):
                return be_type(*item)

        if not isinstance(item, be_type):
            if be_type == float_types:
                return self.api_coerce_float(value=item)
            if be_type == integer_types:
                return self.api_coerce_int(value=item)
            if be_type == string_types and isinstance(item, simple_types):
                return item

        if not isinstance(item, be_type):
            raise exceptions.ListItemTypeError(
                obj=self, item=item, items=items, op=op, attr=attr, be_type=be_type
            )
        return item

    @classmethod
    def api_attrs_desc(cls):
        """Get simple and complex attributes of an ApiModel object in string format.

        Notes:
            Used by exceptions to add defined attributes to error messages.

        Returns:
            :obj:`list` of :obj:`str`

        """
        lines = super(ApiList, cls).api_attrs_desc()
        tmpl = cls.T_ATTR_DESC.format
        desc = tmpl(api_type="List", attr=cls.API_ITEM_ATTR, attr_type=cls.API_ITEM_CLS)
        lines.append(desc)
        return lines

    @classmethod
    def api_item_cls_str(cls):
        """Get str of :attr:`API_ITEM_CLS`.

        Returns:
            :obj:`str`

        """
        classes = cls.api_coerce_list(cls.API_ITEM_CLS)
        names = [x.__name__ for x in classes if hasattr(x, "__name__")]
        names = names or ["ANY TYPE"]
        return ", ".join(names)

    @classmethod
    def api_item_cls_is_complex(cls):
        """Check if :attr:`API_ITEM_CLS` is an ApiModel sub class.

        Returns:
            :obj:`bool`

        """
        check = cls.api_coerce_list(cls.API_ITEM_CLS)
        return any(issubclass(x, (ApiItem, ApiList)) for x in check)

    def append(self, value):
        """Support appending an item to list container.

        Args:
            value (:obj:`object`):
                Item to append to :attr:`LIST`.

        Notes:
            Will call :meth:`api_coerce_item` to check value
            is of type defined in :attr:`API_ITEM_CLS`.

        """
        value = self.api_coerce_item(item=value, items=None, attr=None, op="append()")
        self.LIST.append(value)

    def remove(self, value):
        """Support removing an item from list container.

        Args:
            value (:obj:`object`):
                Item to remove from :attr:`LIST`.

        """
        value = self.api_coerce_item(item=value, items=None, attr=None, op="remove()")
        return self.LIST.remove(value)

    def pop(self, value=-1):
        """Support pop of an item from list container.

        Args:
            value (:obj:`object`, optional):
                Item to pop from :attr:`LIST`.

                Defaults to: -1.

        """
        return self.LIST.pop(value)

    def reverse(self):
        """Support reverse on list container."""
        self.LIST.reverse()

    def get_item_by_attr(self, value, attr="name", regex_value=False):
        """Support getting an item from list container by attr value.

        Args:
            value (:obj:`object`):
                Value to check against the attr value of each item in :attr:`LIST`.
            attr (:obj:`str`, optional):
                Attribute to check if value matches.

                Defaults to: "name".
            regex_value (:obj:`bool`, optional):
                Treat value as a regex pattern instead of comparing equality of value
                to attr value.

                Defaults to: False.

        Raises:
            :exc:`tantrum.api_models.exceptions.GetSingleItemError`:
                If number of items in :attr:`LIST` whose attr value
                matches value is either 0 or more than 1.

        Returns:
            :obj:`object`:
                The object from :attr:`LIST` whose attr value matches value.

        """
        items = []
        for i in self.LIST:
            ival = getattr(i, attr, None)
            if regex_value and re.search(format(value), format(ival)):
                items.append(i)
            elif ival == value:
                items.append(i)
        if len(items) == 1:
            return items[0]
        raise exceptions.GetSingleItemError(
            obj=self, value=value, attr=attr, regex_value=regex_value, items=items
        )

    def get_items_by_attr(self, value, attr="name", regex_value=False, new_list=False):
        """Support getting items from list container by attr value.

        Args:
            value (:obj:`object`):
                Value to check against the attr value of each item in :attr:`LIST`.
            attr (:obj:`str`, optional):
                Attribute to check if value matches.

                Defaults to: "name".
            regex_value (:obj:`bool`, optional):
                Treat value as a regex pattern instead of comparing equality of value
                to attr value.

                Defaults to: False.
            new_list (:obj:`bool`, optional):
                Return a new class of this objects type with matching items instead
                of a regular python list type.

                Defaults to: False.

        Returns:
            :obj:`list` of :obj:`object`:
                All objects from :attr:`LIST` whose attr value matches value.

        """
        items = []
        for i in self.LIST:
            ival = getattr(i, attr, None)
            if regex_value and re.search(format(value), format(ival)):
                items.append(i)
            elif ival == value:
                items.append(i)
        return self.__class__(*items) if new_list else items

    def pop_item_by_attr(self, value, attr="name", regex_value=False):
        """Support popping an item from list container by attr value.

        Args:
            value (:obj:`object`):
                Value to check against the attr value of each item in :attr:`LIST`.
            attr (:obj:`str`, optional):
                Attribute to check if value matches.

                Defaults to: "name".
            regex_value (:obj:`bool`, optional):
                Treat value as a regex pattern instead of comparing equality of value
                to attr value.

                Defaults to: False.

        Raises:
            :exc:`tantrum.api_models.exceptions.GetSingleItemError`:
                If number of items in :attr:`LIST` whose attr value
                matches value is either 0 or more than 1.

        Returns:
            :obj:`object`:
                The object popped from :attr:`LIST` whose attr value matches value.

        """
        item = self.get_item_by_attr(value, attr, regex_value)
        return self.LIST.pop(self.LIST.index(item))

    def pop_items_by_attr(self, value, attr="name", regex_value=False, new_list=False):
        """Support popping items from list container by attr value.

        Args:
            value (:obj:`object`):
                Value to check against the attr value of each item in :attr:`LIST`.
            attr (:obj:`str`, optional):
                Attribute to check if value matches.

                Defaults to: "name".
            regex_value (:obj:`bool`, optional):
                Treat value as a regex pattern instead of comparing equality of value
                to attr value.

                Defaults to: False.
            new_list (:obj:`bool`, optional):
                Return a new class of this objects type with matching items instead
                of a regular python list type.

                Defaults to: False.

        Returns:
            :obj:`list` of :obj:`object`:
                All objects popped from :attr:`LIST` whose attr value matches value.

        """
        items = self.get_items_by_attr(value, attr, regex_value, new_list)
        for i in items:
            self.LIST.remove(i)
        return items

    def sort(self, key=operator.attrgetter("id"), reverse=False):
        """Support sorting items in list container in place.

        Args:
            key (:obj:`object`, optional):
                Key to sort items in :attr:`LIST` on.

                Defaults to: operator.attrgetter("id").
            reverse (:obj:`bool`, optional):
                Reverse the sort mechanism.

                Defaults to: False.

        """
        self.LIST.sort(key=key, reverse=reverse)

    def serialize(
        self,
        empty=False,
        list_attrs=False,
        exclude_attrs=None,
        only_attrs=None,
        wrap_name=True,
        wrap_item_attr=True,
    ):
        """Serialize this object into a dict.

        Args:
            empty (:obj:`bool`, optional):
                Include attrs that have a value of None when serializing.

                Defaults to: False.
            list_attrs (:obj:`bool`, optional):
                Include simple attrs of :obj:`ApiList` when serializing.

                Defaults to: False.
            exclude_attrs (:obj:`list` of :obj:`str`, optional):
                Exclude these attrs when serializing.

                Defaults to: None.
            only_attrs (:obj:`list` of :obj:`str`, optional):
                Include only these attrs when serializing.

                Defaults to: None.
            wrap_name (:obj:`bool`, optional):
                Wrap return in a dict with key of :attr:`ApiModel.API_NAME` and
                value of return.

                Defaults to: True.
            wrap_item_attr (:obj:`bool`, optional):
                Wrap return in a dict with key of :attr:`ApiList.API_ITEM_ATTR`
                and value of return.

                Only used when serializing items of type :obj:`ApiList`.

                Defaults to: True.

        Notes:
            All child objects will get wrap_name=False.

            If wrap_name and wrap_item_attr are both False,
            return will be :obj:`list` of :obj:`dict`, otherwise return will be a
            :obj:`dict`.

        Returns:
            :obj:`list` of :obj:`object` or :obj:`dict`

        """
        exclude_attrs = self.api_coerce_list(value=exclude_attrs)
        only_attrs = self.api_coerce_list(value=only_attrs)
        sargs = {
            "empty": empty,
            "exclude_attrs": exclude_attrs,
            "only_attrs": only_attrs,
            "list_attrs": list_attrs,
            "wrap_name": False,
            "wrap_item_attr": wrap_item_attr,
        }
        simples = {}
        if list_attrs:
            for attr in self.api_attrs():
                if attr in exclude_attrs or (only_attrs and attr not in only_attrs):
                    continue
                value = getattr(self, attr, None)
                is_model = isinstance(value, ApiModel)
                value = value.serialize(**sargs) if is_model else value
                include = (value is None and empty) or value is not None
                simples.update({attr: value} if include else {})
        items = [i.serialize(**sargs) if isinstance(i, ApiModel) else i for i in self]
        if wrap_item_attr:
            ret = {}
            ret.update(simples)
            sub_ret = {self.API_ITEM_ATTR: items}
            if wrap_name:
                sub_ret = {self.API_NAME: sub_ret}
            ret.update(sub_ret)
            return ret
        if wrap_name:
            ret = {}
            ret.update(simples)
            ret.update({self.API_NAME: items})
            return ret
        return items
