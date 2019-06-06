# -*- coding: utf-8 -*-
"""Clients for making API requests to Tanium."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import six
import warnings

from . import exceptions
from .. import utils

WSDL_PATH = "/libraries/taniumjs/console.wsdl"
""":obj:`str`: URL path to find console.wsdl in :func:`get_wsdl`."""

warnings.simplefilter(action="once", category=exceptions.GetPlatformVersionWarning)
# only warn once about issues getting the platform version


@six.add_metaclass(abc.ABCMeta)
class ApiClient(object):
    """Abstract base class for all ApiClients."""

    @abc.abstractproperty
    def auth_method(self):
        """Get the AuthMethod for this object.

        Returns:
            :obj:`tantrum.auth_methods.AuthMethod`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`tantrum.http_client.HttpClient`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def url(self):
        """Get the URL from :attr:`ApiClient.http_client`.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def version(self):
        """Get the platform version from :attr:`ApiClient.config`.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def config(self):
        """Get the deserialized config.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def info(self):
        """Get the deserialized info.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover


class Soap(ApiClient):
    """Client for making SOAP API requests to Tanium."""

    def __init__(self, http_client, auth_method, lvl="info"):
        """Constructor.

        Args:
            http_client (:obj:`tantrum.http_client.HttpClient`):
                Object for sending HTTP requests.
            auth_method (:obj:`tantrum.auth_methods.AuthMethod`):
                Object for sending login and logout requests.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log for this object."""
        self._auth_method = auth_method
        self._http_client = http_client

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = ["url={!r}".format(self.url)]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    def __call__(
        self,
        data,
        path="/soap",
        method="post",
        timeout=30,
        headers=None,
        verify=None,
        save_last=None,
        save_history=None,
        log_request=None,
        log_response=None,
        cause="",
    ):
        """Get response of POST of data to /soap and return a response object.

        Args:
            data (:obj:`str`):
                Body to send in request.
            timeout (:obj:`int`, optional):
                Response timeout.

                Defaults to: 30.
            headers (:obj:`dict`):
                Headers to send in request.

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


        Returns:
            :obj:`requests.Response`

        """
        headers = headers or {}
        headers = {k: v for k, v in headers.items()}
        headers.update(self.auth_method.token_headers)
        r = self.http_client(
            method=method,
            path=path,
            data=data,
            headers=headers,
            timeout=timeout,
            verify=verify,
            save_last=save_last,
            save_history=save_history,
            log_request=log_request,
            log_response=log_response,
            cause=cause,
        )
        return r

    @property
    def auth_method(self):
        """Get the AuthMethod for this object.

        Returns:
            :obj:`tantrum.auth_methods.AuthMethod`

        """
        return self._auth_method

    @property
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`tantrum.http_client.HttpClient`

        """
        return self._http_client

    @property
    def url(self):
        """Get the URL from :attr:`ApiClient.http_client`.

        Returns:
            :obj:`str`

        """
        return self.http_client.url

    def version(self):
        """Get the platform version from :attr:`ApiClient.config`.

        Returns:
            :obj:`str`

        """
        if not getattr(self, "_version", None):
            self._version = get_version(self.http_client)
        return self._version

    def config(self):
        """Get the deserialized config.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        return get_config(self.http_client)

    def info(self):
        """Get the deserialized info.json from :attr:`ApiClient.url`.

        Returns:
            :obj:`dict`

        """
        return self.http_client(
            method="get",
            path="/info.json",
            headers=self.auth_method.token_headers,
            timeout=15,
        ).json()


def get_version(http_client):
    """Get serverVersion key from :func:`get_config`.

    Args:
        http_client (:obj:`tantrum.http_client.HttpClient`):
            Object for sending HTTP request.

    Raises:
        :exc:`exceptions.GetPlatformVersionWarning`:
            On error getting serverVersion key.

    Returns:
        :obj:`str`

    """
    cause = "Get platform version"
    try:
        return get_config(http_client=http_client, cause=cause)["serverVersion"]
    except Exception as exc:
        error = "Failed to get server version from url {url!r}, error: {exc}"
        error = error.format(url=http_client.url, exc=exc)
        warnings.warn(error, exceptions.GetPlatformVersionWarning)
        return ""


def get_wsdl(http_client):
    """Get response of GET to /libraries/taniumjs/console.wsdl.

    Args:
        http_client (:obj:`tantrum.http_client.HttpClient`):
            Object for sending HTTP request.

    Returns:
        :obj:`str`

    """
    path = WSDL_PATH
    return http_client(method="get", path=path, timeout=5).text


def get_config(http_client, cause=""):
    """Get response of GET to /config/console.json.

    Args:
        http_client (:obj:`tantrum.http_client.HttpClient`):
            Object for sending HTTP request.

    Returns:
        :obj:`dict`

    """
    path = "/config/console.json"
    return http_client(method="get", path=path, timeout=5, cause=cause).json()
