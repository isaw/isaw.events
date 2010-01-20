=========================
plone.recipe.zope2install
=========================

Overview
========

ZC Buildout recipe for installing Zope 2.

Example
=======

Let's start with the most basic example. We will fetch here a random
Zope tarball::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = zope2
    ...
    ... [zope2]
    ... recipe = plone.recipe.zope2install
    ... url = http://www.zope.org/Products/Zope/2.11.2/Zope-2.11.2-final.tgz
    ... fake-zope-eggs = False
    ... """)

If we run the buildout it returns::

    >>> print system(buildout)
    Installing zope2.
    running build_ext
    creating zope.proxy
    copying zope/proxy/proxy.h -> zope.proxy
    building 'AccessControl.cAccessControl' extension
    creating build
    creating build/...
    creating build/.../AccessControl
    ...

Let's have a look at the different folders created::

    >>> ls(sample_buildout, 'parts')
    d  zope2

    >>> ls(sample_buildout, 'develop-eggs')
    -  plone.recipe.zope2install.egg-link

    >>> ls(sample_buildout, 'parts', 'zope2')
    d  Extensions
    -  README.txt
    -  ZopePublicLicense.txt
    -  configure
    d  doc
    d  inst
    d  lib
    -  log.ini
    -  setup.py
    -  setup.pyc
    d  skel
    -  test.py
    -  test.pyc
    -  testing.log
    d  utilities

Fake Zope Eggs Example
======================

Zope 2 isn't eggified yet, Zope 3 is. This can become a problem if you want
to install some egg with dependencies related to Zope 3 eggs (such as
zope.interface, zope.component, ...)

This buildout recipe can help you by adding some fake eggs to Zope libraries
(installed inside zope/lib/python/zope/...) so that setuptools can see that
the dependencies are already satisfied and it won't fetch them anymore.

Since version 3 of the recipe this is the default::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = zope2
    ... find-links =
    ...     http://dist.plone.org/
    ...
    ... [zope2]
    ... recipe = plone.recipe.zope2install
    ... url = http://www.zope.org/Products/Zope/2.10.6/Zope-2.10.6-final.tgz
    ... """)

Now if we run the buildout again::

    >>> print system(buildout)
    Uninstalling zope2.
    Installing zope2.
    running build_ext
    creating zope.proxy
    copying zope/proxy/proxy.h -> zope.proxy
    building 'AccessControl.cAccessControl' extension
    creating build
    creating build/...
    creating build/.../AccessControl
    ...

The recipe then creates a fake-eggs folder in the buildout:

    >>> ls(sample_buildout)
    -  .installed.cfg
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  downloads
    d  eggs
    d  fake-eggs
    d  parts

With every eggs as a folder:

    >>> ls(sample_buildout, 'fake-eggs')
    d  Acquisition
    d  ClientForm
    d  DateTime
    d  ExtensionClass
    d  Persistence
    d  RestrictedPython
    d  ZConfig
    d  ZODB3
    d  Zope2
    d  docutils
    d  mechanize
    d  pytz
    d  tempstorage
    d  zLOG
    d  zdaemon
    d  zodbcode
    d  zope.annotation
    d  zope.app
    d  zope.app.annotation
    ...

Now if we list all the developed eggs we have::

    >>> ls(sample_buildout, 'develop-eggs')
    -  Acquisition.egg-link
    -  ClientForm.egg-link
    -  DateTime.egg-link
    -  ExtensionClass.egg-link
    -  Persistence.egg-link
    -  RestrictedPython.egg-link
    -  ZConfig.egg-link
    -  ZODB3.egg-link
    -  Zope2.egg-link
    -  docutils.egg-link
    -  mechanize.egg-link
    -  plone.recipe.zope2install.egg-link
    -  pytz.egg-link
    -  tempstorage.egg-link
    -  zLOG.egg-link
    -  zdaemon.egg-link
    -  zodbcode.egg-link
    -  zope.annotation.egg-link
    -  zope.app.annotation.egg-link
    ...

Let's have a look at the content of one of them::

    >>> cat(sample_buildout, 'develop-eggs', 'zope.annotation.egg-link')
    /sample-buildout/fake-eggs/zope.annotation
    .

And inside of each folder of the fake-eggs we have the egg-info::

    >>> ls(sample_buildout, 'fake-eggs', 'zope.annotation')
    -  zope.annotation.egg-info

Which contains::

    >>> cat(sample_buildout, 'fake-eggs', 'zope.annotation',
    ...     'zope.annotation.egg-info')
    Metadata-Version: 1.0
    Name: zope.annotation
    Version: 0.0

You might also want to add other fake eggs to your buildout, to do so use the
additional-fake-eggs option, for example::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = zope2
    ... find-links =
    ...     http://dist.plone.org/
    ...
    ... [zope2]
    ... recipe = plone.recipe.zope2install
    ... url = http://www.zope.org/Products/Zope/2.10.6/Zope-2.10.6-final.tgz
    ... additional-fake-eggs = Foo
    ... """)

    >>> print system(buildout)
    Uninstalling zope2.
    Installing zope2.
    running build_ext
    creating zope.proxy
    copying zope/proxy/proxy.h -> zope.proxy
    building 'AccessControl.cAccessControl' extension
    creating build
    creating build/...
    creating build/.../AccessControl
    ...

Let's check if the additional fake egg exists:

    >>> cat(sample_buildout, 'fake-eggs', 'Foo', 'Foo.egg-info')
    Metadata-Version: 1.0
    Name: Foo
    Version: 0.0

If you need to have a specific version of an egg, this can be done like this:

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = zope2
    ... find-links =
    ...     http://dist.plone.org/
    ...
    ... [zope2]
    ... recipe = plone.recipe.zope2install
    ... url = http://www.zope.org/Products/Zope/2.10.6/Zope-2.10.6-final.tgz
    ... additional-fake-eggs = ZODB3=3.7
    ...                        zope.app.tree = 1.7
    ... """)

    >>> print system(buildout)
    Uninstalling zope2.
    Installing zope2.
    running build_ext
    creating zope.proxy
    copying zope/proxy/proxy.h -> zope.proxy
    building 'AccessControl.cAccessControl' extension
    creating build
    creating build/...
    creating build/.../AccessControl
    ...

    >>> cat(sample_buildout, 'fake-eggs', 'ZODB3', 'ZODB3.egg-info')
    Metadata-Version: 1.0
    Name: ZODB3
    Version: 3.7

    >>> cat(sample_buildout, 'fake-eggs', 'zope.app.tree', 'zope.app.tree.egg-info')
    Metadata-Version: 1.0
    Name: zope.app.tree
    Version: 1.7

In some cases you might also want to ignore some of the packages shipped
with the Zope tarball::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = zope2
    ... find-links =
    ...     http://dist.plone.org/
    ...
    ... [zope2]
    ... recipe = plone.recipe.zope2install
    ... url = http://www.zope.org/Products/Zope/2.10.6/Zope-2.10.6-final.tgz
    ... skip-fake-eggs =
    ...     zope.annotation
    ...     zope.app.apidoc
    ... """)

Let's run the buildout::

    >>> print system(buildout)
    Uninstalling zope2.
    Installing zope2.
    running build_ext
    creating zope.proxy
    copying zope/proxy/proxy.h -> zope.proxy
    building 'AccessControl.cAccessControl' extension
    creating build
    creating build/...
    creating build/.../AccessControl
    ...

Now if we list all the developed eggs we have:

    >>> ls(sample_buildout, 'develop-eggs')
    -  Acquisition.egg-link
    -  ClientForm.egg-link
    -  DateTime.egg-link
    -  ExtensionClass.egg-link
    -  Foo.egg-link
    -  Persistence.egg-link
    -  RestrictedPython.egg-link
    -  ZConfig.egg-link
    -  ZODB3.egg-link
    -  Zope2.egg-link
    -  docutils.egg-link
    -  mechanize.egg-link
    -  plone.recipe.zope2install.egg-link
    -  pytz.egg-link
    -  tempstorage.egg-link
    -  zLOG.egg-link
    -  zdaemon.egg-link
    -  zodbcode.egg-link
    -  zope.app.annotation.egg-link
    -  zope.app.applicationcontrol.egg-link
    ...

If you want to develop one of the packages shipped
with the Zope tarball, you use skip-fake-eggs.
However, the corresponding develop egg should be left intact.

First, make a directory with develop eggs::

    >>> mkdir(sample_buildout, 'devel')
    >>> mkdir(sample_buildout, 'devel', 'Acquisition')
    >>> write(sample_buildout, 'devel', 'Acquisition', 'setup.py',
    ... '''
    ... from setuptools import setup
    ... setup(
    ...     name = "Acquisition",
    ...     )
    ... ''')
    >>> mkdir(sample_buildout, 'devel', 'zope.annotation')
    >>> write(sample_buildout, 'devel', 'zope.annotation', 'setup.py',
    ... '''
    ... from setuptools import setup
    ... setup(
    ...     name = "zope.annotation",
    ...     )
    ... ''')

Second, make a buildout with the given develop eggs, skipped as fake eggs::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = zope2
    ... find-links =
    ...     http://dist.plone.org/
    ... develop = devel/Acquisition
    ...           devel/zope.annotation
    ...
    ... [zope2]
    ... recipe = plone.recipe.zope2install
    ... url = http://www.zope.org/Products/Zope/2.10.6/Zope-2.10.6-final.tgz
    ... skip-fake-eggs =
    ...     Acquisition
    ...     zope.annotation
    ...     zope.app.apidoc
    ... """)

Let's run the buildout::

    >>> print system(buildout)
    Develop: '/sample-buildout/devel/Acquisition'
    Develop: '/sample-buildout/devel/zope.annotation'
    Uninstalling zope2.
    Installing zope2.
    running build_ext
    creating zope.proxy
    copying zope/proxy/proxy.h -> zope.proxy
    building 'AccessControl.cAccessControl' extension
    creating build
    creating build/...
    creating build/.../AccessControl
    ...

Now if we list all the developed eggs we have::

    >>> ls(sample_buildout, 'develop-eggs')
    -  Acquisition.egg-link
    -  ClientForm.egg-link
    -  DateTime.egg-link
    -  ExtensionClass.egg-link
    -  Foo.egg-link
    -  Persistence.egg-link
    -  RestrictedPython.egg-link
    -  ZConfig.egg-link
    -  ZODB3.egg-link
    -  Zope2.egg-link
    -  docutils.egg-link
    -  mechanize.egg-link
    -  plone.recipe.zope2install.egg-link
    -  pytz.egg-link
    -  tempstorage.egg-link
    -  zLOG.egg-link
    -  zdaemon.egg-link
    -  zodbcode.egg-link
    -  zope.annotation.egg-link
    -  zope.app.annotation.egg-link
    -  zope.app.applicationcontrol.egg-link
    ...

Let's check the develop-egg links::

    >>> cat(sample_buildout, 'develop-eggs', 'Acquisition.egg-link')
    /sample-buildout/devel/Acquisition
    .

    >>> cat(sample_buildout, 'develop-eggs', 'zope.annotation.egg-link')
    /sample-buildout/devel/zope.annotation
    .

Smart compilation
=================

Let's try the smart compilation option.

Just add it to your buildout config like this::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = zope2
    ... find-links =
    ...     http://dist.plone.org/
    ...
    ... [zope2]
    ... recipe = plone.recipe.zope2install
    ... url = http://www.zope.org/Products/Zope/2.10.6/Zope-2.10.6-final.tgz
    ... smart-recompile = true
    ... """)

Now if we run the buildout again::

    >>> print system(buildout)
    Uninstalling zope2.
    Installing zope2.
    running build_ext
    creating zope.proxy
    copying zope/proxy/proxy.h -> zope.proxy
    building 'AccessControl.cAccessControl' extension
    creating build
    creating build/...
    creating build/.../AccessControl
    ...

And a second time, even if we remove .installed.cfg it is not recompiled::

    >>> import os
    >>> os.remove('.installed.cfg')
    >>> print system(buildout)
    Installing zope2.
    Creating fake eggs
    <BLANKLINE>

Let's remove the option::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = zope2
    ... find-links =
    ...     http://dist.plone.org/
    ...
    ... [zope2]
    ... recipe = plone.recipe.zope2install
    ... url = http://www.zope.org/Products/Zope/2.10.6/Zope-2.10.6-final.tgz
    ... """)

Now if we run the buildout again::

    >>> print system(buildout)
    Uninstalling zope2.
    Installing zope2.
    running build_ext
    creating zope.proxy
    copying zope/proxy/proxy.h -> zope.proxy
    building 'AccessControl.cAccessControl' extension
    creating build
    creating build/...
    creating build/.../AccessControl
    ...

