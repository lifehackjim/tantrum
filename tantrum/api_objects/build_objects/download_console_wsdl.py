#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility for downloading console.wsdl from a Tanium platform."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys
import datetime

try:
    import pathlib
except Exception:
    import pathlib2 as pathlib

__version__ = "3.0.0"
TMPL_INIT = '''# -*- coding: utf-8 -*-
"""WSDL contents downloaded from Tanium platform server."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

downloaded_on = "{date}"

from_version = "{version}"

from_url_path = "{url_path}"

data = """{data}

"""  # noqa
'''


def add_args(argparser, args):
    """Add arguments to argparser.

    Args:
        argparser (:obj:`argparse.ArgumentParser`):
            Object to add args to.
        args (:obj:`list` of :obj:`dict`):
            List of arguments to add to argparser

    Returns:
        :obj:`argparse.ArgumentParser`

    """
    required = argparser.add_argument_group("Required Arguments")
    optional = argparser.add_argument_group("Optional Arguments")

    for arg in args:
        arg_required = arg.get("required", False)
        arg_default = arg.get("default", argparse.SUPPRESS)
        arg_help = arg.get("help", "")
        arg_opts = arg.pop("opts") if "opts" in arg else []

        grp = required if arg_required else optional

        helps = []
        helps.append(arg_help)

        if arg_default is not argparse.SUPPRESS and not arg_required:
            helps.append("DEFAULT: {d!r}".format(d=arg_default))

        choices = arg.get("choices", [])
        if choices:
            helps.append("VALID VALUES: {c}".format(c=", ".join(choices)))

        arg["help"] = "\n".join(helps)
        grp.add_argument(*arg_opts, **arg)
    return argparser


def arg_parse(script_path):
    """Parse arguments from command line."""
    args = [
        {
            "opts": ["-u", "--url"],
            "dest": "url",
            "metavar": "https://{host}:{port}",
            "help": "URL to Tanium Platform Server",
            "required": True,
        },
        {
            "opts": ["-o", "--overwrite"],
            "dest": "overwrite",
            "default": False,
            "action": "store_true",
            "help": "Overwrite output objects files that already exist.",
            "required": False,
        },
        {
            "opts": ["-p", "--tantrum_path"],
            "dest": "tantrum_path",
            "default": script_path.parent.parent.parent.parent.parent,
            "help": "Path to tantrum package",
            "required": False,
        },
        {
            "opts": ["--output_dir"],
            "dest": "output_dir",
            "default": script_path.parent,
            "help": "Directory to create API version sub-directory with console.wsdl",
            "required": False,
        },
        {
            "opts": ["--version"],
            "help": "Version of this script.",
            "version": "%(prog)s {v}".format(v=__version__),
            "default": argparse.SUPPRESS,
            "action": "version",
        },
        {
            "opts": ["-h", "--help"],
            "help": "Show this help message and exit.",
            "default": argparse.SUPPRESS,
            "action": "help",
        },
    ]

    argparser = argparse.ArgumentParser(
        description=__doc__,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    add_args(argparser=argparser, args=args)
    args, extra_args = argparser.parse_known_args()
    return args, extra_args


def check_dir(path, name):
    """Check that a directory exists.

    Args:
        path (:obj:`pathlib.Path` or :obj:`str`):
            Path to check.
        name (:obj:`str`):
            Reference name of path.

    Raises:
        :exc:`Exception`:
            If path does not exist.

    Returns:
        :obj:`pathlib.Path`

    """
    path = pathlib.Path(path).expanduser().absolute()

    if not path.is_dir():
        error = "Unable to find {name!r} path '{path!r}'"
        error = error.format(path=format(path), name=name)
        raise Exception(error)
    return path


def write_contents(path, contents, overwrite=False):
    """Write contents to path."""
    if path.is_file():
        if overwrite:
            m = "!! Overwrite is True - overwriting pre-existing file: {path!r}"
            m = m.format(path=format(path))
            print(m)
        else:
            m = "!! Overwrite is False, not overwriting pre-existing file: {path!r}"
            m = m.format(path=format(path))
            print(m)
            return
    path.write_text(contents)
    print("Wrote file: {}".format(path))


def main(url, output_dir, tantrum, overwrite=False):
    """Download a WSDL from a platform server to path named after version of server.

    Args:
        url (:obj:`str`):
            URL of platform server
        output_dir (:obj:`pathlib.Path` or :obj:`str`):
            Directory under which to create version directory.
        tantrum (:obj:`object`):
            tantrum3 module.
        overwrite (:obj:`bool`, optional):
            Over write WSDL file if exists.

            Defaults to: False.

    """
    output_dir = check_dir(path=output_dir, name="output")
    client = tantrum.http_client.HttpClient(url=url, verify=False)
    version = tantrum.api_clients.get_version(client)
    wsdl = tantrum.api_clients.get_wsdl(client)

    version_dir = output_dir / version.replace(".", "_")

    if not version_dir.is_dir():
        version_dir.mkdir()
        m = "Created directory {path!r}"
        m = m.format(path=format(version_dir))
        print(m)

    date = datetime.datetime.utcnow()
    url_path = tantrum.api_clients.WSDL_PATH

    wsdl_path = version_dir / "__init__.py"
    wsdl_contents = TMPL_INIT.format(
        data=wsdl, version=version, date=date, url_path=url_path
    )
    write_contents(path=wsdl_path, contents=wsdl_contents, overwrite=overwrite)

    m = "Done with version {version!r}, " "you need to manually populate 'soap.py'"
    m = m.format(version=version)
    print(m)


if __name__ == "__main__":
    script_path = pathlib.Path(sys.argv[0]).expanduser().absolute()
    args, _ = arg_parse(script_path)
    sys.path.insert(0, format(args.tantrum_path))
    import tantrum

    main(
        url=args.url,
        output_dir=args.output_dir,
        tantrum=tantrum,
        overwrite=args.overwrite,
    )
