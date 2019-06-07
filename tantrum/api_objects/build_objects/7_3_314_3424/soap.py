# -*- coding: utf-8 -*-
"""Python objects for Tanium's API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

from .. import api_models
from . import exceptions

float_types = (float,)
""":obj:`tuple` of :obj:`type`: Float types."""

integer_types = six.integer_types
""":obj:`tuple` of :obj:`type`: Integer types."""

string_types = six.string_types
""":obj:`tuple` of :obj:`type`: String types."""

simple_types = tuple(list(integer_types) + list(string_types) + list(float_types))
""":obj:`tuple` of :obj:`type`: All types that should be considered simple types."""

TYPE = "soap"
""":obj:`str`: Type of API this module was built from."""

API_DT = "%Y-%m-%dT%H:%M:%S"
""":obj:`str`: Datetime format for this API type and version."""


def api_fixes():
    """Fix incorrect attribute definitions on auto generated ApiModel classes."""
    models = get_api_all_model()

    fix = {"deleted_flag": "integer_types"}
    models["SavedQuestion"].API_SIMPLE.update(fix)

    fix = {"external_flag": "integer_types"}
    models["User"].API_SIMPLE.update(fix)

    fix = {"cache_row_id": "integer_types"}
    models["AuditData"].API_SIMPLE.update(fix)

    fix = {"cache_info": "CacheInfo"}
    models["AuditDataList"].API_COMPLEX.update(fix)


def expand_cls_globals():
    """Replace str values with global vars for attrs on ApiModel classes.

    Quite the funky chicken dance for solving issues with order of class definition.
    """
    item_classes = ApiItem.__subclasses__()
    list_classes = ApiList.__subclasses__()
    for c in item_classes:
        c.API_SIMPLE = expand_global(obj=c.API_SIMPLE)
        c.API_COMPLEX = expand_global(obj=c.API_COMPLEX)
        c.API_LIST_CLS = expand_global(obj=c.API_LIST_CLS)
    for c in list_classes:
        c.API_SIMPLE = expand_global(obj=c.API_SIMPLE)
        c.API_COMPLEX = expand_global(obj=c.API_COMPLEX)
        c.API_ITEM_CLS = expand_global(obj=c.API_ITEM_CLS)


def expand_global(obj):
    """Replace str values with global vars recursively.

    Args:
        obj (:obj:`str` or :obj:`dict` or :obj:`list`):
            Object to expand into global var.

    Returns:
        :obj:`str` or :obj:`dict` or :obj:`list` or :obj:`object`:
            String objects are the only ones that will be expanded.

    """
    if isinstance(obj, string_types):
        if obj == "None":
            return None
        try:
            return globals()[obj]
        except Exception:
            return obj
    if isinstance(obj, dict):
        return {k: expand_global(obj=v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [expand_global(obj=v) for v in obj]
    return obj


def get_api_all_item():
    """Get map of class name to class for all ApiItem subclasses.

    Returns:
        :obj:`dict`

    """
    return {c.__name__: c for c in ApiItem.__subclasses__()}


def get_api_all_list():
    """Get map of class name to class for all ApiList subclasses.

    Returns:
        :obj:`dict`

    """
    return {c.__name__: c for c in ApiList.__subclasses__()}


def get_api_all_model():
    """Get map of class name to class for all ApiItem and ApiList subclasses.

    Returns:
        :obj:`dict`

    """
    return {c.__name__: c for c in ApiItem.__subclasses__() + ApiList.__subclasses__()}


class ApiModel(api_models.ApiModel):
    """Model for a complex item in the API."""

    pass


class ApiItem(ApiModel, api_models.ApiItem):
    """Model for a complex item in the API."""

    pass


class ApiList(ApiModel, api_models.ApiList):
    """Model for an array in the API."""

    pass


class ResultInfoList(ApiList):
    """Manually defined API array object."""

    API_NAME = "result_infos"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"now": "string_types", "max_available_age": "integer_types"}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = ["now", "max_available_age"]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "result_info"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ResultInfo"
    """:class:`ApiItem`: Item class this list class holds."""

    def __repr__(self):
        """Make repr output be same as str output.

        Returns:
            :obj:`str`

        """
        return self.__str__()


class ResultInfo(ApiItem):
    """Manually defined API object."""

    API_NAME = "result_info"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "age": "integer_types",
        "archived_question_id": "integer_types",
        "error_count": "integer_types",
        "estimated_total": "integer_types",
        "expire_seconds": "integer_types",
        "id": "integer_types",
        "issue_seconds": "integer_types",
        "mr_passed": "integer_types",
        "mr_tested": "integer_types",
        "no_results_count": "integer_types",
        "passed": "integer_types",
        "question_id": "integer_types",
        "report_count": "integer_types",
        "row_count": "integer_types",
        "row_count_flag": "integer_types",
        "row_count_machines": "integer_types",
        "saved_question_id": "integer_types",
        "seconds_since_issued": "integer_types",
        "select_count": "integer_types",
        "tested": "integer_types",
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = [
        "question_id",
        "estimated_total",
        "row_count",
        "mr_tested",
        "mr_passed",
    ]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ResultInfoList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "result_infos"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""

    def __repr__(self):
        """Make repr output be same as str output.

        Returns:
            :obj:`str`

        """
        return self.__str__()


class ResultSetList(ApiList):
    """Manually defined API array object."""

    API_NAME = "result_sets"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"now": "string_types"}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = ["now"]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "result_set"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ResultSet"
    """:class:`ApiItem`: Item class this list class holds."""


class MergedResultSet(ApiItem):
    """Manually defined API object."""

    API_NAME = "merged_result"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"now": "string_types", "max_available_age": "string_types"}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"result_infos": "ResultInfoList", "result_sets": "ResultSetList"}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = ["now", "max_available_age"]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = None
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ResultSet(ApiItem):
    """Manually defined API object."""

    API_NAME = "result_set"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "age": "integer_types",
        "archived_question_id": "integer_types",
        "cache_id": "integer_types",
        "error_count": "integer_types",
        "estimated_total": "integer_types",
        "expiration": "integer_types",
        "expire_seconds": "integer_types",
        "filtered_row_count": "integer_types",
        "filtered_row_count_machines": "integer_types",
        "id": "integer_types",
        "issue_seconds": "integer_types",
        "item_count": "integer_types",
        "mr_passed": "integer_types",
        "mr_tested": "integer_types",
        "no_results_count": "integer_types",
        "passed": "integer_types",
        "question_id": "integer_types",
        "report_count": "integer_types",
        "row_count": "integer_types",
        "row_count_machines": "integer_types",
        "saved_question_id": "integer_types",
        "seconds_since_issued": "integer_types",
        "select_count": "integer_types",
        "tested": "integer_types",
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cs": "ColumnList", "rs": "RowList"}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = [
        "question_id",
        "estimated_total",
        "mr_tested",
        "mr_passed",
        "row_count",
        "columns",
    ]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ResultSetList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "result_sets"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""

    def __init__(self, **kwargs):
        """Constructor.

        Notes:
            Sets :attr:`Column.API_DATA_SET` so column objects can access rows.

            Sets :attr:`RowColumn.API_COLUMN` to the index correlated :obj:`Column`
            so row columns can access the column name, result type, etc.

            Sets :attr:`Column.API_IDX` and :attr:`RowColumn.API_IDX` so column
            objects know what their index is without having to do lookups.

        Args:
            **kwargs:
                Passed back to parent class.

        """
        super(ResultSet, self).__init__(**kwargs)
        self.cs = ColumnList() if self.cs is None else self.cs
        self.rs = RowList() if self.rs is None else self.rs
        for row in self.rows:
            for idx, row_column in enumerate(row):
                row_column.API_COLUMN = self.columns[idx]
                row_column.API_IDX = idx
        for idx, column in enumerate(self.columns):
            column.API_DATA_SET = self
            column.API_IDX = idx

    @property
    def rows(self):
        """Expose complex attr "rs" as "rows".

        Returns:
            :obj:`list`

        """
        return self.rs

    @property
    def columns(self):
        """Expose complex attr "cs" as "columns".

        Returns:
            :obj:`list`

        """
        return self.cs


class ColumnList(ApiList):
    """Manually defined API array object."""

    API_NAME = "cs"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = ["names"]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "c"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Column"
    """:class:`ApiItem`: Item class this list class holds."""

    def __repr__(self):
        """Make repr output be same as str output.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    @property
    def names(self):
        """Expose column names of all :obj:`Column` in this obj.

        Returns:
            :obj:`list` of :obj:`str`

        """
        return [x.name for x in self]

    def __getitem__(self, value):
        """Support indexing of :attr:`names`.

        Args:
            value (:obj:`int` or :obj:`str`):
                If int: Index of item to retrieve from simple attr "c".
                If str: Column name to index correlate from :attr:`names`

        Returns:
            :attr:`RowColumn`:
                The RowColumn object at index value from :attr:`names`.

        """
        if isinstance(value, string_types):
            try:
                value = self.names.index(value)
            except ValueError:
                error = [
                    "Valid Column Names:",
                    "{vc}",
                    "{c!r} is an invalid column name in this data set",
                ]
                error = "\n  ".join(error)
                error = error.format(c=value, vc=self.names)
                raise exceptions.ModuleError(error)
        return self.LIST[value]


class Column(ApiItem):
    """Manually defined API object."""

    API_DATA_SET = None
    """:obj:`ResultSet`: Parent of this object, set by :meth:`ResultSet.__init__`."""

    API_IDX = None
    """:obj:`int`: Index of this object in :obj:`ColumnList`."""

    API_NAME = "c"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"dn": "string_types", "rt": "integer_types", "wh": "integer_types"}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = ["name", "result_type", "hash"]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ColumnList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "cs"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""

    @property
    def name(self):
        """Expose simple attr "dn" as name.

        Returns:
            :obj:`str`

        """
        return self.dn

    @property
    def hash(self):
        """Expose simple attr "wh" as hash.

        Returns:
            :obj:`str`

        """
        return self.wh

    @property
    def type(self):
        """Expose simple attr "rt" as type.

        Returns:
            :obj:`str`

        """
        return self.rt

    @property
    def result_type(self):
        """Expose simple attr "rt" as result_type.

        Notes:
            Will try to map str from "rt" as int to constants from
            :attr:`Sensor.API_CONSTANTS`.

        Returns:
            :obj:`str`

        """
        sensor = get_api_all_model()["Sensor"]
        constants = sensor.API_CONSTANTS.items()
        result_map = {v: k for k, v in constants if not k.lower().endswith("sensor")}
        result_type = self.api_coerce_int(self.type)
        return result_map.get(result_type, result_type)

    def get_values(self, attr="value", join=None):
        """Get values of this column from all rows.

        Args:
            attr (:obj:`str`, optional):
                Attribute to get values of.

                Defaults to: "value".
            join (:obj:`str`, optional):
                String to join multi value columns.

                Defaults to: None.

        Returns:
            :obj:`list` of :obj:`str`

        """
        values = []
        for row in self.API_DATA_SET.rows:
            row_column = row[self.API_IDX]
            row_column_values = row_column.get_values(attr=attr, join=join)
            values.append(row_column_values)
        return values


class RowList(ApiList):
    """Manually defined API array object."""

    API_NAME = "rs"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "r"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Row"
    """:class:`ApiItem`: Item class this list class holds."""

    def __repr__(self):
        """Make repr output be same as str output.

        Returns:
            :obj:`str`

        """
        return self.__str__()


class Row(ApiItem):
    """Manually defined API object."""

    API_NAME = "r"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"id": "integer_types", "cid": "integer_types"}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"c": "RowColumnList"}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = ["id", "cid", "columns"]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_API_NAME = "rs"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""

    API_LIST_CLS = "RowList"
    """:class:`ApiItem`: Item class this list class holds."""

    def __repr__(self):
        """Make repr output be same as str output.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    def __getitem__(self, value):
        """Support indexing of :attr:`names`.

        Args:
            value (:obj:`int` or :obj:`str`):
                If int: Index of item to retrieve from :attr:`names`.
                If str: Column name to index correlate from :attr:`ColumnList.names`

        Returns:
            :attr:`RowColumn`:
                The RowColumn object at index value from :attr:`names`.

        """
        if isinstance(value, string_types):
            try:
                value = self.names.index(value)
            except ValueError:
                error = [
                    "Valid Column Names:",
                    "{vc}",
                    "{c!r} is an invalid column name in this data set",
                ]
                error = "\n  ".join(error)
                error = error.format(c=value, vc=self.names)
                raise exceptions.ModuleError(error)
        return self.columns[value]

    @property
    def names(self):
        """Return the names of each row column from :attr:`RowColumn.API_COLUMN`.

        Returns:
            :obj:`list` of :obj:`str`

        """
        return [x.API_COLUMN.name for x in self.columns]

    @property
    def columns(self):
        """Expose complex attr "c" as "columns".

        Returns:
            :obj:`RowColumnList`

        """
        return self.c

    def __len__(self):
        """Expose length of :attr:`columns`.

        Returns:
            :obj:`int`

        """
        return len(self.columns)

    def get_values(self, meta=False, hashes=False, join=None):
        """Get all values from all columns in this row.

        Args:
            meta (:obj:`bool`, optional):
                Include sensor hash and result type for each column.

                Defaults to: False.

            hashes (:obj:`bool`, optional):
                Include hashes of values.

                Defaults to: False.
            join (:obj:`str`, optional):
                String to join multi value columns.

                Defaults to: None.

        Returns:
            :obj:`dict`

        """
        values = {}
        for idx, column in enumerate(self.columns):
            values[column.name] = column.get_values(attr="value", join=join)
            if hashes:
                key = "{} Hash Values".format(column.name)
                values[key] = column.get_values(attr="hash", join=join)
            if meta:
                key = "{} Sensor Hash".format(column.name)
                values[key] = column.hash
                key = "{} Result Type".format(column.name)
                values[key] = column.result_type
        return values


class RowColumnList(ApiList):
    """Manually defined API array object."""

    API_NAME = "rc"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "row_columns"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "RowColumn"
    """:class:`ApiItem`: Item class this list class holds."""

    def api_coerce_items_hook(self, attr, value, op):
        """Check hook that allows subclasses to modify list items.

        Args:
            attr (:obj:`str`):
                Attribute being set on this object.
            value (:obj:`ApiList` or :obj:`list` or :obj:`tuple`):
                The list object holding items.
            op (:obj:`str`):
                Operation being performed that called this method.

        Examples:
            This converts all "v" attributes of each column for this row into a
            list of dicts:

                >>> # single value columns "v" is a single dict:
                >>> {"v": {"h": "", "text": ""}}
                >>> # multiple value columns "v" is a list of dict:
                >>> {"v": [{"h": "", "text": ""}, {"h": "", "text": ""}]}
                >>> # Count columns "v" is a string:
                >>> {"v": "1"}
                >>> # all become:
                >>> {"v": [{"text": "", "hash": ""}]}

        Notes:
            The driving force behind this is basically just the Count column.
            It returns a string of the value, instead of a dict or a list of dicts.

        Returns:
            :obj:`list`:
                The list of items modified or as is.

        """
        if not isinstance(value, (list, tuple)):
            error = "{value} is not a list"
            error = error.format(value=value)
            raise exceptions.ModuleError(error)

        new_value = []
        for item in value:
            if not isinstance(item, dict):
                error = "Item {item} in {value} is not a dict"
                error = error.format(item=item, value=value)
                raise exceptions.ModuleError(error)

            item_v = item["v"]
            if isinstance(item_v, (tuple, list)):
                new_item_value = []
                for item_value in item_v:
                    is_simple = isinstance(item_value, simple_types)
                    is_none = item_value is None
                    item_value = (
                        {"text": item_value, "h": None} if is_simple else item_value
                    )

                    item_value = {"text": "", "h": None} if is_none else item_value

                    if not isinstance(item_value, dict):
                        error = "Item value '{item_value}' in {item} is not a dict"
                        error = error.format(item_value=item_value, item=item["v"])
                        raise exceptions.ModuleError(error)

                    new_item_value.append(item_value)
                item_v = new_item_value

            is_none = item_v is None
            is_simple = isinstance(item_v, simple_types)
            item_v = [{"text": "", "h": None}] if is_none else item_v
            item_v = [{"text": item["v"], "h": None}] if is_simple else item_v
            item_v = self.api_coerce_list(item_v)
            item["v"] = item_v
            new_value.append(item)
        return new_value


'''
# older version of hook, it didn't work right :)
    def api_coerce_items_hook(self, attr, value, op):
        """Check hook that allows subclasses to modify list items.

        Args:
            attr (:obj:`str`):
                Attribute being set on this object.
            value (:obj:`ApiList` or :obj:`list` or :obj:`tuple`):
                The list object holding items.
            op (:obj:`str`):
                Operation being performed that called this method.

        Examples:
            This converts all "v" attributes of each column for this row into a
            list of dicts:

                >>> # single value columns "v" is a single dict:
                >>> {"v": {"h": "", "text": ""}}
                >>> # multiple value columns "v" is a list of dict:
                >>> {"v": [{"h": "", "text": ""}, {"h": "", "text": ""}]}
                >>> # Count columns "v" is a string:
                >>> {"v": "1"}
                >>> # all become:
                >>> {"v": [{"text": "", "hash": ""}]}

        Notes:
            The driving force behind this is basically just the Count column.
            It returns a string of the value, instead of a dict or a list of dicts.

        Returns:
            :obj:`list`:
                The list of items modified or as is.

        """
        items = []
        for item in value:
            do_fix = isinstance(item, dict) and isinstance(item["v"], string_types)
            item["v"] = {"text": item["v"], "h": None} if do_fix else item["v"]
            item["v"] = self.api_coerce_list(item["v"])
            items.append(item)
        return items
'''


class RowColumn(ApiList):
    """Manually defined API array object."""

    API_COLUMN = None
    """:obj:`Column`: Index correlated column, set by :meth:`ResultSet.__init__`."""

    API_IDX = None
    """:obj:`int`: Index of this object in :obj:`RowColumnList`."""

    API_NAME = "row_column"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = ["name", "hash", "result_type"]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "v"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "RowValue"
    """:class:`ApiItem`: Item class this list class holds."""

    @property
    def name(self):
        """Expose column name from :attr:`API_COLUMN`.

        Returns:
            :obj:`str`

        """
        return self.API_COLUMN.name

    @property
    def result_type(self):
        """Expose column result type from :attr:`API_COLUMN`.

        Returns:
            :obj:`str`

        """
        return self.API_COLUMN.result_type

    @property
    def hash(self):
        """Expose column sensor hash from :attr:`API_COLUMN`.

        Returns:
            :obj:`str`

        """
        return self.API_COLUMN.hash

    def get_values(self, attr="value", join=None):
        """Get all values from this row column.

        Args:
            attr (:obj:`str`, optional):
                Attribute to get values of.

                Defaults to: "value".
            join (:obj:`str`, optional):
                String to join multi value columns.

                Defaults to: None.

        Returns:
            :obj:`list` or :obj:`str`

        """
        values = []
        for row_value in self:
            value = getattr(row_value, attr)
            values.append("" if value is None else value)

        if join:
            values = join.join([format(v) for v in values])
        return values


class RowValue(ApiItem):
    """Manually defined API object."""

    API_NAME = "v"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = ""
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"h": "integer_types", "text": "simple_types"}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = ["hash", "value"]
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "RowColumn"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "row_column"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""

    @property
    def hash(self):
        """Expose simple attr "h" as hash.

        Returns:
            :obj:`str`

        """
        return self.h

    @property
    def value(self):
        """Expose simple attr "text" as value.

        Returns:
            :obj:`str`

        """
        return self.text
