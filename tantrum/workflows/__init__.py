# -*- coding: utf-8 -*-
"""Workflow encapsulation package for performing actions using the Tanium API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import json
import time

from collections import OrderedDict

from . import exceptions
from .. import utils

OPERATOR_MAP = {
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

PCT_FMT = "{0:.0f}%".format


def get_operator_map(operator):
    if operator in OPERATOR_MAP:
        return OPERATOR_MAP[operator]
    m = "Operator {o!r} is invalid, must be one of {vo}"
    m = m.format(o=operator, vo=list(OPERATOR_MAP.keys()))
    raise exceptions.ModuleError(m)


def get_type_map(type):
    if type in TYPE_MAP:
        return TYPE_MAP[type]
    m = "Type {o!r} is invalid, must be one of {vo}"
    m = m.format(o=type, vo=list(TYPE_MAP.keys()))
    raise exceptions.ModuleError(m)


def calc_percent(part, whole):
    """Utility method for getting percentage of part out of whole

    Parameters
    ----------
    part: int, float
    whole: int, float

    Returns
    -------
    int : the percentage of part out of whole
    """
    if 0 in [part, whole]:
        return float(0)
    return 100 * (float(part) / float(whole))


def calc_percent_of(percent, whole):
    """Utility method for getting percentage of whole

    Parameters
    ----------
    percent: int, float
    whole: int, float

    Returns
    -------
    int : the percentage of whole
    """
    return int((percent * whole) / 100.0)


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

    @staticmethod
    def build_last_reg_filter(
        adapter, last_reg=300, operator="greaterequal", not_flag=False, filters=None
    ):
        op_dict = get_operator_map(operator)
        now_dt = datetime.datetime.utcnow()
        ago_td = datetime.timedelta(seconds=-(int(last_reg)))
        ago_dt = now_dt + ago_td
        ago_str = ago_dt.strftime(adapter.api_objects.module_dt)
        cfilter = adapter.api_objects.CacheFilter(
            field="last_registration",
            type="Date",
            operator=op_dict["op"],
            not_flag=not_flag,
            value=ago_str,
        )
        filters = filters or adapter.api_objects.CacheFilterList()
        filters.append(cfilter)
        return filters

    @classmethod
    def get_all(
        cls,
        adapter,
        filters=None,
        sort_fields="last_registration",
        cache_paging=1,
        cache_expiration=600,
        lvl="info",
    ):
        """Pass."""
        log = utils.logs.get_obj_log(obj=cls, lvl=lvl)
        find_obj = adapter.api_objects.ClientStatus()
        get_args = {"cache_sort_fields": sort_fields}
        if filters is not None:
            get_args["cache_filters"] = filters
        if cache_paging:
            get_args["row_start"] = 0
            get_args["row_count"] = cache_paging
            get_args["cache_expiration"] = cache_expiration
        result = adapter.cmd_get(obj=find_obj, **get_args)
        log.debug(result.http_response(http_client=adapter.http_client))
        result_obj = result()

        m = "Received initial {o!r} length={len}, cache_info={cache!r}"
        m = m.format(
            o=result_obj.__class__.__name__,
            len=len(result_obj),
            cache=getattr(result_obj, "cache_info", None),
        )
        log.info(m)
        if cache_paging:
            total_rows = result_obj.cache_info.filtered_row_count
            paging_get_args = {k: v for k, v in get_args.items()}
            while len(result_obj) < total_rows:
                paging_get_args["row_start"] += cache_paging
                paging_result = adapter.cmd_get(obj=find_obj, **paging_get_args)
                log.debug(paging_result.http_response(http_client=adapter.http_client))
                paging_result_obj = paging_result()

                m = "Received page of {o!r} length={len}, cache_info={cache!r}"
                m = m.format(
                    o=paging_result_obj.__class__.__name__,
                    len=len(paging_result_obj),
                    cache=getattr(paging_result_obj, "cache_info", None),
                )
                log.info(m)

                result_obj += paging_result_obj
                m = "{o!r} received so far {len} out of total {total}"
                m = m.format(
                    o=result_obj.__class__.__name__,
                    len=len(result_obj),
                    total=total_rows,
                )
                log.info(m)
        return cls(adapter=adapter, obj=result_obj, lvl=lvl, result=result)


class Question(Workflow):
    def __str__(self):
        """Show object info.

        Returns:
            (:obj:`str`)

        """
        ctmpl = "{c.__module__}.{c.__name__}".format
        atmpl = "{k}='{v}'".format
        attrs = ["id", "query_text"]
        bits = [atmpl(k=attr, v=getattr(self.obj, attr, None)) for attr in attrs]
        bits += [atmpl(k=k, v=v) for k, v in self.expiration.items()]
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

    @property
    def expiration(self):
        now_dt = datetime.datetime.utcnow()
        now_td = datetime.timedelta()
        ret = {
            "expiration": now_dt,
            "expire_in": now_td,
            "expire_ago": now_td,
            "expired": True,
        }
        if self.obj.expiration:
            ex_dt = self.api_objects.module_dt_format(self.obj.expiration)
            is_ex = now_dt >= ex_dt
            ret["expiration"] = ex_dt
            ret["expired"] = is_ex
            if is_ex:
                ret["expire_ago"] = now_dt - ex_dt
            else:
                ret["expire_in"] = ex_dt - now_dt
        return ret

    def refetch(self):
        self._check_id()
        result = self.adapter.cmd_get(obj=self.obj)
        self._last_result = result
        self.obj = result()
        return self

    def answers_info(self):
        self._check_id()
        result = self.adapter.cmd_get_result_info(obj=self.obj)
        info = result()
        self._last_result = result
        self._last_info = info
        return info

    def answers(self):
        self._check_id()
        result = self.adapter.cmd_get_result_data(obj=self.obj)
        data = result()
        self._last_result = result
        self._last_data = data
        return data

    def answers_paged(self, size=1):  # float= %, int = #
        return NotImplementedError

    def answers_sse(self):
        return NotImplementedError

    def answers_poll(self, sleep=5, pct=99, secs=0, answered=0, passed=0):
        """Poll for answers for this question.

        Args:
            sleep (:obj:`int`, optional):
                Check for answers every N seconds.

                Defaults to: 5.
            pct (:obj:`int`, optional):
                Wait until the percentage of clients answered is N percent.

                Defaults to: 99.
            secs (:obj:`int`, optional):
                If not 0, wait until N seconds for pct of clients answered instead of
                until question expiration.

                Defaults to: 0.
            answered (:obj:`int`, optional):
                If not 0, wait until N clients have answered instead of
                ``estimated_total`` of clients from API.

                Defaults to: 0.
            passed (:obj:`int`, optional):
                If not 0, wait until N clients have passed the right hand
                side of the question.

                Defaults to: 0.

        """
        self._check_id()
        start = datetime.datetime.utcnow()
        if secs:
            stop_dt = start + datetime.timedelta(seconds=secs)
        else:
            stop_dt = self.expiration["expiration"]

        m = "Will poll for answers for {o} until {stop_dt}"
        m = m.format(o=self, stop_dt=stop_dt)
        self.log.debug(m)

        while True:
            m = "New polling loop for {o}"
            m = m.format(o=self)
            self.log.debug(m)

            infos = self.answers_info()

            m = "Received answers info: {}"
            m = m.format(infos.serialize())
            self.log.debug(m)

            info = infos[0]

            # if answered and
            stop_count = secs or info.estimated_total
            answers_pct = calc_percent(part=info.mr_passed, whole=stop_count)

            m = (
                "Answers received {answers_pct} ({info.mr_passed} out of {stop_count}) "
                "(estimated_total: {info.estimated_total})"
            )
            m = m.format(
                answers_pct=PCT_FMT(answers_pct), info=info, stop_count=stop_count
            )
            self.log.debug(m)

            if answers_pct >= pct:
                m = "Reached {answers_pct} "
            if datetime.datetime.utcnow() >= stop_dt:

                m = "Reached stop_dt {stop_dt}, considering all answers in"
                m = m.format(stop_dt=stop_dt)
                self.log.debug(m)

                return infos

            if self.expiration["expired"]:

                m = "Reached expiration {expiration}, considering all answers in"
                m = m.format(expiration=self.expiration)
                self.log.debug(m)

                return infos

            time.sleep(sleep)
        return NotImplementedError

    def ask(self):
        if self.obj.id:
            wipe_attrs = ["id", "context_group", "management_rights_group"]
            for attr in wipe_attrs:
                setattr(self.obj, attr, None)
        result = self.adapter.cmd_add(obj=self.obj)
        self._last_result = result
        self.obj = result()
        self.refetch()
        return self

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
        if not getattr(self.obj, "selects", None):
            self.obj.selects = self.api_objects.SelectList()
        self.obj.selects.append(select)


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
        type=None,
    ):
        """Set a filter for this sensor to be used in a question.

        Args:
            value (:obj:`str`):
                Filter sensor rows returned on this value.
            operator (:obj:`str`, optional):
                Operator to use for filter_value.
                Must be one of :data:`OPERATOR_MAP`.

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
            type (:obj:`str`, optional):
                Have filter consider the value type as this.
                Must be one of :data:`TYPE_MAP`

                Defaults to: None.

        """
        op_dict = get_operator_map(operator)
        if type:
            get_type_map(type)

        self.filter.value = op_dict["tmpl"].format(value=value)
        self.filter.operator = op_dict["op"]
        self.filter.ignore_case_flag = ignore_case_flag
        self.filter.not_flag = not_flag
        self.filter.all_values_flag = all_values_flag
        self.filter.max_age_seconds = max_age_seconds
        self.filter.value_type = type

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
