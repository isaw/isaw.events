import sys, os, re, textwrap
from elementtree import HTMLTreeBuilder
from string import Template

# --
# This is used to build the seltest_all.py file into the same directory.
# --

# root directory finding code
def getRootDirOfModule(module_name):
    return os.path.dirname(sys.modules[module_name].__file__)

def getRootDirOfClass(cls):
    return getRootDirOfModule(cls.__module__)

def getRootDirOfInstance(obj):
    return getRootDirOfClass(obj.__class__)

def getSeleniumTestsFromSuite(owner_instance, suite):
    """Get absolute filenames of all tests from the suite.
    Suite contains the directory that we need to find.
    owner_instance is used for the directory finding,
    the suite's directory is traversed relative from that.
    """
    test_filenames = []
    # The owner instance is only used to traverse the sute directory
    # relative from it.
    root_dir = getRootDirOfInstance(owner_instance)
    tests_root_dir = os.path.join(root_dir, suite.test_directory)
    for test_filename in os.listdir(tests_root_dir):
        if test_filename.lower().endswith('.html') or \
                test_filename.endswith('.htm'):
            test_filenames.append((test_filename, os.path.join(tests_root_dir, test_filename)))
    # sort the testfilenames
    test_filenames.sort()
    # return only the absolute filenames
    test_filenames = [filename[1] for filename in test_filenames]
    return test_filenames

template = Template(textwrap.dedent('''\
        from seleniumtestcase import SeleniumTestCase
        import unittest, time

        class seltest_$testname(SeleniumTestCase):

        $tests

        def test_suite():
            return unittest.makeSuite(seltest_$testname)

        if __name__ == "__main__":
            unittest.main()
        '''))

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



def cookSeleniumTests(filenames):
    """Cook selenium tests
    """
    # Try to open the file for writing.
    output_dir =  getRootDirOfModule('kss.demo.selenium_utils')
    output_filename = os.path.join(output_dir, 'seltest_all.py')
    try:
        f = open(output_filename, 'wb')
    except IOError, exc:
        raise IOError, ('Cannot open file "%s" for writing. '
                        'Make sure zope process has write access in directory. '
                        '["%s"]') \
                        % (output_filename, exc)

    htmlparser = HTMLTreeBuilder.TreeBuilder()
    tests = []

    # Now, we find all filenames that are in the suite passed to us.
    testname = 'all'

    for filename in filenames:
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

    # Use the last test's name as filename (???)
    # XXX I think we want to change this.
    f.write(template.substitute(dict(
        testname=testname,
        tests='\n'.join(tests),
        )))
    f.close()
