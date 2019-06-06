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
    """Validate operator against :data:`OPERATOR_MAP`."""
    if operator in OPERATOR_MAP:
        return OPERATOR_MAP[operator]
    m = "Operator {o!r} is invalid, must be one of {vo}"
    m = m.format(o=operator, vo=list(OPERATOR_MAP.keys()))
    raise exceptions.ModuleError(m)


def get_type_map(type):
    """Validate type against :data:`TYPE_MAP`."""
    if type in TYPE_MAP:
        return TYPE_MAP[type]
    m = "Type {o!r} is invalid, must be one of {vo}"
    m = m.format(o=type, vo=list(TYPE_MAP.keys()))
    raise exceptions.ModuleError(m)


class Workflow(object):
    def __init__(self, adapter, obj, lvl="info", result=None):
        """Constructor.

        Args:
            adapter (:obj:`tantrum.adapters.Adapter`):
                Adapter to use for this workflow.
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for this workflow.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".
            result (:obj:`tantrum.results.Result`, optional):
                Result object that ``obj`` was generated from.

                Defaults to: None.

        """
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
        """Build a set of filters to be used in :meth:`Clients.get_all.

        Args:
            adapter (:obj:`tantrum.adapters.Adapter`):
                Adapter to use for this workflow.
            last_reg (:obj:`int`, optional):
                Only return clients that have registered in N number of seconds.

                Defaults to: 300.
            operator (:obj:`str`, optional):
                Defines how the last_registered attribute of each client status is
                compared against the value in last_reg.
                Must be one of :data:`OPERATOR_MAP`.

                Defaults to: "greaterequal".
            not_flag (:obj:`int`, optional):
                If True have the API return all rows that do not match the operator.

                Defaults to: 1000.
            filters (:obj:`object`, optional):
                If a CacheFilterList object is supplied, the last_registration filter
                generated by this method will be appended to it. If this is None,
                a new CacheFilterList will be created with the last_registration filter
                being the only item in it.

                Defaults to: None.

        Returns:
            :obj:`Clients`

        """
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
        cache_paging=1000,
        cache_expiration=600,
        lvl="info",
    ):
        """Get all Clients.

        Args:
            adapter (:obj:`tantrum.adapters.Adapter`):
                Adapter to use for this workflow.
            filters (:obj:`object`, optional):
                Tantrum CacheFilterList returned from
                :meth:`Clients.build_last_reg_filter`.

                Defaults to: None.
            sort_fields (:obj:`str`, optional):
                Attribute of a ClientStatus object to have API sort the return on.

                Defaults to: "last_registration".
            cache_paging (:obj:`int`, optional):
                Get N number of clients at a time from the API.
                If set to 0, disables paging and gets all clients in one call.

                Defaults to: 1000.
            cache_expiration (:obj:`int`, optional):
                When cache_paging is not 0, have the API keep the cache of clients
                for this many seconds before expiring the cache.

                Defaults to: 600.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        Returns:
            :obj:`Clients`

        """
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
        """Create a new Question workflow.

        Args:
            adapter (:obj:`tantrum.adapters.Adapter`):
                Adapter to use for this workflow.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        Returns:
            :obj:`Question`

        """
        return cls(obj=adapter.api_objects.Question(), adapter=adapter, lvl=lvl)

    @classmethod
    def get_by_id(cls, adapter, id, lvl="info"):
        """Get a question object by id.

        Args:
            adapter (:obj:`tantrum.adapters.Adapter`):
                Adapter to use for this workflow.
            id (:obj:`int`):
                id of question to fetch.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        Returns:
            :obj:`Question`

        """
        result = adapter.cmd_get(obj=adapter.api_objects.Question(id=id))
        return cls(adapter=adapter, obj=result(), lvl=lvl, result=result)

    def _check_id(self):
        """Check that question has been asked if id is set."""
        if not self.obj.id:
            m = "No id issued yet, ask the question!"
            raise exceptions.ModuleError(m)

    @property
    def expiration(self):
        """Get expiration details for this question.

        Returns:
            :obj:`dict`

        """
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
        """Re-fetch this question."""
        self._check_id()
        result = self.adapter.cmd_get(obj=self.obj)
        self._last_result = result
        self.obj = result()

    def ask(self, **kwargs):
        """Ask the question.

        Notes:
            If question has already been asked (id is set), we wipe out attrs:
            ["id", "context_group", "management_rights_group"], then add it.

        """
        if self.obj.id:
            wipe_attrs = ["id", "context_group", "management_rights_group"]
            for attr in wipe_attrs:
                setattr(self.obj, attr, None)
        result = self.adapter.cmd_add(obj=self.obj, **kwargs)
        self._last_result = result
        self.obj = result()
        self.refetch()

    def answers_get_info(self):
        """Return the ResultInfo for this question.

        Returns:
            :obj:`tantrum.api_models.ApiModel`: ResultInfoList API Object

        """
        self._check_id()

        result = self.adapter.cmd_get_result_info(obj=self.obj)
        self._last_result = result

        infos = result()
        self._last_infos = infos

        m = "Received answers info: {infos}"
        m = m.format(infos=infos.serialize())
        self.log.debug(m)
        self.log.debug(format(self))
        return infos

    def answers_poll(self, sleep=5, pct=99, secs=0, total=0):
        """Poll for answers from clients for this question.

        Args:
            sleep (:obj:`int`, optional):
                Check for answers every N seconds.

                Defaults to: 5.
            pct (:obj:`int`, optional):
                Wait until the percentage of clients total is N percent.

                Defaults to: 99.
            secs (:obj:`int`, optional):
                If not 0, wait until N seconds for pct of clients total instead of
                until question expiration.

                Defaults to: 0.
            total (:obj:`int`, optional):
                If not 0, wait until N clients have total instead of
                ``estimated_total`` of clients from API.

                Defaults to: 0.

        Returns:
            :obj:`object`: ResultInfoList API object

        """
        self._check_id()

        start = datetime.datetime.utcnow()

        if secs:
            stop_dt = start + datetime.timedelta(seconds=secs)
        else:
            stop_dt = self.expiration["expiration"]

        m = "Start polling loop for answers until for {o} until {stop_dt}"
        m = m.format(o=self, stop_dt=stop_dt)
        self.log.debug(m)

        infos = self.answers_get_info()
        info = infos[0]
        est_total = info.estimated_total
        this_total = total if total and total <= est_total else est_total
        now_pct = utils.tools.calc_percent(part=info.mr_passed, whole=this_total)

        while True:
            m = "New polling loop for {o}"
            m = m.format(o=self)
            self.log.debug(m)

            if now_pct >= pct:
                m = "Reached {now_pct} out of {pct}, considering all answers in"
                m = m.format(now_pct=PCT_FMT(now_pct), pct=PCT_FMT(pct))
                self.log.info(m)
                break

            if datetime.datetime.utcnow() >= stop_dt:
                m = "Reached stop_dt {stop_dt}, considering all answers in"
                m = m.format(stop_dt=stop_dt)
                self.log.info(m)
                break

            if self.expiration["expired"]:
                m = "Reached expiration {expiration}, considering all answers in"
                m = m.format(expiration=self.expiration)
                self.log.info(m)
                break

            time.sleep(sleep)

            infos = self.answers_get_info()
            info = infos[0]
            now_pct = utils.tools.calc_percent(part=info.mr_passed, whole=this_total)

            m = [
                "Answers in {now_pct} out of {pct}",
                "{info.mr_passed} out of {this_total}",
                "estimated_total: {info.estimated_total}",
            ]
            m = ", ".join(m)
            m = m.format(
                now_pct=PCT_FMT(now_pct),
                pct=PCT_FMT(pct),
                info=info,
                this_total=this_total,
            )
            self.log.info(m)

        end = datetime.datetime.utcnow()
        elapsed = end - start
        m = [
            "Finished polling in: {dt}",
            "clients answered: {info.mr_passed}",
            "estimated clients: {info.estimated_total}",
            "rows in answers: {info.row_count}",
        ]
        m = ", ".join(m)
        m = m.format(dt=elapsed, info=info)
        self.log.info(m)
        return infos

    def answers_get_data(self, include_hashes=False):
        """Get the answers for this question.

        Args:
            include_hashes (:obj:`bool`, optional):
                Have the API include the hashes of rows values

                Defaults to: False.

        Notes:
            This will not use any paging, which means ALL answers will be returned
            in one API response. For large data sets of answers, this is unwise.

        Returns:
            :obj:`tantrum.api_models.ApiModel`: ResultDataList API Object

        """
        self._check_id()

        start = datetime.datetime.utcnow()
        result = self.adapter.cmd_get_result_data(
            obj=self.obj, include_hashes_flag=include_hashes
        )
        self._last_result = result

        end = datetime.datetime.utcnow()
        elapsed = end - start

        m = "Finished getting answers in {dt}"
        m = m.format(dt=elapsed)
        self.log.info(m)

        datas = result()
        self._last_datas = datas
        return datas

    def answers_get_data_paged(
        self, size=1000, cache_expiration=900, include_hashes=False
    ):
        """Get the answers for this question one page at a time.

        Args:
            size (:obj:`int`, optional):
                Size of each page to fetch at a time.

                Defaults to: 1000.
            cache_expiratio (:obj:`int`, optional):
                Have the API keep the cache_id that is created on initial get
                answers page alive for N seconds.

                Defaults to: 900.
            include_hashes (:obj:`bool`, optional):
                Have the API include the hashes of rows values

                Defaults to: False.

        Returns:
            :obj:`tantrum.api_models.ApiModel`: ResultDataList API Object

        """
        self._check_id()

        start = datetime.datetime.utcnow()

        row_start = 0
        row_count = size

        result = self.adapter.cmd_get_result_data(
            obj=self.obj,
            row_start=row_start,
            row_count=row_count,
            cache_expiration=cache_expiration,
            include_hashes_flag=include_hashes,
        )
        self._last_result = result

        datas = result()
        self._last_datas = datas

        data = datas[0]
        cache_id = data.cache_id
        page_count = 1
        row_start += row_count
        all_rows = data.rows

        m = "Received initial answers: {rows}"
        m = m.format(rows=data.rows)
        self.log.info(m)

        while True:
            time.sleep(1)

            page_result = self.adapter.cmd_get_result_data(
                obj=self.obj,
                row_start=row_start,
                row_count=row_count,
                cache_id=cache_id,
                cache_expiration=cache_expiration,
                include_hashes_flag=include_hashes,
            )
            self._last_result = page_result

            # this should catch errors where API returns result data as None sometimes
            # need to refetch data for N retries if that happens
            page_datas = page_result()
            self._last_datas = page_datas

            page_data = page_datas[0]

            page_rows = page_data.rows

            m = "Received page #{page_count} answers: {rows}"
            m = m.format(page_count=page_count, rows=len(page_rows or []))
            self.log.info(m)

            # this is less than ideal, should check page_data.row_count
            if not page_rows:
                m = "Received a page with no answers, considering all answers received"
                self.log.info(m)
                break

            all_rows += page_rows
            row_start += row_count
            page_count += 1

        end = datetime.datetime.utcnow()
        elapsed = end - start

        m = "Finished getting {rows} answers in {dt}"
        m = m.format(rows=len(all_rows or []), dt=elapsed)
        self.log.info(m)

        return datas

    def answers_get_data_sse_xml(self):
        return NotImplementedError

    def answers_get_data_sse_csv(self):
        return NotImplementedError

    def answers_get_data_sse_cef(self):
        return NotImplementedError

    def add_left_sensor(
        self, sensor, set_param_defaults=True, allow_empty_params=False
    ):
        """Add a sensor to the left hand side of the question.

        Args:
            sensor (:obj:`Sensor`):
                Sensor workflow object.
            set_param_defaults (:obj:`bool`, optional):
                If sensor has parameters defined, and no value is set,
                try to derive the default value from each parameters definition.

                Defaults to: True.
            allow_empty_params (:obj:`bool`, optional):
                If sensor has parameters defined, and the value is not set, "", or None,
                throw an exception.

                Defaults to: True.

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
        if self.params_defined or self.param_values:
            bits += [
                "params_defined={}".format(list(self.params_defined.keys())),
                "param_values={}".format(list(self.param_values.items())),
            ]
        bits = "({})".format(", ".join(bits))
        cls = ctmpl(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    @classmethod
    def get_by_name(cls, adapter, name, lvl="info"):
        """Get a sensor object by name.

        Args:
            adapter (:obj:`tantrum.adapters.Adapter`):
                Adapter to use for this workflow.
            name (:obj:`str`):
                Name of sensor to fetch.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        Returns:
            :obj:`Sensor`

        """
        result = adapter.cmd_get(obj=adapter.api_objects.Sensor(name=name))
        return cls(adapter=adapter, obj=result(), lvl=lvl, result=result)

    @classmethod
    def get_by_id(cls, adapter, id, lvl="info"):
        """Get a sensor object by id.

        Args:
            adapter (:obj:`tantrum.adapters.Adapter`):
                Adapter to use for this workflow.
            id (:obj:`int`):
                id of sensor to fetch.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        Returns:
            :obj:`Sensor`

        """
        result = adapter.cmd_get(obj=adapter.api_objects.Sensor(id=id))
        return cls(adapter=adapter, obj=result(), lvl=lvl, result=result)

    @property
    def params_defined(self):
        """Get the parameter definitions for this sensor.

        Notes:
            Will try to resolve a default value and store it in "derived_default" key
            for each parameter definition returned.

        Returns:
            :obj:`collections.OrderedDict`

        """
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
    def param_values(self):
        """Get all of the parameter key and values.

        Returns:
            :obj:`OrderedDict`

        """
        ret = OrderedDict()
        for k in self.params_defined:
            ret[k] = ""
        for p in self.params:
            ret[p.key] = p.value
        return ret

    @property
    def params(self):
        """Get the parameters that are set for this sensor.

        Returns:
            :obj:`tantrum.api_objects.ApiObjects`: ParameterList API object

        """
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
                Allow parameter keys that are not in the parameters definition
                for this sensor to be set.
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
        """Get the filter for this sensor.

        Returns:
            :obj:`tantrum.api_objects.ApiObjects`: Filter API object

        """
        if not hasattr(self, "_filter"):
            self._filter = self.api_objects.Filter()
            self._filter.sensor = self.api_objects.Sensor()
            self._filter.sensor.hash = self.obj.hash
        return self._filter

    @property
    def filter_vals(self):
        """Get the key value pairs of the filter for this sensor.

        Returns:
            :obj:`list` of :obj:`str`

        """
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
            if key not in self.param_values and set_param_defaults:
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
