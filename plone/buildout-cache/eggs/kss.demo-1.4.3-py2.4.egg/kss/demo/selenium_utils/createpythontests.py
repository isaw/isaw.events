#!/usr/bin/env python

raise SystemExit, 'Due to changes in the plugin registry, command line ' \
    'method is disabled until kss.demo is ported to kss.base.\n' \
    '    (Hint: call .../@@kss_demo_registry_admin/cookSeleniumTests from zope.)'

# Generate selenium test controller files from HTML selenium tests

from elementtree import HTMLTreeBuilder, ElementTree
import glob
from string import Template
import os
import re

template = Template('''
from seleniumtestcase import SeleniumTestCase
import unittest, time

class seltest_$testname(SeleniumTestCase):

$tests

def test_suite():
    return unittest.makeSuite(seltest_$testname)

if __name__ == "__main__":
    unittest.main()
''')

variable_regexp = re.compile('\$\{(?P<varname>\w*)\}')

def formatcommand(command, *args):
    if not command:
        return '' # Change this to raise an exception?

    arguments = []
    for arg in args:
        if not arg:
            continue
        matched = variable_regexp.match(arg)
        if matched is None:
            arguments.append('"%s"'%arg)
        else:
            arguments.append("self.getVar('%s')"%matched.group('varname'))
    return 'self.%s(%s)' % (command, ', '.join(arguments))

htmlparser = HTMLTreeBuilder.TreeBuilder()
tests = []
for filename in glob.glob('*.html'):
    tree = HTMLTreeBuilder.parse(filename)
    root = tree.getroot()

    try:
        testname = root.find('.//title').text
    except AttributeError:
        continue
    commands = []
    for row in root.findall('.//tbody/tr'):
        commands.append(formatcommand(*[td.text for td in row.findall('td')]))

    testfilename = 'seltest_%s.py' % testname
    testbody='    def test_%s(self):\n'%testname+' '*8+'\n        '.join(commands)+'\n'
    tests.append(testbody)

f = open('seltest_all.py', 'wb')
f.write(template.substitute(dict(
    testname=testname,
    tests='\n'.join(tests),
    )))
f.close()
