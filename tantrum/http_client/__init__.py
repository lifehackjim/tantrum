# -*- coding: utf-8 -*-
"""Client for making HTTP requests."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests

from . import exceptions
from .. import utils
from .. import version


class HttpClient(object):
    """Convenience class for requests package."""

    def __init__(self, url, verify=True, timeout=5, lvl="info"):
        """Constructor.

        Args:
            url (:obj:`str`):
                URL to use.
            timeout (:obj:`int`, optional):
                Connect timeout to use for requests.

                Defaults to: 5.
            lvl (:obj:`str`, optional):
                Logging level for this object.

                Defaults to: "info".
            verify (:obj:`bool` or :obj:`str`, optional):
                Enable/Disable SSL certificate validation using built in CAs,
                or a path to custom cert.

                Defaults to: True.

        Notes:
            If verify is True or None, verification is done using default/built in
            CA. OS env vars $REQUESTS_CA_BUNDLE, and $CURL_CA_BUNDLE are used if set
            and trust_env is True, and if trust_env is False session's verify is used.

            If verify is False, no verification is done. This overrides OS env and
            session's verify for this request and no verification is done at all.
            Don't do this.

            If verify is a str, verification is done with PEM file at path.
            This overrides OS env and session's verify for this request.

            Caveat: If previous request made with session and close has not been
            called on session, the verify of the previous request will be used
            no matter what is supplied here.

        """
        self.log = utils.logs.get_obj_log(obj=self, lvl=lvl)
        """:obj:`logging.Logger`: Log for this object."""
        self.timeout = timeout
        """:obj:`int`: Connect timeout used for all requests."""
        self.parsed_url = self.parse_url(url)
        """:obj:`UrlParser`: Parsed version of URL."""
        self.last_request = None
        """:obj:`requests.PreparedRequest`: Last request sent."""
        self.last_response = None
        """:obj:`requests.Response`: Last response received."""
        self.history = []
        """:obj:`list`: History of all responses received.

        Used by :meth:`HttpClient.response_hook_history`.
        """
        self.verify = verify
        """:obj:`bool`: SSL Verification."""

        self.session = requests.Session()
        """:obj:`requests.Session`: Requests session object."""

    @property
    def url(self):
        """Get the URL string from :attr:`HttpClient.parsed_url`.

        Returns:
            :obj:`str`

        """
        return self.parsed_url.url

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
        method="get",
        path="",
        data=None,
        timeout=5,
        params=None,
        headers=None,
        b64_headers=None,
        **kwargs
    ):
        """Create, prepare a request, and then send it.

        Args:
            method (:obj:`str`, optional):
                Method to use.

                Defaults to: "get".
            path (:obj:`str`, optional):
                Path to append to :attr:`HttpClient.url` for this request.

                Defaults to: "".
            data (:obj:`str`, optional):
                Data to send with POST.

                Defaults to: None.
            timeout (:obj:`int`, optional):
                Response timeout.

                Defaults to: 5.
            params (:obj:`dict`, optional):
                URL parameters.

                Defaults to: None.
            headers (:obj:`dict`, optional):
                Headers.

                Defaults to: None.
            b64_headers (:obj:`list` of :obj:`str`, optional):
                Headers to base 64 encode.

                Defaults to: None.
            **kwargs:
                cause (:obj:`str`): String to explain purpose of request.

                Defaults to: "".

        Returns:
            :obj:`requests.Response`

        """
        cause = kwargs.pop("cause", "")
        verify = kwargs.pop("verify", self.verify)
        b64 = b64_headers or []

        h = {}
        h.update(headers or {})
        h.setdefault("User-Agent", self.user_agent)
        h.update({k: utils.tools.b64_encode(v) for k, v in h.items() if k in b64})

        req_args = {}
        req_args["url"] = requests.compat.urljoin(self.url, path)
        req_args["method"] = method
        req_args["data"] = data
        req_args["headers"] = h
        req_args["params"] = params

        send_args = {}
        send_args["timeout"] = (self.timeout, timeout)
        send_args.update(
            self.session.merge_environment_settings(
                url=self.url,
                proxies=None,  # rely on OS env proxies, then self.session.proxies
                stream=None,  # not using
                verify=verify,
                cert=None,  # rely on client cert set in self.session.cert
            )
        )

        request = requests.Request(**req_args)
        prequest = self.last_request = self.session.prepare_request(request=request)
        prequest.cause = cause

        m = "sent: url={p.url!r}, method={p.method!r}, size={size}"
        m = m.format(p=prequest, size=len(prequest.body or ""))
        self.log.debug(m)

        r = self.last_response = self.session.send(prequest, **send_args)
        r.cause = cause
        return r

    def control_hook(self, enable, hook):
        """Add or remove a hook from :attr:`HttpClient.session`.

        Args:
            enable (:obj:`bool`):
                True: Add hook to session.
                False: Remove hook from session.
            hook (:obj:`object`):
                Hook function to add/remove to session.

        Returns:
            :obj:`bool`:
                True/False if hook was actually removed/added.

        """
        ret = False
        self.session.hooks = getattr(self.session, "hooks", {}) or {}
        self.session.hooks["response"] = self.session.hooks.get("response", [])
        if enable:
            if hook not in self.session.hooks["response"]:
                self.session.hooks["response"].append(hook)
                ret = True
        else:
            if hook in self.session.hooks["response"]:
                self.session.hooks["response"].remove(hook)
                ret = True
        return ret

    def response_hook_log_debug(self, response, *args, **kwargs):
        """Response hook to log info.

        Args:
            response (:obj:`requests.Response`):
                Response to process.
            *args:
                Unused, yet supplied by :obj:`requests.Session`.
            **kwargs:
                Unused, yet supplied by :obj:`requests.Session`.

        Returns:
            :obj:`requests.Response`

        """
        m = (
            "rcvd: url={response.url!r}, method={request.method!r}, size={size}, "
            "status={response.status_code!r}, reason={response.reason!r}, "
            "elapsed={response.elapsed}, cause={cause!r}"
        )
        m = m.format(
            response=response,
            request=response.request,
            size=len(response.text or ""),
            cause=getattr(response, "cause", ""),
        )
        self.log.debug(m)
        return response

    def response_hook_history(self, response, *args, **kwargs):
        """Response hook to add response to :attr:`HttpClient.history`.

        Args:
            response (:obj:`requests.Response`):
                Response to process.
            *args:
                Unused, yet supplied by :obj:`requests.Session`.
            **kwargs:
                Unused, yet supplied by :obj:`requests.Session`.
        """
        self.history = getattr(self, "history", [])
        self.history.append(response)

    def parse_url(self, url):
        """Parse a URL using UrlParser.

        Args:
            url (:obj:`str`):
                URL to parse.

        Returns:
            :obj:`UrlParser`

        """
        parsed_url = UrlParser(url=url, default_scheme="https")
        m = "Parsed url {old!r} into {new!r} using {parsed}"
        m = m.format(old=url, new=parsed_url.url, parsed=parsed_url)
        self.log.debug(m)
        return parsed_url

    @property
    def user_agent(self):
        """Build a user agent string for use in headers.

        Returns:
            :obj:`str`

        """
        return "{pkg}.{name}/{ver}".format(
            pkg=__name__.split(".")[0],
            name=self.__class__.__name__,
            ver=version.__version__,
        )


class UrlParser(object):
    """Parse a URL and ensure it has the neccessary bits."""

    def __init__(self, url, default_scheme=""):
        """Constructor.

        Args:
            url (:obj:`str`):
                URL to parse
            default_scheme (:obj:`str`, optional):
                If no scheme in URL, use this.

                Defaults to: ""

        Raises:
            :exc:`exceptions.ModuleError`:
                If parsed URL winds up without a hostname, port, or scheme.

        """
        self._init_url = url
        """:obj:`str`: Initial URL provided."""
        self._init_scheme = default_scheme
        """:obj:`str`: Default scheme provided."""
        self._init_parsed = requests.compat.urlparse(url)
        """:obj:`urllib.parse.ParseResult`: First pass of parsing URL."""
        self.parsed = self.reparse(
            parsed=self._init_parsed, default_scheme=default_scheme
        )
        """:obj:`urllib.parse.ParseResult`: Second pass of parsing URL."""

        for part in ["hostname", "port", "scheme"]:
            if not getattr(self.parsed, part, None):
                error = "\n".join(
                    [
                        "",
                        "Parsed into: {pstr}",
                        "URL format should be like: scheme://hostname:port",
                        "No {part} provided in URL {url!r}",
                    ]
                )
                error = error.format(part=part, url=url, pstr=self.parsed_str)
                raise exceptions.ModuleError(error)

    def __str__(self):
        """Show object info.

        Returns:
            :obj:`str`

        """
        bits = ["parsed={!r}".format(self.parsed_str)]
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
    def hostname(self):
        """Hostname part from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        return self.parsed.hostname

    @property
    def port(self):
        """Port part from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`int`

        """
        return int(self.parsed.port)

    @property
    def scheme(self):
        """Scheme part from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        return self.parsed.scheme

    @property
    def url(self):
        """Get scheme, hostname, and port from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        return self.unparse_base(p=self.parsed)

    @property
    def url_full(self):
        """Get full URL from :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        return self.unparse_all(p=self.parsed)

    @property
    def parsed_str(self):
        """Create string of :attr:`UrlParser.parsed`.

        Returns:
            :obj:`str`

        """
        parsed = getattr(self, "parsed", None)
        attrs = [
            "scheme",
            "netloc",
            "hostname",
            "port",
            "path",
            "params",
            "query",
            "fragment",
        ]
        vals = ", ".join(
            [
                "{a}={v!r}".format(a=a, v="{}".format(getattr(parsed, a, "")) or "")
                for a in attrs
            ]
        )
        return vals

    def make_netloc(self, host, port):
        """Create netloc from host and port.

        Args:
            host (:obj:`str`):
                Host part to use in netloc.
            port (:obj:`str`):
                Port part to use in netloc.

        Returns:
            :obj:`str`

        """
        netloc = ":".join([host, port]) if port else host
        return netloc

    def reparse(self, parsed, default_scheme=""):
        """Reparse a parsed URL into a parsed URL with values fixed.

        Args:
            parsed (:obj:`urllib.parse.ParseResult`):
                Parsed URL to reparse.
            default_scheme (:obj:`str`, optional):
                If no scheme in URL, use this.

                Defaults to: ""

        Returns:
            :obj:`urllib.parse.ParseResult`

        """
        scheme, netloc, path, params, query, fragment = parsed
        host = parsed.hostname
        port = format(parsed.port or "")

        if not netloc and scheme and path and path.split("/")[0].isdigit():
            """For case:
            >>> urllib.parse.urlparse('host:443/')
            ParseResult(
                scheme='host', netloc='', path='443/', params='', query='', fragment=''
            )
            """
            host = scheme  # switch host from scheme to host
            port = path.split("/")[0]  # remove / from path and assign to port
            path = ""  # empty out path
            scheme = default_scheme
            netloc = ":".join([host, port])

        if not netloc and path:
            """For cases:
            >>> urllib.parse.urlparse('host:443')
            ParseResult(
                scheme='', netloc='', path='host:443', params='', query='', fragment=''
            )
            >>> urllib.parse.urlparse('host')
            ParseResult(
                scheme='', netloc='', path='host', params='', query='', fragment=''
            )
            """
            netloc, path = path, netloc
            if ":" in netloc:
                host, port = netloc.split(":", 1)
                netloc = ":".join([host, port]) if port else host
            else:
                host = netloc

        scheme = scheme or default_scheme
        if not scheme and port:
            if format(port) == "443":
                scheme = "https"
            elif format(port) == "80":
                scheme = "http"

        if not port:
            if scheme == "https":
                port = "443"
                netloc = self.make_netloc(host, port)
            elif scheme == "http":
                port = "80"
                netloc = self.make_netloc(host, port)

        pass2 = requests.compat.urlunparse(
            (scheme, netloc, path, params, query, fragment)
        )
        ret = requests.compat.urlparse(pass2)
        return ret

    def unparse_base(self, p):
        """Unparse a parsed URL into just the scheme, hostname, and port parts.

        Args:
            p (:obj:`urllib.parse.ParseResult`):
                Parsed URL to unparse.

        Returns:
            :obj:`str`

        """
        # only unparse self.parsed into url with scheme and netloc
        return requests.compat.urlunparse((p.scheme, p.netloc, "", "", "", ""))

    def unparse_all(self, p):
        """Unparse a parsed URL with all the parts.

        Args:
            p (:obj:`urllib.parse.ParseResult`):
                Parsed URL to unparse.

        Returns:
            :obj:`str`

        """
        return requests.compat.urlunparse(p)
