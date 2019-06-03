#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility for generating API objects files for tantrum.

For each directory in this scripts path that has a file console.wsdl:
    treat directory name as API version
    parse console.wsdl for API objects
    for each filename in [soap.py]:
        the source contents are combined with the parsed objects
        file is written to ${filename}_${api_version}.py in the parent directory
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import black
import datetime
import importlib
import logging
import platform
import string
import sys
import xmltodict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOG = logging.getLogger()

try:
    import pathlib
except Exception:
    import pathlib2 as pathlib

__version__ = "3.0.0"

TMPL_BUILD_META = '''
BUILD_META = {
    "script": "${script}",
    # Script used to build this file
    "script_version": "${script_version}",
    # Version of script used to build this file
    "script_platform": "${script_platform}",
    # OS Platform that ran this build script
    "script_python": "${script_python}",
    # Python version that ran this build script
    "date": "${date}",
    # Date/time in UTC format of when this file was built
    "source_file": "${source_file}",
    # File that was used to auto-generate objects in this file
    "source_file_date": "${source_file_date}",
    # Date/time in UTC format of the source_file
}
""":obj:`dict`: How this module was built (date/time in UTC format)."""'''
TMPL_BUILD_META = string.Template(TMPL_BUILD_META)
""":obj:`string.Template`: Template used to build BUILD_META dict part."""

TMPL_VERSION = '''
VERSION = {
    "major": ${major},
    "minor": ${minor},
    "protocol": ${protocol},
    "build": ${build},
    "string": "${string}",
}
""":obj:`dict`: Tanium API version these objects are intended to be used for."""

__version__ = VERSION["string"]
""":obj:`str`: Tanium API version these objects are intended to be used for."""
'''
TMPL_VERSION = string.Template(TMPL_VERSION)
""":obj:`string.Template`: Template used to build VERSION dict part."""

TMPL_COMMANDS = '''
COMMANDS = [${commands}
]
""":obj:`list` of :obj:`str`:API commands."""'''
TMPL_COMMANDS = string.Template(TMPL_COMMANDS)
""":obj:`string.Template`: Template used to build COMMANDS list part."""

TMPL_LIST_CLS = '''
class ${class_name}(ApiList):
    """Automagically generated API array object."""

    API_NAME = "${api_name}"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "${src_type}"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {${simple_parts}}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {${complex_parts}}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {${constant_parts}}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_ITEM_ATTR = "${item_attr}"
    """:obj:`str`: Name of :attr:`API_ITEM_CLS` used in API calls."""

    API_ITEM_CLS = "${item_cls}"
    """:class:`ApiItem`: Item class this list class holds."""
'''
TMPL_LIST_CLS = string.Template(TMPL_LIST_CLS)
""":obj:`string.Template`: Template used to build ApiList class objects."""

TMPL_ITEM_CLS = '''
class ${class_name}(ApiItem):
    """Automagically generated API object."""

    API_NAME = "${api_name}"
    """:obj:`str`: Name of object used in API calls."""

    API_NAME_SRC = "${src_type}"
    """:obj:`str`: Name of object in source file."""

    API_SIMPLE = {${simple_parts}}
    """:obj:`dict`: Map of simple attributes to their types."""

    API_COMPLEX = {${complex_parts}}
    """:obj:`dict`: Map of complex attributes to their types."""

    API_CONSTANTS = {${constant_parts}}
    """:obj:`dict`: Map of constants to their values."""

    API_STR_ADD = []
    """:obj:`list` or :obj:`str`: Attributes to add to str formatting."""

    API_LIST_CLS = "${list_cls}"
    """:class:`ApiList`: List class that holds this item class."""

    API_LIST_API_NAME = "${list_name}"
    """:obj:`str`: Name of :attr:`API_LIST_CLS` used in API calls."""
'''
TMPL_ITEM_CLS = string.Template(TMPL_ITEM_CLS)
""":obj:`string.Template`: Template used to build ApiItem class objects."""

TMPL_ATTR = """        "{name}": "{type_camel}",  # noqa: E501"""
""":obj:`str`: String formatter used to build simple/complex attrs."""

TMPL_CONSTANT = """        "{name}": {value!r},"""
""":obj:`str`: String formatter used to build constants."""

TMPL_MODULE = """${input_part}
${parsed_part}
api_fixes()
expand_cls_globals()
"""
TMPL_MODULE = string.Template(TMPL_MODULE)
""":obj:`string.Template`: Template used to build the output file."""

TMPL_DOC = """{TYPE} API Object Module for Version {major}.{minor}.{protocol}.{build}
#####################################################################################

.. automodule:: tantrum.api_objects.{type}_{major}_{minor}_{protocol}_{build}
    :members:
    :undoc-members:
    :show-inheritance:
    :private-members:
    :member-order: bysource
"""
""":obj:`str`: String formatter used to build sphinx doc file."""

TMPL_VER_STR = "{major}_{minor}_{protocol}_{build}"
""":obj:`str`: String formatter used to build version str for file name."""

TMPL_FILE_STEM = "{api_type}_{ver_str}"
""":obj:`str`: String formatter used to build stem str for file name."""


def get_paths_with(path, with_file, only=None):
    """Get all directories under path that have with_file in them."""
    path = pathlib.Path(path).absolute()
    paths = [p for p in path.glob("*") if p.is_dir() and (p / with_file).is_file()]
    if only:
        paths = [p for p in paths if p.name == only]
    if not paths:
        if only:
            error = "No paths exist that only match '{o}' with file '{f}' under '{p}'"
        else:
            error = "No paths exist with file '{f}' under '{p}'"
        error = error.format(f=with_file, p=path / "*", o=only)
        raise Exception(error)
    return paths


def write_path(path, contents):
    """Write the contents of a file.."""
    path.write_text(contents)
    m = "Wrote {c} bytes to '{p}'"
    m = m.format(c=len(contents), p=path)
    LOG.info(m)


def get_input_path_contents(path):
    """Get the contents of a file."""
    if not path.is_file():
        error = "Unable to find file: '{p}'"
        error = error.format(p=path)
        raise Exception(error)
    contents = path.read_text()
    return contents


def parse_version_from_path(path):
    """Get version parts from a path name."""
    path = pathlib.Path(path).absolute()
    version = path.name
    try:
        parts = version.split("_")
        ret = {}
        ret["major"] = try_int(parts[0])
        ret["minor"] = try_int(parts[1])
        ret["protocol"] = try_int(parts[2])
        ret["build"] = try_int(parts[3])
        ret["string"] = version.replace("_", ".")
        ret["file"] = version
    except Exception:
        error = "Bad API version in '{p}', must look like: '7_2_314_3181'"
        error = error.format(p=path)
        raise Exception(error)
    return ret


def camelcase(text):
    """Convert some_string or some-string to SomeString."""
    text_spaced = text.replace("_", " ").replace("-", " ")
    ret = string.capwords(text_spaced).replace(" ", "")
    return ret


def try_int(value):
    """Coerce an object into an int."""
    try:
        return int(value)
    except Exception:
        return value


def coerce_list(o):
    """Coerce an object into a list."""
    if not isinstance(o, (list, tuple)):
        o = [o]
    return o


def add_args(argparser, args):
    """Add arguments to an argparser based off of list of dicts in args."""
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
            helps.append("DEFAULT: '{d}'".format(d=arg_default))

        choices = arg.get("choices", [])
        if choices:
            helps.append("VALID VALUES: {c}".format(c=", ".join(choices)))

        arg["help"] = "\n".join(helps)
        grp.add_argument(*arg_opts, **arg)
    return argparser


def arg_parse(args):
    """Parse arguments from command line."""
    argparser = argparse.ArgumentParser(
        description=__doc__,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    add_args(argparser=argparser, args=args)
    args, extra_args = argparser.parse_known_args()
    return args, extra_args


def check_dest_path(path, overwrite=False):
    """Check if path exists."""
    if path.is_file():
        error = "Overwrite is {o} and found pre-existing file: '{p}'"
        error = error.format(o=overwrite, p=path)
        if not overwrite:
            raise Exception(error)
        else:
            LOG.warning(error)


class WsdlParser(object):
    """Parse a WSDL file to find all API objects."""

    object_skips = ["TaniumSOAPResult", "TaniumSOAPRequest", "auth"]
    # objects to skip over when parsing objects

    typemap = {
        "xsd:string": "string_types",
        "xsd:int": "integer_types",
        "xsd:long": "integer_types",
        "xsd:double": "float_types",
    }
    # mapping of xsd types to python types

    simpletypes = ["string_types", "integer_types", "float_types"]

    override_names = {
        "effective_content_set_privilege_request": "effective_content_set_privilege_request"  # noqa
    }

    def __init__(self, text):
        """Constructor."""
        self.src_text = text

        try:
            self.root = xmltodict.parse(self.src_text)
        except Exception as e:
            m = "Unable to parse XML text, error: {e}".format(e)
            raise Exception(m)
        self.schema = self.root["definitions"]["types"]["xsd:schema"]
        olist = [
            x for x in self.schema["xsd:complexType"] if x["@name"] == "object_list"
        ][0]
        olist_els = olist["xsd:sequence"]["xsd:element"]
        self.objlistmap = {x["@type"]: x["@name"] for x in olist_els}

    def get_commands(self):
        """Parse the list of valid commands from the WSDL."""
        simple_types = self.schema["xsd:simpleType"]
        elems = simple_types["xsd:restriction"]["xsd:enumeration"]
        commands = [x["@value"] for x in elems]
        return commands

    def add_list_cls_to_items(self, objects):
        """Try to determine the list class that owns an item class."""
        list_objects = [x for x in objects if x["list_attr"]]
        complex_list_objects = [
            x for x in list_objects if not x["list_attr"]["is_simple"]
        ]
        item_objects = [x for x in objects if not x["list_attr"]]
        mismatch1 = []
        mismatch2 = []
        for obj in complex_list_objects:
            list_attr = obj["list_attr"]
            if list_attr["name"] in obj["api_name"]:
                item_obj = [
                    x for x in objects if x["class_name"] == list_attr["type_camel"]
                ]
                item_obj[0]["list_cls"] = obj["class_name"]
                item_obj[0]["list_name"] = obj["api_name"]
            else:
                mismatch1.append(obj)

        for obj in mismatch1:
            list_attr = obj["list_attr"]
            item_obj = [x for x in item_objects if x["src_type"] == list_attr["type"]]
            if item_obj:
                if "list_cls" not in item_obj[0]:
                    item_obj[0]["list_cls"] = obj["class_name"]
                    item_obj[0]["list_name"] = obj["api_name"]
            else:
                mismatch2.append(obj)

        for obj in item_objects:
            obj["list_cls"] = obj.get("list_cls", None)
            obj["list_name"] = obj.get("list_name", "")
        return objects

    def get_objects(self):
        """Parse the list of complex types into a list of dicts."""
        objects = []

        for ctype in self.schema["xsd:complexType"]:
            if ctype["@name"] in self.object_skips:
                continue
            obj = self._parse_complex_type(ctype)
            if not obj["class_name"] in [x["class_name"] for x in objects]:
                objects.append(obj)

        objects = self.add_list_cls_to_items(objects)
        return objects

    def _parse_complex_type(self, ctype):
        """Parse a complex type into a dict.

        Should produce a dictionary as follows:
            src_type: str
                object type as known in the wsdl
            api_name: str
                object name used in API requests/responses
            class_name: str
                object name of Python class
            constants: list of dict
                object constants defined in wsdl, if any
            simple_attrs: list of dict
                object attributes that are simple (str, int, float)
            complex_attrs: list of dict
                object attributes that are not simple (other objects)
            if object is a list object:
                list_attr: dict
                    attribute used to store items
                item_cls: str
                    camel type of items this list class stores
                item_attr: str
                    attribute name used in API requests/responses
            if object is not a list object:
                list_cls: str
                    camel type of list_cls that holds this item

        Each attribute dict in list_attr, simple_attrs, and complex_attrs is as follows:
            name: str
                name of attribute
            type: str
                type of object attribute stores (string/int/float/ or other API object)
            type_camel: str
                camel case type if type is complex, else just type
            is_list: bool
                this attribute is an array
            is_simple: bool
                this attribute is simple
        """
        obj = {}
        obj["src_type"] = ctype["@name"]
        obj["class_name"] = self._camel(ctype["@name"])
        obj["api_name"] = self._get_obj_name(ctype["@name"])
        obj["constants"] = []
        obj["list_attr"] = {}

        attrs = []
        xsd_all = ctype.get("xsd:all", {})
        xsd_seq = ctype.get("xsd:sequence", {})
        xsd_attr = ctype.get("xsd:attribute", [])

        xsd_all_els = coerce_list(xsd_all.get("xsd:element", []) or [])
        xsd_seq_els = coerce_list(xsd_seq.get("xsd:element", []) or [])
        xsd_attr_els = coerce_list(xsd_attr)

        all_els = xsd_all_els + xsd_seq_els + xsd_attr_els
        all_els = [x for x in all_els if x]

        for el in all_els:
            el_maxoccurs = el.get("@maxOccurs", "")
            is_unbounded = el_maxoccurs == "unbounded"
            is_list_ending = ctype["@name"].endswith("_list")
            is_one_seq = len(xsd_seq_els) == 1
            is_list = is_unbounded or (is_list_ending and is_one_seq)
            attr = {}
            attr["name"] = el["@name"]
            attr["type"] = self.typemap.get(el["@type"], el["@type"])
            attr["type_camel"] = self._camel(attr["type"])
            attr["is_list"] = is_list
            attr["is_simple"] = attr["type"] in self.simpletypes
            attrs.append(attr)

        xsd_cons = ctype.get("xsd:annotation", {})
        xsd_cons = xsd_cons["xsd:appinfo"]["constants"]["constant"] if xsd_cons else []

        obj["constants"] = [
            {"name": el["name"], "value": try_int(el["value"]["#text"])}
            for el in xsd_cons
        ]

        list_attrs = [x for x in attrs if x["is_list"]]
        if len(list_attrs) == 1:
            obj["list_attr"] = list_attrs[0]
            obj["item_cls"] = obj["list_attr"]["type_camel"]
            obj["item_attr"] = obj["list_attr"]["name"]
            attrs = [x for x in attrs if x is not list_attrs[0]]

        obj["simple_attrs"] = [x for x in attrs if x["is_simple"]]
        obj["complex_attrs"] = [x for x in attrs if not x["is_simple"]]
        return obj

    def _get_obj_name(self, name):
        """Fancy dance to figure out the name that is used in requests/responses."""
        if name in self.override_names:
            return self.override_names[name]
        if name in self.objlistmap:
            return self.objlistmap[name]
        if name.endswith("_list") and name != "object_list":
            return name.replace("_list", "") + ("es" if name.endswith("s") else "s")
        return name

    def _camel(self, t):
        return t if t in self.simpletypes else camelcase(t)


def build_class_parts(objects, tmpl):
    """Build a class object."""
    parts = []
    for obj in objects:
        obj["constant_parts"] = build_cls_attr(
            items=obj["constants"], tmpl=TMPL_CONSTANT
        )
        obj["simple_parts"] = build_cls_attr(items=obj["simple_attrs"], tmpl=TMPL_ATTR)
        obj["complex_parts"] = build_cls_attr(
            items=obj["complex_attrs"], tmpl=TMPL_ATTR
        )
        part = tmpl.substitute(**obj)
        parts.append(part)
    return "\n".join(parts)


def build_meta_part(name, path, src_url):
    """Build the BUILD_META dict."""
    path = pathlib.Path(path)
    path_stat = pathlib.Path(path).stat()
    path_mtime = datetime.datetime.utcfromtimestamp(path_stat.st_mtime)
    now = datetime.datetime.utcnow()
    meta = {}
    meta["script"] = name
    meta["script_version"] = __version__
    meta["script_platform"] = platform.platform()
    meta["script_python"] = sys.version.splitlines()[0]
    meta["date"] = "{}".format(now)
    meta["source_file"] = "{}".format(src_url)
    meta["source_file_date"] = "{}".format(path_mtime)
    return TMPL_BUILD_META.substitute(**meta)


def build_version_part(version):
    """Build VERSION dict."""
    return TMPL_VERSION.substitute(**version)


def build_commands_part(commands):
    """Build COMMANDS list."""
    cmds = ["    {!r},".format(c) for c in commands]
    cmds = ([""] + cmds) if cmds else cmds
    return TMPL_COMMANDS.substitute(commands="\n".join(cmds))


def build_cls_attr(items, tmpl):
    """Build class attributes."""
    ret = [tmpl.format(**i) for i in items]
    if ret:
        ret = [""] + ret + ["    "]
    return "\n".join(ret)


def build_parts(path, file, version):
    """Generate all of the parts."""
    module = importlib.import_module(version["file"])
    wsdl_parser = WsdlParser(text=module.data)

    commands = wsdl_parser.get_commands()
    all_objects = wsdl_parser.get_objects()
    list_objects = [x for x in all_objects if x["list_attr"]]
    item_objects = [x for x in all_objects if not x["list_attr"]]

    m = "Parsed {i} item objects, {co} list objects, and {cc} commands from '{p}'"
    m = m.format(i=len(item_objects), co=len(list_objects), cc=len(commands), p=path)
    LOG.debug(m)

    src_url = module.from_url_path
    parts = [
        build_class_parts(objects=item_objects, tmpl=TMPL_ITEM_CLS),
        build_class_parts(objects=list_objects, tmpl=TMPL_LIST_CLS),
        build_meta_part(name=this_script.name, path=path, src_url=src_url),
        build_commands_part(commands=commands),
        build_version_part(version=version),
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    this_script = pathlib.Path(sys.argv[0]).expanduser().absolute()
    script_args = [
        {
            "opts": ["-o", "--overwrite"],
            "dest": "overwrite",
            "default": False,
            "action": "store_true",
            "help": "Overwrite output objects files that already exist.",
            "required": False,
        },
        {
            "opts": ["-b", "--build"],
            "dest": "build_dir",
            "default": None,
            "help": "Only build for this version instead of for all.",
            "required": False,
        },
        {
            "opts": ["-d", "--debug"],
            "dest": "debug",
            "default": False,
            "action": "store_true",
            "help": "Show debug logging.",
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
    args, _ = arg_parse(args=script_args)

    LOG.setLevel(logging.DEBUG if args.debug else logging.INFO)

    build_file = "__init__.py"
    get_path = this_script.parent
    paths = get_paths_with(path=get_path, with_file=build_file, only=args.build_dir)

    obj_files = ["soap.py"]
    output_path = this_script.parent.parent
    pkg_root = output_path.parent.parent
    docs_output_path = pkg_root / "docs" / "api" / "api_objects"

    for path in paths:
        version = parse_version_from_path(path=path)
        version_str = TMPL_VER_STR.format(**version)
        parsed_part = build_parts(path=path, file=build_file, version=version)
        for obj_file in obj_files:
            input_path = path / obj_file
            try:
                input_part = get_input_path_contents(path=input_path)
            except Exception as exc:
                error = "Build error, skipping build for '{p}' - error:\n!!  {e}"
                error = error.format(p=input_path, e=exc)
                LOG.error(error)
                continue

            api_type = input_path.stem
            file_stem = TMPL_FILE_STEM.format(api_type=api_type, ver_str=version_str)

            py_contents = TMPL_MODULE.substitute(
                input_part=input_part, parsed_part=parsed_part
            )
            py_contents = py_contents.strip()
            mode = black.FileMode(target_versions=black.PY36_VERSIONS)
            py_contents = black.format_file_contents(
                src_contents=py_contents, fast=False, mode=mode
            )

            rst_dest_file = "{stem}.rst".format(stem=file_stem)
            rst_dest_path = docs_output_path / api_type / rst_dest_file
            rst_contents = TMPL_DOC.format(
                TYPE=api_type.upper(), type=api_type, **version
            )
            write_path(contents=rst_contents, path=rst_dest_path)

            py_dest_file = "{stem}.py".format(stem=file_stem)
            py_dest_path = output_path / py_dest_file
            try:
                check_dest_path(path=py_dest_path, overwrite=args.overwrite)
            except Exception as exc:
                error = "Skipping build for '{p}':\n!!  {e}"
                error = error.format(p=input_path, e=exc)
                LOG.error(error)
                continue
            write_path(contents=py_contents, path=py_dest_path)
