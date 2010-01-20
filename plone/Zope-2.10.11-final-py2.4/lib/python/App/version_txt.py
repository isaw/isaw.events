##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Extract Zope 2 version information

$id$
"""
import os
import re
import sys

_location = None
_filename = 'version.txt'

_version_file = None
_version_string = None
_zope_version = None

def _get_filename():
    global _location
    if _version_file is not None:
        return _version_file
    if _location is None:
        import Zope2
        _location = os.path.dirname(Zope2.__file__)
    return os.path.join(_location, _filename)

def _prep_version_data():
    global _version_string, _zope_version
    if _version_string is None:
        v = sys.version_info
        pyver = "python %d.%d.%d, %s" % (v[0], v[1], v[2], sys.platform)
        fn = _get_filename()
        expr = re.compile(
            r'(?P<product>[A-Za-z0-9]+) +(?P<major>[0-9]+)'
            '\.(?P<minor>[0-9]+)\.(?P<micro>[0-9]+)'
            '(?P<status>[A-Za-z]+)?(?P<release>[0-9]+)?')
        try:
            s = open(fn).read().strip()
        except IOError:
            ss = 'unreleased version'
            _zope_version = (-1, -1, -1, '', -1)
        else:
            ss = re.sub("\(.*?\)\?","",s)
            dict = expr.match(s).groupdict()
            _zope_version = (
                int(dict.get('major') or -1),
                int(dict.get('minor') or -1),
                int(dict.get('micro') or -1),
                dict.get('status') or '',
                int(dict.get('release') or -1),
                )
        _version_string = "%s, %s" % (ss, pyver)


def version_txt():
    _prep_version_data()
    return '(%s)' % _version_string

def getZopeVersion():
    """
    Format of zope_version tuple:
    (major <int>, minor <int>, micro <int>, status <string>, release <int>)
    If unreleased, integers may be -1.
    """
    _prep_version_data()
    return _zope_version
