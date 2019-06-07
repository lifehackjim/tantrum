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


class SensorQuery(ApiItem):
    """Automagically generated API object."""

    API_NAME = "sensor_query"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_query"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "platform": "string_types",  # noqa: E501
        "script": "string_types",  # noqa: E501
        "script_type": "string_types",  # noqa: E501
        "signature": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SensorQueryList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "sensor_querys"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SensorSubcolumn(ApiItem):
    """Automagically generated API object."""

    API_NAME = "sensor_subcolumn"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_subcolumn"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "name": "string_types",  # noqa: E501
        "index": "integer_types",  # noqa: E501
        "value_type": "string_types",  # noqa: E501
        "ignore_case_flag": "integer_types",  # noqa: E501
        "hidden_flag": "integer_types",  # noqa: E501
        "exclude_from_parse_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SensorSubcolumnList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "sensor_subcolumns"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SensorStat(ApiItem):
    """Automagically generated API object."""

    API_NAME = "sensor_stat"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_stat"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "what_hash": "integer_types",  # noqa: E501
        "count": "integer_types",  # noqa: E501
        "real_ms_min": "float_types",  # noqa: E501
        "real_ms_max": "float_types",  # noqa: E501
        "real_ms_avg": "float_types",  # noqa: E501
        "real_ms_std": "float_types",  # noqa: E501
        "user_ms_avg": "float_types",  # noqa: E501
        "user_ms_std": "float_types",  # noqa: E501
        "sys_ms_avg": "float_types",  # noqa: E501
        "sys_ms_std": "float_types",  # noqa: E501
        "read_bytes_avg": "float_types",  # noqa: E501
        "read_bytes_std": "float_types",  # noqa: E501
        "write_bytes_avg": "float_types",  # noqa: E501
        "write_bytes_std": "float_types",  # noqa: E501
        "other_bytes_avg": "float_types",  # noqa: E501
        "other_bytes_std": "float_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SensorStatList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "sensor_stats"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SavedActionPolicy(ApiItem):
    """Automagically generated API object."""

    API_NAME = "saved_action_policy"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_action_policy"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "saved_question_id": "integer_types",  # noqa: E501
        "saved_question_group_id": "integer_types",  # noqa: E501
        "row_filter_group_id": "integer_types",  # noqa: E501
        "max_age": "integer_types",  # noqa: E501
        "min_count": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "saved_question_group": "Group",  # noqa: E501
        "row_filter_group": "Group",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SavedActionApproval(ApiItem):
    """Automagically generated API object."""

    API_NAME = "saved_action_approval"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_action_approval"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "owner_user_id": "integer_types",  # noqa: E501
        "approved_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"metadata": "MetadataList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SavedActionApprovalList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "saved_action_approvals"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SavedAction(ApiItem):
    """Automagically generated API object."""

    API_NAME = "saved_action"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_action"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "comment": "string_types",  # noqa: E501
        "status": "integer_types",  # noqa: E501
        "issue_seconds": "integer_types",  # noqa: E501
        "distribute_seconds": "integer_types",  # noqa: E501
        "start_time": "string_types",  # noqa: E501
        "end_time": "string_types",  # noqa: E501
        "action_group_id": "integer_types",  # noqa: E501
        "public_flag": "integer_types",  # noqa: E501
        "policy_flag": "integer_types",  # noqa: E501
        "expire_seconds": "integer_types",  # noqa: E501
        "approved_flag": "integer_types",  # noqa: E501
        "issue_count": "integer_types",  # noqa: E501
        "creation_time": "string_types",  # noqa: E501
        "next_start_time": "string_types",  # noqa: E501
        "last_start_time": "string_types",  # noqa: E501
        "user_start_time": "string_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "package_spec": "PackageSpec",  # noqa: E501
        "action_group": "Group",  # noqa: E501
        "target_group": "Group",  # noqa: E501
        "policy": "SavedActionPolicy",  # noqa: E501
        "metadata": "MetadataList",  # noqa: E501
        "row_ids": "SavedActionRowIdList",  # noqa: E501
        "user": "User",  # noqa: E501
        "approver": "User",  # noqa: E501
        "last_action": "Action",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SavedActionList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "saved_actions"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Sensor(ApiItem):
    """Automagically generated API object."""

    API_NAME = "sensor"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "hash": "integer_types",  # noqa: E501
        "string_count": "integer_types",  # noqa: E501
        "category": "string_types",  # noqa: E501
        "description": "string_types",  # noqa: E501
        "source_id": "integer_types",  # noqa: E501
        "source_hash": "integer_types",  # noqa: E501
        "source_name": "string_types",  # noqa: E501
        "parameter_definition": "string_types",  # noqa: E501
        "value_type": "string_types",  # noqa: E501
        "max_age_seconds": "integer_types",  # noqa: E501
        "ignore_case_flag": "integer_types",  # noqa: E501
        "exclude_from_parse_flag": "integer_types",  # noqa: E501
        "delimiter": "string_types",  # noqa: E501
        "creation_time": "string_types",  # noqa: E501
        "modification_time": "string_types",  # noqa: E501
        "last_modified_by": "string_types",  # noqa: E501
        "preview_sensor_flag": "integer_types",  # noqa: E501
        "hidden_flag": "integer_types",  # noqa: E501
        "keep_duplicates_flag": "integer_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "content_set": "IdReference",  # noqa: E501
        "queries": "SensorQueryList",  # noqa: E501
        "parameters": "ParameterList",  # noqa: E501
        "subcolumns": "SensorSubcolumnList",  # noqa: E501
        "mod_user": "User",  # noqa: E501
        "string_hints": "StringHintList",  # noqa: E501
        "metadata": "MetadataList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {
        "WMI_SENSOR": 1,
        "BES_SENSOR": 2,
        "VBS_SENSOR": 4,
        "PSHELL_SENSOR": 5,
        "MULTITYPE_SENSOR": 6,
        "JS_SENSOR": 7,
        "PY_SENSOR": 8,
        "HASH_RESULT": 0,
        "TEXT_RESULT": 1,
        "VERSION_RESULT": 2,
        "NUMERIC_RESULT": 3,
        "BES_DATETIME_RESULT": 4,
        "IP_RESULT": 5,
        "WMI_DATETIME_RESULT": 6,
        "TIMEDIFF_REUSLT": 7,
        "DATASIZE_RESULT": 8,
        "NUMERIC_INTEGER_RESULT": 9,
        "REGEX_RESULT": 11,
    }
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SensorList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "sensors"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class AuditData(ApiItem):
    """Automagically generated API object."""

    API_NAME = "audit_data"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "audit_data"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "object_id": "integer_types",  # noqa: E501
        "details": "string_types",  # noqa: E501
        "creation_time": "string_types",  # noqa: E501
        "modification_time": "string_types",  # noqa: E501
        "last_modified_by": "string_types",  # noqa: E501
        "modifier_user_id": "integer_types",  # noqa: E501
        "type": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"mod_user": "User"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "AuditDataList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "audit_datas"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class AuditLog(ApiItem):
    """Automagically generated API object."""

    API_NAME = "audit_log"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "audit_log"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "type": "string_types",  # noqa: E501
        "start_time": "string_types",  # noqa: E501
        "end_time": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"entries": "AuditDataList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "AuditLogList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "audit_logs"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Server(ApiItem):
    """Automagically generated API object."""

    API_NAME = "server"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "server"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "heart_beat": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ServerList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "servers"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class MetadataItem(ApiItem):
    """Automagically generated API object."""

    API_NAME = "metadata_item"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "metadata_item"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "name": "string_types",  # noqa: E501
        "value": "string_types",  # noqa: E501
        "admin_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "MetadataList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "metadatas"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Filter(ApiItem):
    """Automagically generated API object."""

    API_NAME = "filter"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "filter"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "operator": "string_types",  # noqa: E501
        "value_type": "string_types",  # noqa: E501
        "value": "string_types",  # noqa: E501
        "not_flag": "integer_types",  # noqa: E501
        "max_age_seconds": "integer_types",  # noqa: E501
        "ignore_case_flag": "integer_types",  # noqa: E501
        "all_values_flag": "integer_types",  # noqa: E501
        "substring_flag": "integer_types",  # noqa: E501
        "substring_start": "integer_types",  # noqa: E501
        "substring_length": "integer_types",  # noqa: E501
        "delimiter": "string_types",  # noqa: E501
        "delimiter_index": "integer_types",  # noqa: E501
        "utf8_flag": "integer_types",  # noqa: E501
        "aggregation": "string_types",  # noqa: E501
        "all_times_flag": "integer_types",  # noqa: E501
        "start_time": "string_types",  # noqa: E501
        "end_time": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"sensor": "Sensor"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "FilterList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "filters"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class IdReference(ApiItem):
    """Automagically generated API object."""

    API_NAME = "id_reference"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "id_reference"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Group(ApiItem):
    """Automagically generated API object."""

    API_NAME = "group"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "group"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "text": "string_types",  # noqa: E501
        "and_flag": "integer_types",  # noqa: E501
        "not_flag": "integer_types",  # noqa: E501
        "type": "integer_types",  # noqa: E501
        "source_id": "integer_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
        "track_computer_id_flag": "integer_types",  # noqa: E501
        "track_computer_id_interval": "integer_types",  # noqa: E501
        "saved_question_id": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "sub_groups": "GroupList",  # noqa: E501
        "filters": "FilterList",  # noqa: E501
        "parameters": "ParameterList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "GroupList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "groups"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Select(ApiItem):
    """Automagically generated API object."""

    API_NAME = "select"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "select"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "sensor": "Sensor",  # noqa: E501
        "filter": "Filter",  # noqa: E501
        "group": "Group",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SelectList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "selects"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class XmlError(ApiItem):
    """Automagically generated API object."""

    API_NAME = "xml_error"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "xml_error"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "type": "string_types",  # noqa: E501
        "exception": "string_types",  # noqa: E501
        "error_context": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ErrorList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "errors"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class CacheInfo(ApiItem):
    """Automagically generated API object."""

    API_NAME = "cache_info"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "cache_info"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "cache_id": "integer_types",  # noqa: E501
        "page_row_count": "integer_types",  # noqa: E501
        "filtered_row_count": "integer_types",  # noqa: E501
        "cache_row_count": "integer_types",  # noqa: E501
        "expiration": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"errors": "ErrorList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class QuestionListInfo(ApiItem):
    """Automagically generated API object."""

    API_NAME = "question_list_info"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "question_list_info"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "highest_id": "integer_types",  # noqa: E501
        "total_count": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Question(ApiItem):
    """Automagically generated API object."""

    API_NAME = "question"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "question"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "expire_seconds": "integer_types",  # noqa: E501
        "skip_lock_flag": "integer_types",  # noqa: E501
        "expiration": "string_types",  # noqa: E501
        "is_expired": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "query_text": "string_types",  # noqa: E501
        "hidden_flag": "integer_types",  # noqa: E501
        "action_tracking_flag": "integer_types",  # noqa: E501
        "force_computer_id_flag": "integer_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
        "index": "integer_types",  # noqa: E501
        "from_canonical_text": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "selects": "SelectList",  # noqa: E501
        "context_group": "Group",  # noqa: E501
        "group": "Group",  # noqa: E501
        "user": "User",  # noqa: E501
        "management_rights_group": "Group",  # noqa: E501
        "saved_question": "SavedQuestion",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "QuestionList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "questions"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class PackageFileTemplate(ApiItem):
    """Automagically generated API object."""

    API_NAME = "package_file_template"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "package_file_template"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "hash": "string_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "source": "string_types",  # noqa: E501
        "download_seconds": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "PackageFileTemplateList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "package_file_templates"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class PackageFileStatus(ApiItem):
    """Automagically generated API object."""

    API_NAME = "package_file_status"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "package_file_status"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "server_id": "integer_types",  # noqa: E501
        "server_name": "string_types",  # noqa: E501
        "status": "integer_types",  # noqa: E501
        "cache_status": "string_types",  # noqa: E501
        "cache_message": "string_types",  # noqa: E501
        "bytes_downloaded": "integer_types",  # noqa: E501
        "bytes_total": "integer_types",  # noqa: E501
        "download_start_time": "string_types",  # noqa: E501
        "last_download_progress_time": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "PackageFileStatusList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "package_file_statuss"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class PackageFile(ApiItem):
    """Automagically generated API object."""

    API_NAME = "package_file"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "package_file"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "hash": "string_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "size": "integer_types",  # noqa: E501
        "source": "string_types",  # noqa: E501
        "download_seconds": "integer_types",  # noqa: E501
        "trigger_download": "integer_types",  # noqa: E501
        "cache_status": "string_types",  # noqa: E501
        "status": "integer_types",  # noqa: E501
        "bytes_downloaded": "integer_types",  # noqa: E501
        "bytes_total": "integer_types",  # noqa: E501
        "download_start_time": "string_types",  # noqa: E501
        "last_download_progress_time": "string_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"file_status": "PackageFileStatusList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "PackageFileList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "package_files"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class PackageSpec(ApiItem):
    """Automagically generated API object."""

    API_NAME = "package_spec"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "package_spec"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "display_name": "string_types",  # noqa: E501
        "command": "string_types",  # noqa: E501
        "command_timeout": "integer_types",  # noqa: E501
        "expire_seconds": "integer_types",  # noqa: E501
        "hidden_flag": "integer_types",  # noqa: E501
        "process_group_flag": "integer_types",  # noqa: E501
        "signature": "string_types",  # noqa: E501
        "source_id": "integer_types",  # noqa: E501
        "source_name": "string_types",  # noqa: E501
        "source_hash": "string_types",  # noqa: E501
        "source_hash_changed_flag": "integer_types",  # noqa: E501
        "verify_group_id": "integer_types",  # noqa: E501
        "verify_expire_seconds": "integer_types",  # noqa: E501
        "skip_lock_flag": "integer_types",  # noqa: E501
        "parameter_definition": "string_types",  # noqa: E501
        "creation_time": "string_types",  # noqa: E501
        "modification_time": "string_types",  # noqa: E501
        "last_modified_by": "string_types",  # noqa: E501
        "available_time": "string_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
        "last_update": "string_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "content_set": "IdReference",  # noqa: E501
        "files": "PackageFileList",  # noqa: E501
        "file_templates": "PackageFileTemplateList",  # noqa: E501
        "verify_group": "Group",  # noqa: E501
        "parameters": "ParameterList",  # noqa: E501
        "sensors": "SensorList",  # noqa: E501
        "mod_user": "User",  # noqa: E501
        "metadata": "MetadataList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "PackageSpecList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "package_specs"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ClientStatus(ApiItem):
    """Automagically generated API object."""

    API_NAME = "client_status"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "client_status"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "host_name": "string_types",  # noqa: E501
        "computer_id": "string_types",  # noqa: E501
        "ipaddress_client": "string_types",  # noqa: E501
        "ipaddress_server": "string_types",  # noqa: E501
        "protocol_version": "integer_types",  # noqa: E501
        "full_version": "string_types",  # noqa: E501
        "last_registration": "string_types",  # noqa: E501
        "send_state": "string_types",  # noqa: E501
        "receive_state": "string_types",  # noqa: E501
        "status": "string_types",  # noqa: E501
        "port_number": "integer_types",  # noqa: E501
        "public_key_valid": "integer_types",  # noqa: E501
        "registered_with_tls": "integer_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SystemStatusList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "system_status"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SystemSetting(ApiItem):
    """Automagically generated API object."""

    API_NAME = "system_setting"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "system_setting"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "value": "string_types",  # noqa: E501
        "default_value": "string_types",  # noqa: E501
        "value_type": "string_types",  # noqa: E501
        "setting_type": "string_types",  # noqa: E501
        "hidden_flag": "integer_types",  # noqa: E501
        "read_only_flag": "integer_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "audit_data": "AuditData",  # noqa: E501
        "metadata": "MetadataList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SystemSettingList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "system_settings"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SoapError(ApiItem):
    """Automagically generated API object."""

    API_NAME = "soap_error"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "soap_error"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "object_name": "string_types",  # noqa: E501
        "exception_name": "string_types",  # noqa: E501
        "context": "string_types",  # noqa: E501
        "object_request": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class WhiteListedUrl(ApiItem):
    """Automagically generated API object."""

    API_NAME = "white_listed_url"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "white_listed_url"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "chunk_id": "string_types",  # noqa: E501
        "download_seconds": "integer_types",  # noqa: E501
        "expire_seconds": "integer_types",  # noqa: E501
        "url_regex": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"metadata": "MetadataList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "WhiteListedUrlList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "white_listed_urls"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class VersionAggregate(ApiItem):
    """Automagically generated API object."""

    API_NAME = "version_aggregate"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "version_aggregate"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "version_string": "string_types",  # noqa: E501
        "count": "integer_types",  # noqa: E501
        "filtered": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "VersionAggregateList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "version_aggregates"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SystemStatusAggregate(ApiItem):
    """Automagically generated API object."""

    API_NAME = "system_status_aggregate"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "system_status_aggregate"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "send_forward_count": "integer_types",  # noqa: E501
        "send_backward_count": "integer_types",  # noqa: E501
        "send_none_count": "integer_types",  # noqa: E501
        "send_ok_count": "integer_types",  # noqa: E501
        "receive_forward_count": "integer_types",  # noqa: E501
        "receive_backward_count": "integer_types",  # noqa: E501
        "receive_none_count": "integer_types",  # noqa: E501
        "receive_ok_count": "integer_types",  # noqa: E501
        "slowlink_count": "integer_types",  # noqa: E501
        "blocked_count": "integer_types",  # noqa: E501
        "leader_count": "integer_types",  # noqa: E501
        "normal_count": "integer_types",  # noqa: E501
        "registered_with_tls_count": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"versions": "VersionAggregateList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class UserRole(ApiItem):
    """Automagically generated API object."""

    API_NAME = "user_role"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "user_role"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "description": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"permissions": "PermissionList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "UserRoleList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "roles"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class UserOwnedObjectIds(ApiItem):
    """Automagically generated API object."""

    API_NAME = "user_owned_object_ids"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "user_owned_object_ids"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "saved_actions": "SavedActionList",  # noqa: E501
        "saved_questions": "SavedQuestionList",  # noqa: E501
        "plugin_schedules": "PluginScheduleList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class User(ApiItem):
    """Automagically generated API object."""

    API_NAME = "user"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "user"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "domain": "string_types",  # noqa: E501
        "display_name": "string_types",  # noqa: E501
        "group_id": "integer_types",  # noqa: E501
        "effective_group_id": "integer_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
        "last_login": "string_types",  # noqa: E501
        "active_session_count": "integer_types",  # noqa: E501
        "local_admin_flag": "integer_types",  # noqa: E501
        "locked_out": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "permissions": "PermissionList",  # noqa: E501
        "roles": "UserRoleList",  # noqa: E501
        "metadata": "MetadataList",  # noqa: E501
        "content_set_roles": "ContentSetRoleList",  # noqa: E501
        "effective_content_set_privileges": "EffectiveContentSetPrivilegeList",  # noqa: E501
        "owned_object_ids": "UserOwnedObjectIds",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "UserList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "users"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ActionListInfo(ApiItem):
    """Automagically generated API object."""

    API_NAME = "action_list_info"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "action_list_info"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "highest_id": "integer_types",  # noqa: E501
        "total_count": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Action(ApiItem):
    """Automagically generated API object."""

    API_NAME = "action"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "action"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "comment": "string_types",  # noqa: E501
        "start_time": "string_types",  # noqa: E501
        "expiration_time": "string_types",  # noqa: E501
        "status": "string_types",  # noqa: E501
        "skip_lock_flag": "integer_types",  # noqa: E501
        "expire_seconds": "integer_types",  # noqa: E501
        "distribute_seconds": "integer_types",  # noqa: E501
        "creation_time": "string_types",  # noqa: E501
        "stopped_flag": "integer_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "target_group": "Group",  # noqa: E501
        "action_group": "Group",  # noqa: E501
        "package_spec": "PackageSpec",  # noqa: E501
        "user": "User",  # noqa: E501
        "approver": "User",  # noqa: E501
        "history_saved_question": "SavedQuestion",  # noqa: E501
        "saved_action": "SavedAction",  # noqa: E501
        "metadata": "MetadataList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ActionList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "actions"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ActionStop(ApiItem):
    """Automagically generated API object."""

    API_NAME = "action_stop"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "action_stop"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"id": "integer_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"action": "Action"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ActionStopList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "action_stops"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ArchivedQuestion(ApiItem):
    """Automagically generated API object."""

    API_NAME = "archived_question"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "archived_question"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"id": "integer_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ArchivedQuestionList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "archived_questions"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SavedQuestion(ApiItem):
    """Automagically generated API object."""

    API_NAME = "saved_question"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_question"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "seeding_question_ids": "string_types",  # noqa: E501
        "public_flag": "integer_types",  # noqa: E501
        "hidden_flag": "integer_types",  # noqa: E501
        "issue_seconds": "integer_types",  # noqa: E501
        "issue_seconds_never_flag": "integer_types",  # noqa: E501
        "expire_seconds": "integer_types",  # noqa: E501
        "sort_column": "integer_types",  # noqa: E501
        "query_text": "string_types",  # noqa: E501
        "row_count_flag": "integer_types",  # noqa: E501
        "keep_seconds": "integer_types",  # noqa: E501
        "archive_enabled_flag": "integer_types",  # noqa: E501
        "skip_schedule_on_update_flag": "integer_types",  # noqa: E501
        "most_recent_question_id": "integer_types",  # noqa: E501
        "action_tracking_flag": "integer_types",  # noqa: E501
        "mod_time": "string_types",  # noqa: E501
        "index": "integer_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "content_set": "IdReference",  # noqa: E501
        "question": "Question",  # noqa: E501
        "packages": "PackageSpecList",  # noqa: E501
        "user": "User",  # noqa: E501
        "archive_owner": "User",  # noqa: E501
        "mod_user": "User",  # noqa: E501
        "metadata": "MetadataList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SavedQuestionList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "saved_questions"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ParseJob(ApiItem):
    """Automagically generated API object."""

    API_NAME = "parse_job"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parse_job"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "question_text": "string_types",  # noqa: E501
        "parser_version": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ParseJobList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "parse_jobs"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Parameter(ApiItem):
    """Automagically generated API object."""

    API_NAME = "parameter"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parameter"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "key": "string_types",  # noqa: E501
        "value": "string_types",  # noqa: E501
        "type": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ParameterList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "parameters"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ParseResult(ApiItem):
    """Automagically generated API object."""

    API_NAME = "parse_result"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parse_result"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "parameter_definition": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"parameters": "ParameterList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ParseResultList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "parse_results"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SensorReference(ApiItem):
    """Automagically generated API object."""

    API_NAME = "sensor_reference"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_reference"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "name": "string_types",  # noqa: E501
        "start_char": "integer_types",  # noqa: E501
        "real_ms_avg": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SensorReferenceList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "sensor_references"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ParseResultGroup(ApiItem):
    """Automagically generated API object."""

    API_NAME = "parse_result_group"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parse_result_group"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "score": "integer_types",  # noqa: E501
        "question_text": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "parse_results": "ParseResultList",  # noqa: E501
        "question": "Question",  # noqa: E501
        "question_group_sensors": "SensorList",  # noqa: E501
        "parameter_values": "ParameterValueList",  # noqa: E501
        "sensor_references": "SensorReferenceList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ParseResultGroupList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "parse_result_groups"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ClientCount(ApiItem):
    """Automagically generated API object."""

    API_NAME = "client_count"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "client_count"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"count": "integer_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class PluginArgument(ApiItem):
    """Automagically generated API object."""

    API_NAME = "plugin_argument"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_argument"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "name": "string_types",  # noqa: E501
        "type": "string_types",  # noqa: E501
        "value": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "PluginArgumentList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "plugin_arguments"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class UploadFile(ApiItem):
    """Automagically generated API object."""

    API_NAME = "upload_file"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "upload_file"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "key": "string_types",  # noqa: E501
        "destination_file": "string_types",  # noqa: E501
        "hash": "string_types",  # noqa: E501
        "force_overwrite": "integer_types",  # noqa: E501
        "file_size": "integer_types",  # noqa: E501
        "start_pos": "integer_types",  # noqa: E501
        "bytes": "string_types",  # noqa: E501
        "file_cached": "integer_types",  # noqa: E501
        "part_size": "integer_types",  # noqa: E501
        "percent_complete": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "UploadFileList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "upload_files"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class UploadFileStatus(ApiItem):
    """Automagically generated API object."""

    API_NAME = "upload_file_status"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "upload_file_status"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "hash": "string_types",  # noqa: E501
        "percent_complete": "integer_types",  # noqa: E501
        "file_cached": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"file_parts": "UploadFileList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Plugin(ApiItem):
    """Automagically generated API object."""

    API_NAME = "plugin"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "name": "string_types",  # noqa: E501
        "bundle": "string_types",  # noqa: E501
        "plugin_server": "string_types",  # noqa: E501
        "input": "string_types",  # noqa: E501
        "script_response": "string_types",  # noqa: E501
        "exit_code": "integer_types",  # noqa: E501
        "type": "string_types",  # noqa: E501
        "path": "string_types",  # noqa: E501
        "filename": "string_types",  # noqa: E501
        "plugin_url": "string_types",  # noqa: E501
        "run_detached_flag": "integer_types",  # noqa: E501
        "execution_id": "integer_types",  # noqa: E501
        "timeout_seconds": "integer_types",  # noqa: E501
        "cache_row_id": "integer_types",  # noqa: E501
        "local_admin_flag": "integer_types",  # noqa: E501
        "allow_rest": "integer_types",  # noqa: E501
        "raw_http_response": "integer_types",  # noqa: E501
        "raw_http_request": "integer_types",  # noqa: E501
        "use_json_flag": "integer_types",  # noqa: E501
        "status": "string_types",  # noqa: E501
        "status_file_content": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "arguments": "PluginArgumentList",  # noqa: E501
        "sql_response": "PluginSql",  # noqa: E501
        "metadata": "MetadataList",  # noqa: E501
        "commands": "PluginCommandList",  # noqa: E501
        "permissions": "PermissionList",  # noqa: E501
        "content_set": "ContentSet",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {"SQL": "SQL", "SCRIPT": "Script"}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "PluginList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "plugins"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class PluginSchedule(ApiItem):
    """Automagically generated API object."""

    API_NAME = "plugin_schedule"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_schedule"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "plugin_name": "string_types",  # noqa: E501
        "plugin_bundle": "string_types",  # noqa: E501
        "plugin_server": "string_types",  # noqa: E501
        "start_hour": "integer_types",  # noqa: E501
        "end_hour": "integer_types",  # noqa: E501
        "start_date": "string_types",  # noqa: E501
        "end_date": "string_types",  # noqa: E501
        "run_on_days": "string_types",  # noqa: E501
        "run_interval_seconds": "integer_types",  # noqa: E501
        "enabled": "integer_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
        "input": "string_types",  # noqa: E501
        "last_run_time": "string_types",  # noqa: E501
        "last_exit_code": "integer_types",  # noqa: E501
        "last_run_text": "string_types",  # noqa: E501
        "modification_time": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "arguments": "PluginArgumentList",  # noqa: E501
        "user": "User",  # noqa: E501
        "last_run_sql": "PluginSql",  # noqa: E501
        "mod_user": "User",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "PluginScheduleList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "plugin_schedules"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ComputerGroupSpec(ApiItem):
    """Automagically generated API object."""

    API_NAME = "computer_group_spec"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "computer_group_spec"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "computer_name": "string_types",  # noqa: E501
        "ip_address": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ComputerSpecList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "computer_specs"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ComputerGroup(ApiItem):
    """Automagically generated API object."""

    API_NAME = "computer_group"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "computer_group"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"computer_specs": "ComputerSpecList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ComputerGroupList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "computer_groups"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class VerifySignature(ApiItem):
    """Automagically generated API object."""

    API_NAME = "verify_signature"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "verify_signature"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "type": "string_types",  # noqa: E501
        "bytes": "string_types",  # noqa: E501
        "verified": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ObjectList(ApiItem):
    """Automagically generated API object."""

    API_NAME = "object_list"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "object_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "export_id": "string_types",  # noqa: E501
        "server_info": "string_types",  # noqa: E501
        "import_content": "string_types",  # noqa: E501
        "export_version": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "question": "Question",  # noqa: E501
        "questions": "QuestionList",  # noqa: E501
        "group": "Group",  # noqa: E501
        "groups": "GroupList",  # noqa: E501
        "saved_question": "SavedQuestion",  # noqa: E501
        "saved_questions": "SavedQuestionList",  # noqa: E501
        "archived_question": "ArchivedQuestion",  # noqa: E501
        "archived_questions": "ArchivedQuestionList",  # noqa: E501
        "parse_job": "ParseJob",  # noqa: E501
        "parse_jobs": "ParseJobList",  # noqa: E501
        "parse_result_group": "ParseResultGroup",  # noqa: E501
        "parse_result_groups": "ParseResultGroupList",  # noqa: E501
        "action": "Action",  # noqa: E501
        "actions": "ActionList",  # noqa: E501
        "saved_action": "SavedAction",  # noqa: E501
        "saved_actions": "SavedActionList",  # noqa: E501
        "action_stop": "ActionStop",  # noqa: E501
        "action_stops": "ActionStopList",  # noqa: E501
        "package_spec": "PackageSpec",  # noqa: E501
        "package_specs": "PackageSpecList",  # noqa: E501
        "package_file": "PackageFile",  # noqa: E501
        "package_files": "PackageFileList",  # noqa: E501
        "sensor": "Sensor",  # noqa: E501
        "sensors": "SensorList",  # noqa: E501
        "user": "User",  # noqa: E501
        "users": "UserList",  # noqa: E501
        "user_group": "UserGroup",  # noqa: E501
        "user_groups": "UserGroupList",  # noqa: E501
        "solution": "Solution",  # noqa: E501
        "solutions": "SolutionList",  # noqa: E501
        "action_group": "ActionGroup",  # noqa: E501
        "action_groups": "ActionGroupList",  # noqa: E501
        "roles": "UserRoleList",  # noqa: E501
        "client_status": "ClientStatus",  # noqa: E501
        "system_setting": "SystemSetting",  # noqa: E501
        "saved_action_approval": "SavedActionApproval",  # noqa: E501
        "saved_action_approvals": "SavedActionApprovalList",  # noqa: E501
        "system_status": "SystemStatusList",  # noqa: E501
        "system_settings": "SystemSettingList",  # noqa: E501
        "client_count": "ClientCount",  # noqa: E501
        "plugin": "Plugin",  # noqa: E501
        "plugins": "PluginList",  # noqa: E501
        "plugin_schedule": "PluginSchedule",  # noqa: E501
        "plugin_schedules": "PluginScheduleList",  # noqa: E501
        "white_listed_url": "WhiteListedUrl",  # noqa: E501
        "white_listed_urls": "WhiteListedUrlList",  # noqa: E501
        "upload_file": "UploadFile",  # noqa: E501
        "upload_file_status": "UploadFileStatus",  # noqa: E501
        "sensor_stat": "SensorStat",  # noqa: E501
        "sensor_stats": "SensorStatList",  # noqa: E501
        "soap_error": "SoapError",  # noqa: E501
        "computer_groups": "ComputerGroupList",  # noqa: E501
        "computer_group": "ComputerGroup",  # noqa: E501
        "content_set": "ContentSet",  # noqa: E501
        "content_sets": "ContentSetList",  # noqa: E501
        "content_set_privilege": "ContentSetPrivilege",  # noqa: E501
        "content_set_privileges": "ContentSetPrivilegeList",  # noqa: E501
        "content_set_role": "ContentSetRole",  # noqa: E501
        "content_set_roles": "ContentSetRoleList",  # noqa: E501
        "content_set_role_membership": "ContentSetRoleMembership",  # noqa: E501
        "content_set_role_memberships": "ContentSetRoleMembershipList",  # noqa: E501
        "content_set_role_privilege": "ContentSetRolePrivilege",  # noqa: E501
        "content_set_role_privileges": "ContentSetRolePrivilegeList",  # noqa: E501
        "content_set_user_group_role_membership": "ContentSetUserGroupRoleMembership",  # noqa: E501
        "content_set_user_group_role_memberships": "ContentSetUserGroupRoleMembershipList",  # noqa: E501
        "effective_content_set_privileges": "EffectiveContentSetPrivilegeRequest",  # noqa: E501
        "saved_question_package_specs": "SavedQuestionPackageSpecs",  # noqa: E501
        "saved_question_question": "SavedQuestionQuestion",  # noqa: E501
        "saved_question_questions": "SavedQuestionQuestionList",  # noqa: E501
        "audit_log": "AuditLog",  # noqa: E501
        "audit_logs": "AuditLogList",  # noqa: E501
        "server_host": "ServerHost",  # noqa: E501
        "server_hosts": "ServerHostList",  # noqa: E501
        "ldap_sync_connector": "LdapSyncConnector",  # noqa: E501
        "ldap_sync_connectors": "LdapSyncConnectorList",  # noqa: E501
        "server_throttle": "ServerThrottle",  # noqa: E501
        "server_throttles": "ServerThrottleList",  # noqa: E501
        "site_throttle": "SiteThrottle",  # noqa: E501
        "site_throttles": "SiteThrottleList",  # noqa: E501
        "server_throttle_status": "ServerThrottleStatus",  # noqa: E501
        "server_throttle_statuses": "ServerThrottleStatusList",  # noqa: E501
        "site_throttle_status": "SiteThrottleStatus",  # noqa: E501
        "site_throttles_statuses": "SiteThrottleStatusList",  # noqa: E501
        "import_conflict_details": "ImportConflictDetailList",  # noqa: E501
        "hashed_string": "HashedString",  # noqa: E501
        "hashed_strings": "HashedStringList",  # noqa: E501
        "verify_signature": "VerifySignature",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ImportConflictDetail(ApiItem):
    """Automagically generated API object."""

    API_NAME = "import_conflict_detail"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "import_conflict_detail"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "type": "string_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "diff": "string_types",  # noqa: E501
        "is_new": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ImportConflictDetailList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "import_conflict_details"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class CacheFilter(ApiItem):
    """Automagically generated API object."""

    API_NAME = "cache_filter"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "cache_filter"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "field": "string_types",  # noqa: E501
        "value": "string_types",  # noqa: E501
        "type": "string_types",  # noqa: E501
        "operator": "string_types",  # noqa: E501
        "not_flag": "integer_types",  # noqa: E501
        "and_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"sub_filters": "CacheFilterList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "CacheFilterList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "cache_filters"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Options(ApiItem):
    """Automagically generated API object."""

    API_NAME = "options"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "options"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "export_flag": "integer_types",  # noqa: E501
        "export_format": "integer_types",  # noqa: E501
        "export_leading_text": "string_types",  # noqa: E501
        "export_trailing_text": "string_types",  # noqa: E501
        "export_hide_csv_header_flag": "integer_types",  # noqa: E501
        "flags": "integer_types",  # noqa: E501
        "hide_errors_flag": "integer_types",  # noqa: E501
        "include_answer_times_flag": "integer_types",  # noqa: E501
        "row_counts_only_flag": "integer_types",  # noqa: E501
        "aggregate_over_time_flag": "integer_types",  # noqa: E501
        "aggregate_by_value_flag": "integer_types",  # noqa: E501
        "no_result_row_collation_flag": "integer_types",  # noqa: E501
        "most_recent_flag": "integer_types",  # noqa: E501
        "include_hashes_flag": "integer_types",  # noqa: E501
        "hide_no_results_flag": "integer_types",  # noqa: E501
        "use_user_context_flag": "integer_types",  # noqa: E501
        "script_data": "string_types",  # noqa: E501
        "return_lists_flag": "integer_types",  # noqa: E501
        "return_cdata_flag": "integer_types",  # noqa: E501
        "pct_done_limit": "integer_types",  # noqa: E501
        "context_id": "integer_types",  # noqa: E501
        "sample_frequency": "integer_types",  # noqa: E501
        "sample_start": "integer_types",  # noqa: E501
        "sample_count": "integer_types",  # noqa: E501
        "audit_history_size": "integer_types",  # noqa: E501
        "suppress_scripts": "integer_types",  # noqa: E501
        "suppress_object_list": "integer_types",  # noqa: E501
        "row_start": "integer_types",  # noqa: E501
        "row_count": "integer_types",  # noqa: E501
        "sort_order": "string_types",  # noqa: E501
        "filter_string": "string_types",  # noqa: E501
        "filter_not_flag": "integer_types",  # noqa: E501
        "recent_result_buckets": "string_types",  # noqa: E501
        "cache_id": "integer_types",  # noqa: E501
        "cache_expiration": "integer_types",  # noqa: E501
        "cache_sort_fields": "string_types",  # noqa: E501
        "include_user_details": "integer_types",  # noqa: E501
        "include_user_owned_object_ids_flag": "integer_types",  # noqa: E501
        "include_hidden_flag": "integer_types",  # noqa: E501
        "use_error_objects": "integer_types",  # noqa: E501
        "use_json": "integer_types",  # noqa: E501
        "json_pretty_print": "integer_types",  # noqa: E501
        "live_snapshot_report_count_threshold": "integer_types",  # noqa: E501
        "live_snapshot_expiration_seconds": "integer_types",  # noqa: E501
        "live_snapshot_always_use_seconds": "integer_types",  # noqa: E501
        "live_snapshot_invalidate_report_count_percentage": "integer_types",  # noqa: E501
        "disable_live_snapshots": "integer_types",  # noqa: E501
        "allow_cdata_base64_encode_flag": "integer_types",  # noqa: E501
        "cdata_base64_encoded": "integer_types",  # noqa: E501
        "import_analyze_conflicts_only": "integer_types",  # noqa: E501
        "export_dont_include_related": "integer_types",  # noqa: E501
        "export_omit_soap_envelope": "integer_types",  # noqa: E501
        "import_existing_ignore_content_set": "integer_types",  # noqa: E501
        "saved_question_qids_reissue_flag": "integer_types",  # noqa: E501
        "saved_question_qids_allow_multiple_flag": "integer_types",  # noqa: E501
        "saved_question_qids_include_expired_flag": "integer_types",  # noqa: E501
        "saved_question_qids_ignore_mr_group_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "cache_filters": "CacheFilterList",  # noqa: E501
        "import_conflict_options": "ImportConflictOptions",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ContentSet(ApiItem):
    """Automagically generated API object."""

    API_NAME = "content_set"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "description": "string_types",  # noqa: E501
        "reserved_name": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"metadata": "MetadataList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ContentSetList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "content_sets"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ContentSetRolePrivilegeOnRole(ApiItem):
    """Automagically generated API object."""

    API_NAME = "content_set_role_privilege_on_role"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_role_privilege_on_role"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"id": "integer_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "content_set": "IdReference",  # noqa: E501
        "content_set_privilege": "IdReference",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ContentSetRolePrivilegeOnRoleList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "content_set_role_privilege_on_roles"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ContentSetRole(ApiItem):
    """Automagically generated API object."""

    API_NAME = "content_set_role"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_role"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "description": "string_types",  # noqa: E501
        "reserved_name": "string_types",  # noqa: E501
        "deny_flag": "integer_types",  # noqa: E501
        "all_content_sets_flag": "integer_types",  # noqa: E501
        "category": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "metadata": "MetadataList",  # noqa: E501
        "content_set_role_privileges": "ContentSetRolePrivilegeOnRoleList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ContentSetRoleList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "content_set_roles"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ContentSetRoleMembership(ApiItem):
    """Automagically generated API object."""

    API_NAME = "content_set_role_membership"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_role_membership"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"id": "integer_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "user": "User",  # noqa: E501
        "content_set_role": "IdReference",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ContentSetRoleMembershipList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "content_set_role_memberships"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ContentSetUserGroupRoleMembership(ApiItem):
    """Automagically generated API object."""

    API_NAME = "content_set_user_group_role_membership"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_user_group_role_membership"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"id": "integer_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "user_group": "IdReference",  # noqa: E501
        "content_set_role": "IdReference",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ContentSetUserGroupRoleMembershipList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "content_set_user_group_role_memberships"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ContentSetPrivilege(ApiItem):
    """Automagically generated API object."""

    API_NAME = "content_set_privilege"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_privilege"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "reserved_name": "string_types",  # noqa: E501
        "privilege_type": "string_types",  # noqa: E501
        "privilege_module": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"metadata": "MetadataList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ContentSetPrivilegeList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "content_set_privileges"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ContentSetRolePrivilege(ApiItem):
    """Automagically generated API object."""

    API_NAME = "content_set_role_privilege"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_role_privilege"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"id": "integer_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "content_set": "IdReference",  # noqa: E501
        "content_set_role": "IdReference",  # noqa: E501
        "content_set_privilege": "IdReference",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ContentSetRolePrivilegeList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "content_set_role_privileges"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class EffectiveContentSetPrivilege(ApiItem):
    """Automagically generated API object."""

    API_NAME = "effective_content_set_privilege"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "effective_content_set_privilege"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "content_set": "ContentSet",  # noqa: E501
        "content_set_privilege_list": "ContentSetPrivilegeList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "EffectiveContentSetPrivilegeList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "effective_content_set_privileges"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Dashboard(ApiItem):
    """Automagically generated API object."""

    API_NAME = "dashboard"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "dashboard"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "public_flag": "integer_types",  # noqa: E501
        "text": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "user": "User",  # noqa: E501
        "content_set": "ContentSet",  # noqa: E501
        "group": "Group",  # noqa: E501
        "saved_question_list": "SavedQuestionList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "DashboardList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "dashboards"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class DashboardGroup(ApiItem):
    """Automagically generated API object."""

    API_NAME = "dashboard_group"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "dashboard_group"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "public_flag": "integer_types",  # noqa: E501
        "editable_flag": "integer_types",  # noqa: E501
        "other_flag": "integer_types",  # noqa: E501
        "text": "string_types",  # noqa: E501
        "display_index": "integer_types",  # noqa: E501
        "icon": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "user": "User",  # noqa: E501
        "content_set": "ContentSet",  # noqa: E501
        "dashboard_list": "DashboardList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class UserGroup(ApiItem):
    """Automagically generated API object."""

    API_NAME = "user_group"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "user_group"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
        "exclusive_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "user_list": "UserList",  # noqa: E501
        "content_set_roles": "ContentSetRoleList",  # noqa: E501
        "group": "Group",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "UserGroupList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "user_groups"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class Solution(ApiItem):
    """Automagically generated API object."""

    API_NAME = "solution"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "solution"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "solution_id": "string_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "imported_version": "string_types",  # noqa: E501
        "signature": "string_types",  # noqa: E501
        "last_update": "string_types",  # noqa: E501
        "dup_resolve_type": "integer_types",  # noqa: E501
        "imported_by": "string_types",  # noqa: E501
        "description": "string_types",  # noqa: E501
        "category": "string_types",  # noqa: E501
        "installed_xml_url": "string_types",  # noqa: E501
        "delete_xml_url": "string_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SolutionList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "solutions"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ActionGroup(ApiItem):
    """Automagically generated API object."""

    API_NAME = "action_group"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "action_group"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "and_flag": "integer_types",  # noqa: E501
        "public_flag": "integer_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "groups": "GroupList",  # noqa: E501
        "user_groups": "UserGroupList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ActionGroupList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "action_groups"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SavedQuestionPackageSpecs(ApiItem):
    """Automagically generated API object."""

    API_NAME = "saved_question_package_specs"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_question_package_specs"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "saved_question": "IdReference",  # noqa: E501
        "packages": "PackageSpecList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "None"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = ""
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SavedQuestionQuestion(ApiItem):
    """Automagically generated API object."""

    API_NAME = "saved_question_question"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_question_question"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "saved_question": "IdReference",  # noqa: E501
        "questions": "QuestionList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SavedQuestionQuestionList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "saved_question_questions"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class LdapSyncConnector(ApiItem):
    """Automagically generated API object."""

    API_NAME = "ldap_sync_connector"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "ldap_sync_connector"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "enable": "integer_types",  # noqa: E501
        "host": "string_types",  # noqa: E501
        "port": "integer_types",  # noqa: E501
        "secure": "integer_types",  # noqa: E501
        "use_ntlm": "integer_types",  # noqa: E501
        "ldap_user": "string_types",  # noqa: E501
        "ldap_password": "string_types",  # noqa: E501
        "base_users": "string_types",  # noqa: E501
        "filter_users": "string_types",  # noqa: E501
        "members_only_flag": "integer_types",  # noqa: E501
        "user_id": "string_types",  # noqa: E501
        "user_name": "string_types",  # noqa: E501
        "user_domain": "string_types",  # noqa: E501
        "user_display_name": "string_types",  # noqa: E501
        "user_member_of": "string_types",  # noqa: E501
        "base_groups": "string_types",  # noqa: E501
        "filter_groups": "string_types",  # noqa: E501
        "group_id": "string_types",  # noqa: E501
        "group_name": "string_types",  # noqa: E501
        "group_member": "string_types",  # noqa: E501
        "last_sync_timestamp": "string_types",  # noqa: E501
        "last_sync_result": "string_types",  # noqa: E501
        "disable_ldap_auth": "integer_types",  # noqa: E501
        "disable_referrals_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "LdapSyncConnectorList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "ldap_sync_connectors"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ServerThrottle(ApiItem):
    """Automagically generated API object."""

    API_NAME = "server_throttle"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "server_throttle"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "ip_address": "string_types",  # noqa: E501
        "bandwidth_bytes_limit": "integer_types",  # noqa: E501
        "connection_limit": "integer_types",  # noqa: E501
        "download_bandwidth_bytes_limit": "integer_types",  # noqa: E501
        "download_connection_limit": "integer_types",  # noqa: E501
        "sensor_bandwidth_bytes_limit": "integer_types",  # noqa: E501
        "sensor_connection_limit": "integer_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ServerThrottleList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "server_throttles"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SiteThrottle(ApiItem):
    """Automagically generated API object."""

    API_NAME = "site_throttle"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "site_throttle"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "bandwidth_bytes_limit": "integer_types",  # noqa: E501
        "download_bandwidth_bytes_limit": "integer_types",  # noqa: E501
        "sensor_bandwidth_bytes_limit": "integer_types",  # noqa: E501
        "all_subnets_flag": "integer_types",  # noqa: E501
        "deleted_flag": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"subnets": "SiteThrottleSubnetList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SiteThrottleList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "site_throttles"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SiteThrottleSubnet(ApiItem):
    """Automagically generated API object."""

    API_NAME = "site_throttle_subnet"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "site_throttle_subnet"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"range": "string_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SiteThrottleSubnetList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "site_throttle_subnets"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class ServerThrottleStatus(ApiItem):
    """Automagically generated API object."""

    API_NAME = "server_throttle_status"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "server_throttle_status"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
        "queue_delay_milliseconds": "integer_types",  # noqa: E501
        "download_queue_delay_milliseconds": "integer_types",  # noqa: E501
        "sensor_queue_delay_milliseconds": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "ServerThrottleStatusList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "server_throttle_statuses"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SiteThrottleStatus(ApiItem):
    """Automagically generated API object."""

    API_NAME = "site_throttle_status"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "site_throttle_status"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "id": "integer_types",  # noqa: E501
        "name": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"subnets": "SiteThrottleSubnetStatusList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SiteThrottleStatusList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "site_throttles_statuses"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SiteThrottleSubnetStatus(ApiItem):
    """Automagically generated API object."""

    API_NAME = "site_throttle_subnet_status"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "site_throttle_subnet_status"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "range": "string_types",  # noqa: E501
        "queue_delay_milliseconds": "integer_types",  # noqa: E501
        "download_queue_delay_milliseconds": "integer_types",  # noqa: E501
        "sensor_queue_delay_milliseconds": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "SiteThrottleSubnetStatusList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "site_throttle_subnet_statuss"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class HashedString(ApiItem):
    """Automagically generated API object."""

    API_NAME = "hashed_string"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "hashed_string"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "sensor_hash": "integer_types",  # noqa: E501
        "value_hash": "integer_types",  # noqa: E501
        "which_computer_id": "integer_types",  # noqa: E501
        "value": "string_types",  # noqa: E501
        "error_flag": "integer_types",  # noqa: E501
        "collision_flag": "integer_types",  # noqa: E501
        "first_collision": "string_types",  # noqa: E501
        "second_collision": "string_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "first_computer_id": "ComputerIdList",  # noqa: E501
        "second_computer_id": "ComputerIdList",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "HashedStringList"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "hashed_strings"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""


class SensorQueryList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "sensor_querys"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_query_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "query"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SensorQuery"
    """:class:`ApiItem`: Item class this list class holds."""


class SensorSubcolumnList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "sensor_subcolumns"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_subcolumn_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "subcolumn"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SensorSubcolumn"
    """:class:`ApiItem`: Item class this list class holds."""


class StringHintList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "string_hints"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "string_hint_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "string_hint"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "string_types"
    """:class:`ApiItem`: Item class this list class holds."""


class SensorList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "sensors"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "sensor"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Sensor"
    """:class:`ApiItem`: Item class this list class holds."""


class SensorStatList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "sensor_stats"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_stat_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "sensor_stat"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SensorStat"
    """:class:`ApiItem`: Item class this list class holds."""


class SavedActionApprovalList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "saved_action_approvals"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_action_approval_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "saved_action_approval"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SavedActionApproval"
    """:class:`ApiItem`: Item class this list class holds."""


class SavedActionRowIdList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "saved_action_row_ids"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_action_row_id_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "row_id"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "integer_types"
    """:class:`ApiItem`: Item class this list class holds."""


class SavedActionList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "saved_actions"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_action_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "saved_action"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SavedAction"
    """:class:`ApiItem`: Item class this list class holds."""


class AuditDataList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "audit_datas"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "audit_data_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "entry"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "AuditData"
    """:class:`ApiItem`: Item class this list class holds."""


class AuditLogList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "audit_logs"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "audit_log_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "audit_log"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "AuditLog"
    """:class:`ApiItem`: Item class this list class holds."""


class ServerList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "servers"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "server_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "server"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Server"
    """:class:`ApiItem`: Item class this list class holds."""


class ServerHost(ApiList):
    """Automagically generated API array object."""

    API_NAME = "server_host"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "server_host"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {"heart_beat_age_in_minute": "integer_types"}  # noqa: E501
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "servers"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ServerList"
    """:class:`ApiItem`: Item class this list class holds."""


class ServerHostList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "server_hosts"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "server_host_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "server_host"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ServerHost"
    """:class:`ApiItem`: Item class this list class holds."""


class MetadataList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "metadatas"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "metadata_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "item"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "MetadataItem"
    """:class:`ApiItem`: Item class this list class holds."""


class GroupList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "groups"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "group_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "group"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Group"
    """:class:`ApiItem`: Item class this list class holds."""


class FilterList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "filters"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "filter_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "filter"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Filter"
    """:class:`ApiItem`: Item class this list class holds."""


class SelectList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "selects"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "select_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "select"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Select"
    """:class:`ApiItem`: Item class this list class holds."""


class ErrorList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "errors"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "error_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "error"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "XmlError"
    """:class:`ApiItem`: Item class this list class holds."""


class QuestionList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "questions"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "question_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "info": "QuestionListInfo",  # noqa: E501
        "cache_info": "CacheInfo",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "question"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Question"
    """:class:`ApiItem`: Item class this list class holds."""


class PackageFileTemplateList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "package_file_templates"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "package_file_template_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "file_template"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "PackageFileTemplate"
    """:class:`ApiItem`: Item class this list class holds."""


class PackageFileStatusList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "package_file_statuss"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "package_file_status_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "status"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "PackageFileStatus"
    """:class:`ApiItem`: Item class this list class holds."""


class PackageFileList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "package_files"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "package_file_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "file"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "PackageFile"
    """:class:`ApiItem`: Item class this list class holds."""


class PackageSpecList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "package_specs"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "package_spec_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "package_spec"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "PackageSpec"
    """:class:`ApiItem`: Item class this list class holds."""


class WhiteListedUrlList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "white_listed_urls"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "white_listed_url_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "white_listed_url"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "WhiteListedUrl"
    """:class:`ApiItem`: Item class this list class holds."""


class VersionAggregateList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "version_aggregates"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "version_aggregate_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "version"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "VersionAggregate"
    """:class:`ApiItem`: Item class this list class holds."""


class SystemStatusList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "system_status"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "system_status_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "aggregate": "SystemStatusAggregate",  # noqa: E501
        "cache_info": "CacheInfo",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "client_status"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ClientStatus"
    """:class:`ApiItem`: Item class this list class holds."""


class SystemSettingList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "system_settings"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "system_setting_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "system_setting"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SystemSetting"
    """:class:`ApiItem`: Item class this list class holds."""


class UserList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "users"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "user_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "user"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "User"
    """:class:`ApiItem`: Item class this list class holds."""


class PermissionList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "permissions"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "permission_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {
        "ADMIN": "admin",
        "QUESTION_READ": "question_read",
        "QUESTION_WRITE": "question_write",
        "SENSOR_READ": "sensor_read",
        "SENSOR_WRITE": "sensor_write",
        "ACTION_READ": "action_read",
        "ACTION_WRITE": "action_write",
        "ACTION_APPROVE": "action_approval",
        "NOTIFICATION_WRITE": "notification_write",
        "CLIENTS_READ": "clients_read",
        "QUESTION_LOG_READ": "question_log_read",
        "CONTENT_ADMIN": "content_admin",
    }
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "permission"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "string_types"
    """:class:`ApiItem`: Item class this list class holds."""


class UserRoleList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "roles"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "user_role_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "role"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "UserRole"
    """:class:`ApiItem`: Item class this list class holds."""


class ActionList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "actions"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "action_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {
        "info": "ActionListInfo",  # noqa: E501
        "cache_info": "CacheInfo",  # noqa: E501
    }
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "action"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Action"
    """:class:`ApiItem`: Item class this list class holds."""


class ActionStopList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "action_stops"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "action_stop_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "action_stop"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ActionStop"
    """:class:`ApiItem`: Item class this list class holds."""


class ArchivedQuestionList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "archived_questions"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "archived_question_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "archived_question"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ArchivedQuestion"
    """:class:`ApiItem`: Item class this list class holds."""


class SavedQuestionList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "saved_questions"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_question_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "saved_question"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SavedQuestion"
    """:class:`ApiItem`: Item class this list class holds."""


class ParseJobList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "parse_jobs"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parse_job_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "parse_job"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ParseJob"
    """:class:`ApiItem`: Item class this list class holds."""


class ParseResultGroupList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "parse_result_groups"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parse_result_group_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "parse_result_group"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ParseResultGroup"
    """:class:`ApiItem`: Item class this list class holds."""


class ParseResultList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "parse_results"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parse_result_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "parse_result"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ParseResult"
    """:class:`ApiItem`: Item class this list class holds."""


class ParameterList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "parameters"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parameter_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "parameter"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Parameter"
    """:class:`ApiItem`: Item class this list class holds."""


class ParameterValueList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "parameter_values"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "parameter_value_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "value"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "string_types"
    """:class:`ApiItem`: Item class this list class holds."""


class SensorReferenceList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "sensor_references"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "sensor_reference_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "sensor_reference"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SensorReference"
    """:class:`ApiItem`: Item class this list class holds."""


class PluginArgumentList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "plugin_arguments"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_argument_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "argument"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "PluginArgument"
    """:class:`ApiItem`: Item class this list class holds."""


class PluginSqlResultList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "plugin_sql_results"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_sql_result_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "value"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "string_types"
    """:class:`ApiItem`: Item class this list class holds."""


class PluginSqlColumnList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "plugin_sql_columns"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_sql_column_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "name"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "string_types"
    """:class:`ApiItem`: Item class this list class holds."""


class PluginSql(ApiList):
    """Automagically generated API array object."""

    API_NAME = "plugin_sql"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_sql"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {
        "rows_affected": "integer_types",  # noqa: E501
        "result_count": "integer_types",  # noqa: E501
    }
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"columns": "PluginSqlColumnList"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "result_row"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "PluginSqlResultList"
    """:class:`ApiItem`: Item class this list class holds."""


class PluginCommandList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "plugin_commands"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_command_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "command"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "string_types"
    """:class:`ApiItem`: Item class this list class holds."""


class UploadFileList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "upload_files"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "upload_file_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "upload_file"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "UploadFile"
    """:class:`ApiItem`: Item class this list class holds."""


class PluginList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "plugins"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "plugin"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Plugin"
    """:class:`ApiItem`: Item class this list class holds."""


class PluginScheduleList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "plugin_schedules"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "plugin_schedule_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "plugin_schedule"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "PluginSchedule"
    """:class:`ApiItem`: Item class this list class holds."""


class ComputerSpecList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "computer_specs"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "computer_spec_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "computer_spec"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ComputerGroupSpec"
    """:class:`ApiItem`: Item class this list class holds."""


class ComputerGroupList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "computer_groups"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "computer_group_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {"cache_info": "CacheInfo"}  # noqa: E501
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "computer_group"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ComputerGroup"
    """:class:`ApiItem`: Item class this list class holds."""


class ImportConflictDetailList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "import_conflict_details"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "import_conflict_detail_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "import_conflict_detail"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ImportConflictDetail"
    """:class:`ApiItem`: Item class this list class holds."""


class CacheFilterList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "cache_filters"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "cache_filter_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "filter"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "CacheFilter"
    """:class:`ApiItem`: Item class this list class holds."""


class ImportConflictOptions(ApiList):
    """Automagically generated API array object."""

    API_NAME = "import_conflict_options"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "import_conflict_options"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "import_conflict_option"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "integer_types"
    """:class:`ApiItem`: Item class this list class holds."""


class ContentSetList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "content_sets"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "content_set"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ContentSet"
    """:class:`ApiItem`: Item class this list class holds."""


class ContentSetRolePrivilegeOnRoleList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "content_set_role_privilege_on_roles"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_role_privilege_on_role_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "content_set_role_privilege"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ContentSetRolePrivilegeOnRole"
    """:class:`ApiItem`: Item class this list class holds."""


class ContentSetRoleList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "content_set_roles"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_role_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "content_set_role"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ContentSetRole"
    """:class:`ApiItem`: Item class this list class holds."""


class ContentSetRoleMembershipList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "content_set_role_memberships"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_role_membership_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "content_set_role_membership"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ContentSetRoleMembership"
    """:class:`ApiItem`: Item class this list class holds."""


class ContentSetUserGroupRoleMembershipList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "content_set_user_group_role_memberships"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_user_group_role_membership_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "content_set_user_group_role_membership"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ContentSetUserGroupRoleMembership"
    """:class:`ApiItem`: Item class this list class holds."""


class ContentSetPrivilegeList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "content_set_privileges"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_privilege_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "content_set_privilege"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ContentSetPrivilege"
    """:class:`ApiItem`: Item class this list class holds."""


class ContentSetRolePrivilegeList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "content_set_role_privileges"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "content_set_role_privilege_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "content_set_role_privilege"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ContentSetRolePrivilege"
    """:class:`ApiItem`: Item class this list class holds."""


class EffectiveContentSetPrivilegeRequest(ApiList):
    """Automagically generated API array object."""

    API_NAME = "effective_content_set_privilege_request"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "effective_content_set_privilege_request"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "user"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "User"
    """:class:`ApiItem`: Item class this list class holds."""


class EffectiveContentSetPrivilegeList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "effective_content_set_privileges"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "effective_content_set_privilege_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "effective_content_set_privilege"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "EffectiveContentSetPrivilege"
    """:class:`ApiItem`: Item class this list class holds."""


class DashboardList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "dashboards"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "dashboard_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "dashboard"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Dashboard"
    """:class:`ApiItem`: Item class this list class holds."""


class UserGroupList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "user_groups"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "user_group_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "user_group"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "UserGroup"
    """:class:`ApiItem`: Item class this list class holds."""


class SolutionList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "solutions"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "solution_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "solution"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "Solution"
    """:class:`ApiItem`: Item class this list class holds."""


class ActionGroupList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "action_groups"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "action_group_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "action_group"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ActionGroup"
    """:class:`ApiItem`: Item class this list class holds."""


class SavedQuestionQuestionList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "saved_question_questions"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "saved_question_question_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "saved_question_question"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SavedQuestionQuestion"
    """:class:`ApiItem`: Item class this list class holds."""


class LdapSyncConnectorList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "ldap_sync_connectors"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "ldap_sync_connector_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "ldap_sync_connector"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "LdapSyncConnector"
    """:class:`ApiItem`: Item class this list class holds."""


class ServerThrottleList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "server_throttles"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "server_throttle_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "server_throttle"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ServerThrottle"
    """:class:`ApiItem`: Item class this list class holds."""


class SiteThrottleList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "site_throttles"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "site_throttle_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "site_throttle"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SiteThrottle"
    """:class:`ApiItem`: Item class this list class holds."""


class SiteThrottleSubnetList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "site_throttle_subnets"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "site_throttle_subnet_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "subnet"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SiteThrottleSubnet"
    """:class:`ApiItem`: Item class this list class holds."""


class ServerThrottleStatusList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "server_throttle_statuses"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "server_throttle_status_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "server_throttle_status"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "ServerThrottleStatus"
    """:class:`ApiItem`: Item class this list class holds."""


class SiteThrottleStatusList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "site_throttles_statuses"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "site_throttle_status_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "site_throttle_status"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SiteThrottleStatus"
    """:class:`ApiItem`: Item class this list class holds."""


class SiteThrottleSubnetStatusList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "site_throttle_subnet_statuss"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "site_throttle_subnet_status_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "subnet"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "SiteThrottleSubnetStatus"
    """:class:`ApiItem`: Item class this list class holds."""


class ComputerIdList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "computer_ids"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "computer_id_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "id"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "integer_types"
    """:class:`ApiItem`: Item class this list class holds."""


class HashedStringList(ApiList):
    """Automagically generated API array object."""

    API_NAME = "hashed_strings"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "hashed_string_list"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "hashed_string"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "HashedString"
    """:class:`ApiItem`: Item class this list class holds."""


BUILD_META = {
    "script": "build_objects_from_wsdl.py",
    # Script used to build this file
    "script_version": "3.0.0",
    # Version of script used to build this file
    "script_platform": "Darwin-18.6.0-x86_64-i386-64bit",
    # OS Platform that ran this build script
    "script_python": "3.6.8 (default, May 29 2019, 13:34:43) ",
    # Python version that ran this build script
    "date": "2019-06-02 11:50:15.852609",
    # Date/time in UTC format of when this file was built
    "source_file": "/libraries/taniumjs/console.wsdl",
    # File that was used to auto-generate objects in this file
    "source_file_date": "2019-06-02 11:33:31.836163",
    # Date/time in UTC format of the source_file
}
""":obj:`dict`: How this module was built (date/time in UTC format)."""

COMMANDS = [
    "AddObject",
    "GetObject",
    "MoveObject",
    "TransferObject",
    "UpdateObject",
    "DeleteObject",
    "GetSavedQuestions",
    "GetResultInfo",
    "GetResultData",
    "GetMergedResultData",
    "UploadFile",
    "RunPlugin",
    "ExportObject",
    "ImportObject",
    "VerifySignature",
]
""":obj:`list` of :obj:`str`:API commands."""

VERSION = {
    "major": 7,
    "minor": 3,
    "protocol": 314,
    "build": 3424,
    "string": "7.3.314.3424",
}
""":obj:`dict`: Tanium API version these objects are intended to be used for."""

__version__ = VERSION["string"]
""":obj:`str`: Tanium API version these objects are intended to be used for."""

api_fixes()
expand_cls_globals()
