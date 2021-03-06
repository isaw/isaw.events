# -*- coding: utf-8 -*-
"""
This module contains the tool of Events
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('isaw', 'events', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='isaw.events',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='events isaw schedule calendar',
      author='Christopher Warner',
      author_email='christopher.warner@nyu.edu',
      url='http://github.com/christophwarner/isaw.events',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['isaw', ],
      include_package_data=True,
      zip_safe=False,
      dependency_links=['http://code.google.com/p/python-twitter/'],
      install_requires=['setuptools',
                        'python-twitter >= 0.6',
                        'simplejson >= 2.0.9',
                        'tinyurl >= 0.1.0',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'isaw.events.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
 
