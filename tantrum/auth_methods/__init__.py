# -*- coding: utf-8 -*-
"""Authentication methods for the Tanium API."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import six
import re

from datetime import datetime, timedelta

from . import exceptions
from .. import utils


@six.add_metaclass(abc.ABCMeta)
class AuthMethod(object):
    """Abstract base class for all AuthMethods."""

    @abc.abstractproperty
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`tantrum.http_client.HttpClient`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def token(self):
        """Get or set a token.

        Notes:
            If no token received, :meth:`login` to get one.

            If token expired, :meth:`login` to get a new one.

            If token has been received, :meth:`validate` to validate token.

            If token fails validation, :meth:`login` to get a new one.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def token_headers(self):
        """Get dict with :attr:`token` for use in headers.

        Returns:
            :obj:`dict`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def uid(self):
        """Get user ID for token if a token has been received.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractproperty
    def logged_in(self):
        """Check if a token has been received.

        Returns:
            :obj:`bool`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def login(self, **kwargs):
        """Send a login request to receive a token.

        Raises:
            :exc:`exceptions.LoginError`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def logout(self, **kwargs):
        """Send a logout request to revoke a token.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def logout_all(self, **kwargs):
        """Send a logout request to revoke all tokens associated with this token.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def validate(self, **kwargs):
        """Send a validate request to check that token is still valid.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.InvalidToken`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        raise NotImplementedError  # pragma: no cover


class CommonMixin(object):
    """Shared methods common amongst all :class:`AuthMethod`."""

    def __init__(
        self,
        http_client,
        login_timeout=5,
        logout_timeout=5,
        expires_after=295,
        lvl="info",
    ):
        """Constructor.

        Args:
            http_client (:obj:`tantrum.http_client.HttpClient`):
                Object for sending HTTP requests.
            login_timeout (:obj:`int`, optional):
                Timeout for login and validate responses in seconds.

                Defaults to: 5.
            logout_timeout (:obj:`int`, optional):
                Timeout for logout responses in seconds.

                Defaults to: 5.
            expires_after (:obj:`int`, optional):
                Life of received tokens in seconds.

                Defaults to: 295.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log for this object."""

        self.revalidate_after = 5
        """:obj:`int`: Revalidate token if :attr:`last_used` is higher than this."""

        self._http_client = http_client
        self._login_timeout = login_timeout
        self._logout_timeout = logout_timeout
        self._expires_after = expires_after
        self._last_used = None
        self._token = None
        self.token = None

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = [
            "logged_in={}".format(self.logged_in),
            "last_used_secs={}".format(self.last_used_secs),
            "expiry_dt={}".format(self.expiry_dt),
        ]
        bits = "({})".format(", ".join(bits))
        cls = "{c.__module__}.{c.__name__}".format(c=self.__class__)
        return "{cls}{bits}".format(cls=cls, bits=bits)

    def __repr__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        return self.__str__()

    @property
    def http_client(self):
        """Get the HTTP Client for this object.

        Returns:
            :obj:`tantrum.http_client.HttpClient`

        """
        return self._http_client

    @property
    def token(self):
        """Get a token.

        Notes:
            If :attr:`logged_in` is False, :meth:`login` to get one.

            If :attr:`expired` is True, :meth:`login` to get a new one.

            If :attr:`logged_in` is True, and :attr:`last_used_secs` is older than
            :attr:`revalidate_after`, :meth:`validate` to re-validate token.

            If :meth:`validate` fails validation, :meth:`login` to get a new one.

        Returns:
            :obj:`str`

        """
        if not self.logged_in:
            self.login(cause="Initial login")
        elif self.expired:
            self.login(cause="Re-login due to expired token")
        else:
            if self.last_used_secs >= self.revalidate_after:
                try:
                    self.validate(cause="Validate existing token")
                except exceptions.InvalidToken:
                    m = "Token for User ID {uid!r} no longer valid, getting new one"
                    m = m.format(uid=self.uid)
                    self.log.debug(m)
                    self.login(cause="Re-login due to invalid token")
        return self._token

    @token.setter
    def token(self, value):
        """Set the token to value.

        Args:
            value (:obj:`str`):
                Value to set _token to

        """
        self._token = value
        self._last_used = None if value is None else datetime.utcnow()

    @property
    def token_headers(self):
        """Get dict with :attr:`token` for use in headers.

        Returns:
            :obj:`dict`

        """
        return {"session": self.token}

    @property
    def uid(self):
        """Get user ID for token if a token has been received.

        Returns:
            :obj:`str`

        """
        return int((self._token or self.token).split("-")[0])

    @property
    def logged_in(self):
        """Check if a token has been received.

        Returns:
            :obj:`bool`

        """
        return True if self._token else False

    @property
    def expiry_dt(self):
        delta = timedelta(seconds=self._expires_after)
        return None if not self._last_used else self._last_used + delta

    @property
    def expired(self):
        """Check if token has expired.

        Returns:
            :obj:`bool`

        """
        return True if not self._last_used else datetime.utcnow() >= self.expiry_dt

    @property
    def last_used_secs(self):
        """Get the number of seconds since token was issued or last used.

        Returns:
            :obj:`int`

        """
        return (
            0 if not self._last_used else (datetime.utcnow() - self._last_used).seconds
        )

    def login(self, **kwargs):
        """Send a login request to receive a token.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Get new token".

        Raises:
            :exc:`exceptions.LoginError`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        r = self.http_client(
            path="/auth",
            method="post",
            headers={k: v for k, v in self._headers.items() if v},
            b64_headers=self._b64_headers,
            timeout=self._login_timeout,
            cause=kwargs.pop("cause", "Get new token"),
        )

        if r.status_code != 200:
            raise exceptions.LoginError(auth_method=self, response=r)

        self.token = r.text
        m = "Token received for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        return r.text

    def logout(self, **kwargs):
        """Send a logout request to revoke a token.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Revoke token".
                headers (:obj:`dict`):
                    Headers to send in request.

                    Defaults to: {}.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        if not self.logged_in:
            raise exceptions.NotLoggedInError(auth_method=self)

        r = self.http_client(
            path="/auth",
            method="post",
            headers={"session": self._token, "logout": "0"},
            b64_headers=self._b64_headers,
            timeout=self._logout_timeout,
            cause=kwargs.pop("cause", "Revoke token"),
        )

        if r.status_code != 200:
            raise exceptions.LogoutError(auth_method=self, response=r)

        m = "Token revoked for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        self.token = None
        return None

    def logout_all(self, **kwargs):
        """Send a logout request to revoke all tokens associated with this token.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Revoke all tokens".
                headers (:obj:`dict`):
                    Headers to send in request.

                    Defaults to: {}.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.LogoutError`:
                If status code in response is not 200.

        Returns:
            None

        """
        if not self.logged_in:
            raise exceptions.NotLoggedInError(auth_method=self)

        r = self.http_client(
            path="/auth",
            method="post",
            headers={"session": self._token, "logout": "1"},
            b64_headers=self._b64_headers,
            timeout=self._logout_timeout,
            cause=kwargs.pop("cause", "Revoke all tokens"),
        )

        if r.status_code != 200:
            raise exceptions.LogoutError(auth_method=self, response=r)

        m = "All tokens revoked for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        self.token = None
        return None

    def validate(self, **kwargs):
        """Send a validate request to check that token is still valid.

        Args:
            **kwargs:
                cause (:obj:`str`):
                    String to explain purpose of request.

                    Defaults to: "Validate token".
                headers (:obj:`dict`):
                    Headers to send in request.

                    Defaults to: {}.

        Raises:
            :exc:`exceptions.NotLoggedInError`:
                If :attr:`logged_in` is False.
            :exc:`exceptions.InvalidToken`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        if not self.logged_in:
            raise exceptions.NotLoggedInError(auth_method=self)

        r = self.http_client(
            path="/auth",
            method="post",
            headers={"session": self._token},
            timeout=self._login_timeout,
            cause=kwargs.pop("cause", "Validate token"),
        )

        if r.status_code != 200:
            raise exceptions.InvalidToken(auth_method=self, response=r)

        m = "Token validated for User ID {uid!r} from {url!r}"
        m = m.format(uid=self.uid, url=r.url)
        self.log.debug(m)
        self.token = r.text
        return r.text


class Credentials(CommonMixin, AuthMethod):
    """Method that uses credentials to interact with the '/auth' API."""

    def __init__(
        self,
        http_client,
        username,
        password,
        domain="",
        secondary="",
        login_timeout=5,
        logout_timeout=5,
        expires_after=295,
        lvl="info",
    ):
        """Constructor.

        Args:
            http_client (:obj:`tantrum.http_client.HttpClient`):
                HTTP client.
            username (:obj:`str`):
                Header to pass to /auth API.
            password (:obj:`str`):
                Header to pass to /auth API.
            domain (:obj:`str`, optional):
                Header to pass to /auth API.

                Defaults to: ""
            secondary (:obj:`str`, optional):
                Header to pass to /auth API.

                Defaults to: ""
            login_timeout (:obj:`int`, optional):
                Timeout for login and validate responses in seconds.

                Defaults to: 5.
            logout_timeout (:obj:`int`, optional):
                Timeout for logout responses in seconds.

                Defaults to: 5.
            expires_after (:obj:`int`, optional):
                Life of received tokens in seconds.

                Defaults to: 295.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self._headers = {
            "username": username,
            "password": password,
            "domain": domain,
            "secondary": secondary,
        }
        self._b64_headers = ["username", "password"]
        super(Credentials, self).__init__(
            http_client=http_client,
            login_timeout=login_timeout,
            logout_timeout=logout_timeout,
            expires_after=expires_after,
            lvl=lvl,
        )


class SessionId(CommonMixin, AuthMethod):
    """Method that uses session id to interact with the '/auth' API."""

    def __init__(
        self,
        http_client,
        session,
        login_timeout=5,
        logout_timeout=5,
        expires_after=295,
        lvl="info",
    ):
        """Constructor.

        Args:
            http_client (:obj:`tantrum.http_client.HttpClient`):
                HTTP client.
            session (:obj:`str`):
                Header to pass to /auth API.
            login_timeout (:obj:`int`, optional):
                Timeout for login and validate responses in seconds.

                Defaults to: 5.
            logout_timeout (:obj:`int`, optional):
                Timeout for logout responses in seconds.

                Defaults to: 5.
            expires_after (:obj:`int`, optional):
                Life of received tokens in seconds.

                Defaults to: 295.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".

        """
        self._headers = {"session": session}
        self._b64_headers = []
        super(SessionId, self).__init__(
            http_client=http_client,
            login_timeout=login_timeout,
            logout_timeout=logout_timeout,
            expires_after=expires_after,
            lvl=lvl,
        )
        self.token = session

    @property
    def token(self):
        """Get a token.

        Notes:
            If :attr:`CommonMixin.logged_in` is False, can not login to get a
            new one with just a session.

            If :attr:`CommonMixin.expired` is True, can not login to get
            a new one with just a session.

            If :attr:`CommonMixin.logged_in` is True, and
            :attr:`CommonMixin.last_used_secs` is older than
            :attr:`CommonMixin.revalidate_after`,
            :meth:`CommonMixin.validate` to re-validate token.

            If :meth:`CommonMixin.validate` fails validation, can not login
            to get a new one with just a session.

        Returns:
            :obj:`str`

        """
        if self.last_used_secs is None or self.last_used >= self.revalidate_after:
            self.validate(cause="Validate existing token")
        return self._token

    @token.setter
    def token(self, value):
        """Set the token to value and :attr:`CommonMixin.last_used` to now.

        Args:
            value (:obj:`str`):
                Value to set _token to

        """
        self._token = value
        if value is None:
            self._last_used = None
            self._last_validated = None
        else:
            self._last_used = datetime.utcnow()
            self._last_validated = datetime.utcnow()

    def login(self, **kwargs):
        """Send a login request to receive a token.

        Raises:
            :exc:`exceptions.LoginError`:
                If status code in response is not 200.

        Returns:
            :obj:`str`

        """
        error = "Unable to perform a login with a session ID, can only validate"
        raise NotImplementedError(error)


def validate_token(token):
    """Validate that a token is properly formed.

    Args:
        token (:obj:`str`):
            Token to validate

    Returns:
        :obj:`bool`

    """
    return re.match(r"(\d+-\d+-)\w+", token) is not None
