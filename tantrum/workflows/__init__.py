# -*- coding: utf-8 -*-
"""Workflow encapsulation package for performing actions using the Tanium API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json

from collections import OrderedDict

from . import exceptions
from .. import utils

FILTER_MAP = {
    "less": {"op": "Less", "tmpl": "{value}"},
    "lessequal": {"op": "LessEqual", "tmpl": "{value}"},
    "greater": {"op": "Greater", "tmpl": "{value}"},
    "greaterequal": {"op": "GreaterEqual", "tmpl": "{value}"},
    "equal": {"op": "Equal", "tmpl": "{value}"},
    "regex": {"op": "RegexMatch", "tmpl": "{value}"},
    "startswith": {"op": "RegexMatch", "tmpl": ".*{value}"},
    "endswith": {"op": "RegexMatch", "tmpl": "{value}.*"},
    "contains": {"op": "RegexMatch", "tmpl": ".*{value}.*"},
    "hash": {"op": "HashMatch", "tmpl": "{value}"},
}


TYPE_MAP = {
    "Hash": 0,
    # SENSOR_RESULT_TYPE_STRING
    "String": 1,
    # SENSOR_RESULT_TYPE_VERSION
    "Version": 2,
    # SENSOR_RESULT_TYPE_NUMERIC
    "NumericDecimal": 3,
    # SENSOR_RESULT_TYPE_DATE_BES
    "BESDate": 4,
    # SENSOR_RESULT_TYPE_IPADDRESS
    "IPAddress": 5,
    # SENSOR_RESULT_TYPE_DATE_WMI
    "WMIDate": 6,
    #  e.g. "2 years, 3 months, 18 days, 4 hours, 22 minutes:
    # 'TimeDiff', and 3.67 seconds" or "4.2 hours"
    # (numeric + "Y|MO|W|D|H|M|S" units)
    "TimeDiff": 7,
    #  e.g. 125MB or 23K or 34.2Gig (numeric + B|K|M|G|T units)
    "DataSize": 8,
    "NumericInteger": 9,
    "VariousDate": 10,
    "RegexMatch": 11,
    "LastOperatorType": 12,
}


class Workflow(object):
    def __init__(self, adapter, obj, lvl="info", result=None):
        """Constructor."""
        self._lvl = lvl
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        self.obj = obj
        self.adapter = adapter
        self._result = result
        self._last_result = result

    def __repr__(self):
        """Show object info.

        Returns:
            (:obj:`str`)

        """
        return self.__str__()

    @property
    def api_objects(self):
        return self.adapter.api_objects


class Clients(Workflow):
    def __str__(self):
        """Show object info.

        Returns:
            (:obj:`str`)

        """
        ctmpl = "{c.__module__}.{c.__name__}".format
        bits = ["count={}".format(len(self.obj))]
        bits = "({})".format(", ".join(bits))
        cls = ctmpl(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    @classmethod
    def get_all(cls, adapter, lvl="info"):
        """Pass."""
        result = adapter.cmd_get(obj=adapter.api_objects.ClientStatus())
        return cls(adapter=adapter, obj=result(), lvl=lvl, result=result)


class Question(Workflow):
    def __str__(self):
        """Show object info.

        Returns:
            (:obj:`str`)

        """
        ctmpl = "{c.__module__}.{c.__name__}".format
        bits = [
            "left={}".format(len(self.left)),
            "id={}".format(self.obj.id),
            "text={}".format(self.obj.query_text),
        ]
        bits = "(\n  {},\n)".format(",\n  ".join(bits))
        cls = ctmpl(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    @classmethod
    def new(cls, adapter, lvl="info"):
        """Pass."""
        return cls(obj=adapter.api_objects.Question(), adapter=adapter, lvl=lvl)

    @classmethod
    def get_by_id(cls, adapter, id, lvl="info"):
        result = adapter.cmd_get(obj=adapter.api_objects.Question(id=id))
        return cls(adapter=adapter, obj=result(), lvl=lvl, result=result)

    def _check_id(self):
        if not self.obj.id:
            m = "No ID issued yet, ask the question!"
            raise exceptions.ModuleError(m)

    def refetch(self):
        self._check_id()
        result = self.adapter.cmd_get(obj=self.obj)
        self._last_result = result
        self.obj = result()
        return self

    def result_info(self):
        self._check_id()
        result = self.adapter.cmd_get_result_info(obj=self.obj)
        self._last_result = result
        self._last_result_info = result()
        return self._last_result_info

    def result_data(self):
        self._check_id()
        result = self.adapter.cmd_get_result_data(obj=self.obj)
        self._last_result = result
        self._last_result_data = result()
        return self._last_result_data

    def ask(self):
        result = self.adapter.cmd_add(obj=self.obj)
        self.obj = result()
        self.refetch()
        return self

    @property
    def left(self):
        if not getattr(self.obj, "selects", None):
            self.obj.selects = self.api_objects.SelectList()
        return self.obj.selects

    def add_left_sensor(
        self, sensor, set_param_defaults=True, allow_empty_params=False
    ):
        """Add a sensor to the left hand side of the question.

        Args:
            sensor (:obj:`Sensor`):
                Sensor workflow object.

        """
        select = sensor.build_select(
            set_param_defaults=set_param_defaults, allow_empty_params=allow_empty_params
        )
        self.left.append(select)


class Sensor(Workflow):
    def __str__(self):
        """Show object info.

        Returns:
            (:obj:`str`)

        """
        ctmpl = "{c.__module__}.{c.__name__}".format
        bits = [
            "name={!r}".format(self.obj.name),
            "filter={}".format(", ".join(self.filter_vals)),
        ]
        if self.params_defined or self.params_set:
            bits += [
                "params_defined={}".format(list(self.params_defined.keys())),
                "params_set={}".format(list(self.params_set.items())),
            ]
        bits = "({})".format(", ".join(bits))
        cls = ctmpl(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    @classmethod
    def get_by_name(cls, adapter, name, lvl="info"):
        """Pass."""
        result = adapter.cmd_get(obj=adapter.api_objects.Sensor(name=name))
        return cls(adapter=adapter, obj=result(), lvl=lvl, result=result)

    @classmethod
    def get_by_id(cls, adapter, id, lvl="info"):
        """Pass."""
        result = adapter.cmd_get(obj=adapter.api_objects.Sensor(id=id))
        return cls(adapter=adapter, obj=result(), lvl=lvl, result=result)

    @property
    def params_defined(self):
        param_defs = json.loads(self.obj.parameter_definition or "{}")
        params = param_defs.get("parameters", [])
        for p in params:
            pdef = p.get("defaultValue", "")
            pval = p.get("value", "")
            pvals = p.get("values", [])
            if pdef not in ["", None]:
                derived_default = pdef
            elif pval not in ["", None]:
                derived_default = pval
            elif pvals:
                derived_default = pvals[0]
            else:
                derived_default = ""
            p["derived_default"] = derived_default
        return OrderedDict((p["key"], p) for p in params)

    @property
    def params_set(self):
        return OrderedDict((p.key, p.value) for p in self.params)

    @property
    def params(self):
        if not hasattr(self, "_params"):
            self._params = self.api_objects.ParameterList()
        return self._params

    def set_parameter(
        self, key, value="", derive_default=True, delim="||", allow_undefined=True
    ):
        """Set a parameters value for this sensor.

        Args:
            key (:obj:`str`):
                Key name of parameter to set.
            value (:obj:`str`, optional):
                Value of parameter to set.

                Defaults to: "".
            derive_default (:obj:`bool`, optional):
                Get default value from parameter definition if value is "".

                Defaults to: True.
            delim (:obj:`str`, optional):
                String to put before and after parameter key name when sending to API.

                Defaults to: "||".
            allow_undefined (:obj:`bool`, optional):
                Allow undefined parameters to be set.
                Throws exception if False and key not in :attr:`Sensor.param_keys`.

                Defaults to: True.
        """
        param_def = self.params_defined.get(key, None)
        if param_def is None:
            m = "Parameter key {o!r} is not one of the defined parameters {ov}"
            m = m.format(o=key, ov=list(self.params_defined.keys()))
            if allow_undefined:
                self.log.info(m)
            else:
                raise exceptions.ModuleError(m)
        elif derive_default and value == "":
            value = param_def.get("derived_default", "")

        key_delim = "{d}{key}{d}".format(d=delim, key=key)
        param = self.api_objects.Parameter(key=key_delim, value=value)

        self.params.append(param)

    @property
    def filter(self):
        if not hasattr(self, "_filter"):
            self._filter = self.api_objects.Filter()
            self._filter.sensor = self.api_objects.Sensor()
            self._filter.sensor.hash = self.obj.hash
        return self._filter

    @property
    def filter_vals(self):
        if any([self.filter.value, self.filter.operator]):
            keys = [
                "operator",
                "value",
                "ignore_case_flag",
                "not_flag",
                "all_values_flag",
                "max_age_seconds",
                "value_type",
            ]
            vals = ["{}: {!r}".format(k, getattr(self.filter, k)) for k in keys]
        else:
            vals = []
        return vals

    def set_filter(
        self,
        value,
        operator="regex",
        ignore_case_flag=True,
        not_flag=False,
        all_values_flag=False,
        max_age_seconds=0,
        value_type=None,
    ):
        """Set a filter for this sensor to be used in a question.

        Args:
            value (:obj:`str`):
                Filter sensor rows returned on this value.
            operator (:obj:`str`, optional):
                Operator to use for filter_value.
                Must be one of :data:`FILTER_MAP`.

                Defaults to: "regex".
            ignore_case_flag (:obj:`bool`, optional):
                Ignore case when filtering on value.

                Defaults to: True.
            not_flag (:obj:`bool`, optional):
                If set, negate the match.

                Defaults to: False.
            max_age_seconds (:obj:`int`, optional):
                How old a sensor result can be before we consider it invalid.
                0 means to use the max age property of the sensor.

                Defaults to: 0.
            all_values_flag (:obj:`bool`, optional):
                Have filter match all values instead of any value.

                Defaults to: False.
            value_type (:obj:`str`, optional):
                Have filter consider the value type as this.
                Must be one of :data:`TYPE_MAP`

                Defaults to: None.

        """
        if operator not in FILTER_MAP:
            m = "Operator {o!r} must be one of {vo}"
            m = m.format(o=operator, vo=FILTER_MAP.keys())
            raise exceptions.ModuleError(m)

        if value_type not in TYPE_MAP:
            m = "Value type {o!r} must be one of {vo}"
            m = m.format(o=value_type, vo=TYPE_MAP.keys())
            raise exceptions.ModuleError(m)

        self.filter.value = FILTER_MAP[operator]["tmpl"].format(value=value)
        self.filter.operator = FILTER_MAP[operator]["op"]
        self.filter.ignore_case_flag = ignore_case_flag
        self.filter.not_flag = not_flag
        self.filter.all_values_flag = all_values_flag
        self.filter.max_age_seconds = max_age_seconds
        self.filter.value_type = value_type

    def build_select(self, set_param_defaults=True, allow_empty_params=False):
        select = self.api_objects.Select()
        select.filter = self.filter
        select.sensor = self.api_objects.Sensor()

        for key in self.params_defined:
            if key not in self.params_set and set_param_defaults:
                self.set_parameter(key=key, derive_default=True)

        for param in self.params:
            if param.value in ["", None] and not allow_empty_params:
                m = "Parameter {p.key!r} value {p.value!r} is empty, definition: {d}"
                m = m.format(p=param, d=self.params_defined.get(key, None))
                raise exceptions.ModuleError(m)

        if self.params:
            select.sensor.parameters = self.params
            select.sensor.source_id = self.obj.id
            select.filter.sensor.id = self.obj.id
        else:
            select.sensor.hash = self.obj.hash
        select.WORKFLOW = self
        return select


# parsed
# saved
# sensor
