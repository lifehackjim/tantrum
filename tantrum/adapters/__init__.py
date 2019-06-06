# -*- coding: utf-8 -*-
"""Adapter objects that serialize requests to the Tanium API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import re
import six
import warnings
import xmltodict

from . import exceptions
from .. import api_models
from .. import results
from .. import utils


@six.add_metaclass(abc.ABCMeta)
class Adapter(object):
    """Abstract base class for all Adapters."""

    @abc.abstractproperty
    def api_objects(self):
        """Get the API objects container.

        Returns:
            :obj:`tantrum.api_objects.ApiObjects`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def api_client(self):
        """Get the API client.

        Returns:
            :obj:`tantrum.api_clients.ApiClient`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def http_client(self):
        """Get the HTTP client.

        Returns:
            :obj:`tantrum.http_client.HttpClient`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def auth_method(self):
        """Get the Auth Method.

        Returns:
            :obj:`tantrum.auth_methods.AuthMethod`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def result_cls(cls):
        """Get the result deserializer class.

        Returns:
            :class:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_get(self, obj, **kwargs):
        """Send an API request to get an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_add(self, obj, **kwargs):
        """Send an API request to add an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_delete(self, obj, **kwargs):
        """Send an API request to delete an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_update(self, obj, **kwargs):
        """Send an API request to update an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_get_audit_logs(self, type, target, **kwargs):
        """Send an API request to get audit logs for an object.

        Args:
            type (:obj:`str`):
                Type of object to get audit logs of.
            target (:obj:`int`):
                ID of object type to get audit logs for.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_get_client_count(self, **kwargs):
        """Send an API request to get the client count.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_parse_question(self, text, **kwargs):
        """Send an API request to parse text.

        Args:
            text (:obj:`str`):
                Text to parse into question objects.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_add_parsed_question(self, obj, **kwargs):
        """Send an API request to add a parsed question object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_get_result_info(self, obj, **kwargs):
        """Send an API request to get result info for an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_get_result_data(self, obj, **kwargs):
        """Send an API request to get result data for an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def cmd_get_merged_result_data(self, objlist, **kwargs):
        """Send an API request to get merged result data for a list of objects.

        Args:
            objlist (:obj:`list`):
                List of API Objects to use for request.

        Returns:
            :obj:`tantrum.results.Result`

        """
        raise NotImplementedError  # pragma: no cover


class Soap(Adapter):
    """Tanium SOAP request adapter."""

    DEFAULT_OPTIONS = {}
    """:obj:`dict`: Default options to use in :meth:`build_options_from_kwargs`."""

    AUDIT_LOG_TYPES = [
        "authentication",
        "content_set",
        "content_set_role",
        "content_set_role_privilege",
        "dashboard",
        "dashboard_group",
        "group",
        "package_spec",
        "plugin_schedule",
        "saved_action",
        "saved_question",
        "sensor",
        "system_setting",
        "user",
        "user_group",
        "white_listed_url",
    ]
    """:obj:`list` of :obj:`str`: Valid types for :meth:`api_get_audit_logs`."""

    def __init__(self, api_client, api_objects, lvl="info"):
        """Constructor.

        Args:
            api_client (:obj:`tantrum.api_clients.ApiClient`):
                Client to use for sending API requests.
            api_objects (:obj:`tantrum.api_objects.ApiObjects`):
                API objects container to use for this adapter.
            lvl (:obj:`str`, optional):
                Logging level.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log."""

        self._api_objects = api_objects
        self._api_client = api_client

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "api_objects={!r}".format(self.api_objects),
            "api_client={!r}".format(self.api_client),
            "http_client={!r}".format(self.http_client),
            "auth_method={!r}".format(self.auth_method),
        ]
        bits = "(\n  {},\n)".format(",\n  ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    @property
    def api_objects(self):
        """Get the API objects container.

        Returns:
            :obj:`tantrum.api_objects.ApiObjects`

        """
        return self._api_objects

    @property
    def api_client(self):
        """Get the API client.

        Returns:
            :obj:`tantrum.api_clients.ApiClient`

        """
        return self._api_client

    @property
    def http_client(self):
        """Get the HTTP client.

        Returns:
            :obj:`tantrum.http_client.HttpClient`

        """
        return self.api_client.http_client

    @property
    def auth_method(self):
        """Get the Auth Method.

        Returns:
            :obj:`tantrum.auth_methods.AuthMethod`

        """
        return self.api_client.auth_method

    @property
    def result_cls(cls):
        """Get the result deserializer class.

        Returns:
            :class:`tantrum.results.Result`

        """
        return results.Soap

    def build_options_from_kwargs(self, **kwargs):
        """Build an Options API object from kwargs and return the serialized form.

        Args:
            **kwargs:
                options_obj (:obj:`tantrum.api_models.ApiItem`):
                    A pre-established Options object.

                    Defaults to: new Options object from :attr:`api_objects`.
                rest of kwargs:
                    Set on Options object if key is an attr on object and attrs value
                    is None.

        Notes:
            Will set :attr:`DEFAULT_OPTIONS` as defaults to kwargs
            before applying values to Options object attributes.

        Returns:
            :obj:`dict`

        """
        default_options = getattr(self, "DEFAULT_OPTIONS", {}) or {}
        for k, v in default_options.items():
            kwargs.setdefault(k, v)
        opts = kwargs.pop("options_obj", self.api_objects.Options())
        check_object_type(obj=opts, types=(self.api_objects.Options,))
        for k in list(kwargs):
            if hasattr(opts, k) and getattr(opts, k, None) is None:
                setattr(opts, k, kwargs[k])
        return opts.serialize(wrap_name=False)

    def send(
        self,
        obj,
        cmd,
        body_re_limit=4000,
        ser_only_attrs=None,
        ser_exclude_attrs=None,
        ser_empty=None,
        ser_list_attrs=None,
        ser_wrap_name=None,
        ser_wrap_item_attr=None,
        verify=None,
        save_last=None,
        save_history=None,
        log_request=None,
        log_response=None,
        cause="",
        **kwargs
    ):
        """Build and send a SOAP API request.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                ApiModel to serialize and send as part of request.
            cmd (:obj:`str`):
                SOAP Command to use in request.
            body_re_limit (:obj:`int`):
                Value to limit regex search of response body for <session> tag.

                Defaults to: 4000.
            ser_empty (:obj:`bool`):
                Include attributes that have a value of None when serializing.
                Uses False if None.

                Defaults to: None.
            ser_list_attrs (:obj:`bool`):
                Include simple attributes of :obj:`tantrum.api_models.ApiList`
                when serializing.
                Uses False if None.

                Defaults to: None.
            ser_exclude_attrs (:obj:`list` of :obj:`str`):
                Exclude these attributes when serializing.
                Uses [] if None.

                Defaults to: None.
            ser_only_attrs (:obj:`list` of :obj:`str`):
                Include only these attributes when serializing.
                Uses [] if None.

                Defaults to: None.
            ser_wrap_name (:obj:`bool`):
                Wrap the return in another dict whose key is set to the API name.
                Uses True if None.

                Defaults to: None.
            ser_wrap_item_attr (:obj:`bool`):
                Wrap list items in dict whose key is set to the API list
                item attribute.
                Uses True if None.

                Defaults to: None.
            verify (:obj:`bool` or :obj:`str`, optional):
                Enable SSL certification validation.
                If None uses :attr:`tantrum.http_client.HttpClient.verify`.

                Defaults to: None.
            save_last (:obj:`bool`, optional):
                Save last request to :attr:`HttpClient.last_request` and last response
                to :attr:`HttpClient.last_response`.
                If None uses :attr:`tantrum.http_client.HttpClient.save_last`.

                Defaults to: None.
            save_history (:obj:`bool`, optional):
                Append last response to :attr:`HttpClient.history`.
                If None uses :attr:`tantrum.http_client.HttpClient.save_history`.

                Defaults to: None.
            log_request (:obj:`bool`, optional):
                Log request details to debug level.
                If None uses :attr:`tantrum.http_client.HttpClient.log_request`.

                Defaults to: None.
            log_response (:obj:`bool`, optional):
                Log response details to debug level.
                If None uses :attr:`tantrum.http_client.HttpClient.log_response`.

                Defaults to: None.
            cause (:obj:`str`, optional):
                String to explain purpose of request.

                Defaults to: "".
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`build_options_from_kwargs`.

        Raises:
            :obj:`exceptions.SessionNotFoundWarning`:
                If the <session> tag can not be found in the response body.

        Returns:
            :obj:`tantrum.results.Result`

        """
        ser_only_attrs = utils.tools.def_none(ser_only_attrs, [])
        ser_exclude_attrs = utils.tools.def_none(ser_exclude_attrs, [])
        ser_empty = utils.tools.def_none(ser_empty, False)
        ser_list_attrs = utils.tools.def_none(ser_list_attrs, False)
        ser_wrap_name = utils.tools.def_none(ser_wrap_name, True)
        ser_wrap_item_attr = utils.tools.def_none(ser_wrap_item_attr, True)

        if isinstance(obj, api_models.ApiModel):
            obj = obj.serialize(
                only_attrs=ser_only_attrs,
                exclude_attrs=ser_exclude_attrs,
                empty=ser_empty,
                list_attrs=ser_list_attrs,
                wrap_name=ser_wrap_name,
                wrap_item_attr=ser_wrap_item_attr,
            )

        opts = self.build_options_from_kwargs(**kwargs)

        request_dict = soap_envelope(cmd=cmd, obj=obj, opts=opts)
        request_body = serialize_xml(obj=request_dict)

        r = self.api_client(
            data=request_body,
            verify=verify,
            log_request=log_request,
            log_response=log_response,
            save_last=save_last,
            save_history=save_history,
            cause=cause,
        )

        try:
            auth_token = re_soap_tag(text=r.text, tag="session", limit=body_re_limit)
        except Exception:
            auth_token = ""

        if auth_token:
            self.api_client.auth_method.token = auth_token
        else:
            if body_re_limit:
                limit = "the first {}".format(body_re_limit)
            else:
                limit = "ALL"
            error = "XML tag 'session' not in {limit} characters of SOAP response body"
            error = error.format(limit=limit)
            warnings.warn(error, exceptions.SessionNotFoundWarning)
        return self.result_cls.from_response(
            api_objects=self.api_objects, response=r, lvl=self.log.level
        )

    def cmd_get(self, obj, **kwargs):
        """Send an API request to get an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        check_object_type(
            obj=obj, types=(self.api_objects.ApiItem, self.api_objects.ApiList)
        )
        kwargs["cmd"] = "GetObject"
        return self.send(obj=obj, **kwargs)

    def cmd_add(self, obj, **kwargs):
        """Send an API request to add an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))
        kwargs["cmd"] = "AddObject"
        kwargs["ser_exclude_attrs"] = ["id"]
        return self.send(obj=obj, **kwargs)

    def cmd_delete(self, obj, **kwargs):
        """Send an API request to delete an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))
        check_object_attrs(obj=obj, attrs=["id", "name"])
        kwargs["cmd"] = "DeleteObject"
        return self.send(obj=obj, **kwargs)

    def cmd_update(self, obj, **kwargs):
        """Send an API request to update an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ApiItem,))
        check_object_attrs(obj=obj, attrs=["id", "name"])
        kwargs["cmd"] = "UpdateObject"
        return self.send(obj=obj, **kwargs)

    def cmd_get_audit_logs(self, type, target, **kwargs):
        """Send an API request to get audit logs for an object.

        Args:
            type (:obj:`str`):
                Type of object to get audit logs of.
            target (:obj:`int`):
                ID of object type to get audit logs for.
                SOAP allows target of 'None' to get all objects of `type`.
            **kwargs:
                count (:obj:`int`):
                    Limit number of audit logs returned to this.

                    Defaults to: 1.
                rest of kwargs:
                    Passed to :meth:`send`.

        Raises:
            :exc:`exceptions.InvalidTypeError`:
                If type is not one of :attr:`AUDIT_LOG_TYPES`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        if type not in self.AUDIT_LOG_TYPES:
            error = "Invalid object type {ot} - MUST be one of {at}"
            error = error.format(at=self.AUDIT_LOG_TYPES, ot=type)
            raise exceptions.InvalidTypeError(error)

        obj = self.api_objects.AuditLog(type="{t}_audit".format(t=type), id=target)
        kwargs.setdefault("audit_history_size", kwargs.pop("count", 1))
        kwargs["cmd"] = "GetObject"
        return self.send(obj=obj, **kwargs)

    def cmd_get_client_count(self, **kwargs):
        """Send an API request to get the client count.

        Args:
            **kwargs:
                count (:obj:`int`):
                    Number of days to get client count for.

                    Defaults to: 30.
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        obj = {"client_count": kwargs.pop("count", 30)}
        kwargs["cmd"] = "GetObject"
        return self.send(obj=obj, **kwargs)

    def cmd_parse_question(self, text, **kwargs):
        """Send an API request to parse text.

        Args:
            text (:obj:`str`):
                Text to parse into question objects.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        check_object_type(obj=text, types=six.string_types)
        obj = self.api_objects.ParseJob(question_text=text)
        kwargs["cmd"] = "AddObject"
        return self.send(obj=obj, **kwargs)

    def cmd_add_parsed_question(self, obj, **kwargs):
        """Send an API request to add a parsed question object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        check_object_type(obj=obj, types=(self.api_objects.ParseResultGroup,))
        obj = obj.question
        kwargs["cmd"] = "AddObject"
        return self.send(obj=obj, **kwargs)

    def cmd_get_result_info(self, obj, **kwargs):
        """Send an API request to get result info for an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        types = (
            self.api_objects.Question,
            self.api_objects.SavedQuestion,
            self.api_objects.Action,
            self.api_objects.SavedAction,
        )
        check_object_type(obj=obj, types=types)
        check_object_attrs(obj=obj, attrs=["id", "name"])
        kwargs["cmd"] = "GetResultInfo"
        kwargs["ser_only_attrs"] = ["id", "name"]
        return self.send(obj=obj, **kwargs)

    def cmd_get_result_data(self, obj, **kwargs):
        """Send an API request to get result data for an object.

        Args:
            obj (:obj:`tantrum.api_models.ApiModel`):
                API Object to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        types = (
            self.api_objects.Question,
            self.api_objects.SavedQuestion,
            self.api_objects.Action,
            self.api_objects.SavedAction,
        )
        check_object_type(obj=obj, types=types)
        check_object_attrs(obj=obj, attrs=["id", "name"])
        kwargs["cmd"] = "GetResultData"
        kwargs["ser_only_attrs"] = ["id", "name"]
        return self.send(obj=obj, **kwargs)

    def cmd_get_merged_result_data(self, objlist, **kwargs):
        """Send an API request to get merged result data for a list of objects.

        Args:
            objlist (:obj:`list`):
                List of API Objects to use for request.
            **kwargs:
                rest of kwargs:
                    Passed to :meth:`send`.

        Returns:
            :obj:`tantrum.results.Result`

        """
        list_types = (
            list,
            tuple,
            self.api_objects.SavedQuestionList,
            self.api_objects.QuestionList,
        )
        check_object_type(obj=objlist, types=list_types)

        item_types = (self.api_objects.Question, self.api_objects.SavedQuestion)
        pobjlist = [objlist] if isinstance(objlist, item_types) else objlist

        objs = {"question": [], "saved_question": []}
        only_attrs = ["id", "name", "index", "cache_row_id"]
        sargs = {
            "ser_wrap_name": False,
            "ser_wrap_item_attr": False,
            "ser_only_attrs": only_attrs,
        }
        idx = 0
        for pobj in pobjlist:
            sobjlist = [pobj] if isinstance(pobj, item_types) else pobj
            for sobj in sobjlist:
                check_object_type(obj=sobj, types=item_types)
                check_object_attrs(obj=sobj, attrs=["id", "name"])
                sobj.index = idx
                sobj.cache_row_id = getattr(sobj, "cache_row_id", None) or 0
                sobj_dict = sobj.serialize(**sargs)
                objs_target = sobj.API_NAME
                objs[objs_target].append(sobj_dict)
                idx += 1

        kwargs["cmd"] = "GetMergedResultData"
        return self.send(obj=objs, **kwargs)


def soap_envelope(cmd, obj, opts=None):
    """Construct a SOAP envelope with the request command, obj, and options.

    Args:
        cmd (:obj:`str`):
            Command to use for request.
        obj (:obj:`dict`):
            Object(s) to use for request.
        options (:obj:`dict`, optional):
            Options to use for request.

            Defaults to: None.

    Returns:
        :obj:`dict`

    """
    request = {"command": cmd, "object_list": obj, "options": opts}

    body = {
        "@xmlns:t": "urn:TaniumSOAP",
        "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "t:tanium_soap_request": request,
    }
    env = {
        "@soap:encodingStyle": "http://schemas.xmlsoap.org/soap/encoding/",
        "@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/",
        "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
        "soap:Body": body,
    }
    ret = {"soap:Envelope": env}
    return ret


def re_soap_tag(text, tag, limit=4000, pattern=r"<{t}>(.*?)</{t}>"):
    """Search for tag in text[:limit] using pattern.

    Args:
        text (:obj:`str`):
            Text to search for pattern.
        tag (:obj:`str`):
            Tag name to use in pattern as 't'.
        limit (:obj:`int`, optional):
            Length to limit text to when searching for pattern.

            Defaults to: 4000.
        pattern (:obj:`str`, optional):
            Pattern to use when searching for tag.

            Defaults to: r'<{e}>(.*?)</{e}>'

    Notes:
        Given text is 4 GB and pattern is expected at top of text:
            * if head is None and pattern not found: 131 seconds
            * if head is None and pattern found: 0 seconds
            * if head is 4000 and pattern not found: 0 seconds
            * if head is 4000 and pattern found: 0 seconds

    Returns:
        :obj:`str`

    """
    pattern_txt = pattern.format(t=tag)
    pattern_re = re.compile(pattern_txt, re.IGNORECASE | re.DOTALL)
    text_limit = text[:limit]
    match = pattern_re.search(text_limit)
    return match.group(1) if match else ""


def check_object_type(obj, types):
    """Check if an obj is an instance of types.

    Args:
        obj (:obj:`object`):
            Object to check against types.
        types (:obj:`tuple` of :obj:`type`):
            Types to check against obj.

    Raises:
        :exc:`exceptions.InvalidTypeError`:
            If type of obj is not on of types.

    """
    if not isinstance(obj, types):
        error = "Invalid object type {ot} - MUST be one of {at}"
        error = error.format(at=types, ot=type(obj))
        raise exceptions.InvalidTypeError(error)


def check_object_attrs(obj, attrs):
    """Check if any attributes of an obj are set.

    Args:
        obj (:obj:`tantrum.api_models.ApiModel`):
            API object to check.
        attrs (:obj:`list` of :obj:`str`):
            Attributes to check on obj.

    Raises:
        :exc:`exceptions.EmptyAttributeError`:
            If none of the attributes in attrs on obj are not set to None.

    """
    if isinstance(obj, api_models.ApiItem):
        if not any(getattr(obj, x, None) is not None for x in attrs):
            error = "No attributes in {a} defined on {o}"
            error = error.format(a=attrs, o=obj)
            raise exceptions.EmptyAttributeError(error)


def serialize_xml(obj, **kwargs):
    """Encode python object into an XML string.

    Args:
        obj (:obj:`object`):
            Python object to encode into a string.
        **kwargs:
            full_document (:obj:`bool`):
                Include xml stanza at top.

                Defaults to: True.
            pretty (:obj:`bool`):
                Indent the output doc.

                Defaults to: True.
            rest of kwargs:
                Passed to xmltodict.unparse.

    Returns:
        :obj:`str`

    """
    kwargs.setdefault("full_document", True)
    kwargs.setdefault("pretty", True)
    return xmltodict.unparse(obj, **kwargs)
