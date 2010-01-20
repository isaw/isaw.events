##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import os
import re
import shutil
import sys
import tempfile
import urllib2
import urlparse
import setuptools.archive_util

EGG_INFO_CONTENT = """Metadata-Version: 1.0
Name: %s
Version: %s
"""

DEFAULT_FAKE_EGGS = [
    'Acquisition',
    'ClientForm',
    'DateTime',
    'docutils',
    'ExtensionClass',
    'mechanize',
    'pytz',
    'RestrictedPython',
    'Persistence',
    'tempstorage',
    'ZConfig',
    'zLOG',
    'zodbcode',
    'ZODB3',
    'zdaemon',
    'Zope2',
]

# define which values are read as true
TRUEVALS = ('y', 'yes', 't', 'true', 'on', '1')
VERSION_0_0 = '0.0'


class FakeLibInfo(object):
    """
    a really simple to store informations about libraries to be faked
    as eggs.
    """
    version = ''
    name = ''

    def __init__(self, name, version=VERSION_0_0, skip=False):
        self.version = version
        self.name = name
        self.skip = skip

    def make(self, fakeEggsDirectory, developEggsDirectory):
        self.link = os.path.join(developEggsDirectory,
            '%s.egg-link' % self.name)
        self.libDirectory = os.path.join(fakeEggsDirectory, self.name)
        if self.skip:
            self.cleanup()
        else:
            self.makeEggInfoFile()
            self.makeDevelopEggLink()

    def cleanup(self):
        if os.path.isdir(self.libDirectory):
            shutil.rmtree(self.libDirectory)
        if os.path.exists(self.link) and self.linkIsFake():
            os.remove(self.link)

    def makeEggInfoFile(self):
        directory = self.libDirectory
        if not os.path.isdir(directory):
            os.mkdir(directory)
        eggInfoFile = os.path.join(directory, '%s.egg-info' % self.name)
        fd = open(eggInfoFile, 'w')
        fd.write(EGG_INFO_CONTENT % (self.name, self.version))
        fd.close()

    def makeDevelopEggLink(self):
        fd = open(self.link, 'w')
        fd.write("%s\n." % self.libDirectory)
        fd.close()

    def linkIsFake(self):
        fd = open(self.link)
        try:
            line = fd.readline()
            return line.startswith(self.libDirectory)
        finally:
            fd.close()


class Recipe:

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        python = buildout['buildout']['python']
        options['executable'] = buildout[python]['executable']
        self.location = options.get('location', None)
        self.svn = options.get('svn', None)
        self.url = options.get('url', None)
        assert self.location or self.svn or self.url

        if self.location is not None:
            # We have an existing Zope installation; use it.
            assert os.path.exists(self.location), \
                'No such file or directory: %s' % self.location
            options['location'] = self.location
            options['shared-zope'] = 'true'
        elif (self.svn is None and
            buildout['buildout'].get('zope-directory') is not None):
            # if we use a download, then we look for a directory with shared
            # Zope installations. TODO Sharing of SVN checkouts is not yet
            # supported
            _, _, urlpath, _, _, _ = urlparse.urlparse(self.url)
            fname = urlpath.split('/')[-1]
            # cleanup the name a bit
            for s in ('.tar', '.bz2', '.gz', '.tgz'):
                fname = fname.replace(s, '')
            # Include the Python version Zope is compiled with into the
            # download cache name, so you can have the same Zope version
            # compiled with for example Python 2.3 and 2.4 but still share it
            ver = sys.version_info[:2]
            pystring = 'py%s.%s' % (ver[0], ver[1])
            options['location'] = os.path.join(
                buildout['buildout']['zope-directory'],
                '%s-%s' % (fname, pystring))
            options['shared-zope'] = 'true'
        else:
            # put it into parts
            options['location'] = os.path.join(
                buildout['buildout']['parts-directory'],
                self.name)
        # We look for a download cache, where we put the downloaded tarball
        if buildout['buildout'].get('download-cache') is None:
            download_cache = os.path.join(buildout['buildout']['directory'],
                                          'downloads')
            if not os.path.isdir(download_cache):
                os.mkdir(download_cache)
            buildout['buildout'].setdefault('download-cache', download_cache)

        self.fake_zope_eggs = options.get('fake-zope-eggs', 'true')
        if self.fake_zope_eggs.lower() not in TRUEVALS:
            self.fake_zope_eggs = False
        else:
            self.fake_zope_eggs = True
        self.fake_eggs_folder = self.options.get('fake-eggs-folder',
                                                 'fake-eggs')

        skip_fake_eggs = self.options.get('skip-fake-eggs', '')
        self.skip_fake_eggs = [e for e in skip_fake_eggs.split('\n') if e]

    def _compiled(self, path):
        """returns True if the path is compiled"""
        for files, dirs, root in os.walk(path):
            for f in files:
                base, ext = os.path.splitext(f)
                if ext == '.c':
                    if sys.platform == 'win32':
                        compiled_ext = '.pyd'
                    else:
                        compiled_ext = '.so'
                    compiled = os.path.join(root,
                        '%s%s' % (base, compiled_ext))
                    if not os.path.exists(compiled):
                        return False
        return True

    def install(self):
        options = self.options
        location = options['location']
        download_dir = self.buildout['buildout']['download-cache']
        smart_recompile = options.get('smart-recompile') == 'true'

        if os.path.exists(location):
            # if the zope installation exists and is shared, then we are done
            # and don't return a path, so the shared installation doesn't get
            # deleted on uninstall
            if options.get('shared-zope') == 'true':
                # We update the fake eggs in case we have special skips or
                # additions
                if self.fake_zope_eggs:
                    print 'Creating fake eggs'
                    self.fakeEggs()
                return []
        else:
            smart_recompile = True

        if smart_recompile and os.path.exists(location):
            # checking if the c source where compiled.
            if self._compiled(location):
                if self.fake_zope_eggs:
                    print 'Creating fake eggs'
                    self.fakeEggs()
                return []

        # full installation
        if os.path.exists(location):
            shutil.rmtree(location)

        if self.svn:
            assert os.system('svn co %s %s' % (options['svn'], location)) == 0
        else:
            if not os.path.isdir(download_dir):
                os.mkdir(download_dir)

            _, _, urlpath, _, _, _ = urlparse.urlparse(self.url)
            tmp = tempfile.mkdtemp('buildout-'+self.name)
            try:
                fname = os.path.join(download_dir, urlpath.split('/')[-1])
                # Have we already downloaded the file
                if not os.path.exists(fname):
                    f = open(fname, 'wb')
                    try:
                        f.write(urllib2.urlopen(self.url).read())
                    except:
                        os.remove(fname)
                        raise
                    f.close()

                setuptools.archive_util.unpack_archive(fname, tmp)
                # The Zope tarballs have a Zope-<version> folder at the root
                # level, so we need to move that one into the right place.
                files = os.listdir(tmp)
                if len(files) == 0:
                    raise ValueError('Broken Zope tarball named %s' % fname)
                shutil.move(os.path.join(tmp, files[0]), location)
            finally:
                shutil.rmtree(tmp)

        os.chdir(location)
        assert os.spawnl(
            os.P_WAIT, options['executable'], options['executable'],
            'setup.py',
            'build_ext', '-i',
            ) == 0

        # compile .py files to .pyc;
        # ignore return status since compilezpy.py will return
        # an exist status of 1 for even a single failed compile.
        os.spawnl(
            os.P_WAIT, options['executable'], options['executable'],
            os.path.join(location, 'utilities', 'compilezpy.py'),
            'build_ext', '-i',
            )

        if self.fake_zope_eggs:
            print 'Creating fake eggs'
            self.fakeEggs()
        if self.url and options.get('shared-zope') == 'true':
            # don't return path if the installation is shared, so it doesn't
            # get deleted on uninstall
            return []
        return location

    def fakeEggs(self):
        self.makeFakeEggsDirectory()
        self.initAdditionalFakeEggs()
        self.harvestPotentialFakeEggs()

        developEggDir = self.buildout['buildout']['develop-eggs-directory']
        for libInfo in self.libsToFake:
            libInfo.make(self.fakeEggsDirectory, developEggDir)

    def makeFakeEggsDirectory(self):
        self.fakeEggsDirectory = os.path.join(
            self.buildout['buildout']['directory'], self.fake_eggs_folder)
        if not os.path.isdir(self.fakeEggsDirectory):
            os.mkdir(self.fakeEggsDirectory)

    def initAdditionalFakeEggs(self):
        self.libsToFake = []
        # We add all additional fake eggs
        additional = self.options.get('additional-fake-eggs', '')
        additional = [e for e in additional.split('\n') if e]
        additional_names = []
        # Build up a list of all fake egg names without a version spec
        for line in additional:
            if '=' in line:
                spec = line.strip().split('=')
                name = spec[0].strip()
            else:
                name = line.strip()
            additional_names.append(name)
        # Add defaults to the specified set if the egg is not specified
        # in the additional-fake-eggs option, so you can overwrite one of
        # the default eggs with one including a version spec
        for name in DEFAULT_FAKE_EGGS:
            if name not in additional_names:
                additional.append(name)
        for lib in additional:
            # 2 forms available:
            #  * additional-fake-eggs = myEgg
            #  * additional-fake-eggs = myEgg=0.4
            if '=' in lib:
                lib = lib.strip().split('=')
                eggName = lib[0].strip()
                version = lib[1].strip()
            else:
                eggName = lib.strip()
                version = VERSION_0_0
            skip = self.shouldSkipFakeEgg(eggName)
            libInfo = FakeLibInfo(eggName, version, skip)
            self.libsToFake.append(libInfo)

    def shouldSkipFakeEgg(self, name):
        return name in self.skip_fake_eggs

    def harvestPotentialFakeEggs(self):
        zope2Location = self.options['location']
        zopeLibZopeLocation = os.path.join(zope2Location, 'lib', 'python',
                                           'zope')
        zopeLibZopeAppLocation = os.path.join(zope2Location, 'lib', 'python',
                                              'zope', 'app')
        self.libsToFake += self._getInstalledLibs(zopeLibZopeLocation, 'zope')
        self.libsToFake += self._getInstalledLibs(zopeLibZopeAppLocation,
                                             'zope.app')

    def _getInstalledLibs(self, location, prefix):
        installedLibs = []
        for lib in os.listdir(location):
            name = '%s.%s' % (prefix, lib)
            if (os.path.isdir(os.path.join(location, lib)) and
                name not in [libInfo.name for libInfo in self.libsToFake]):
                # Only add the package if it's not yet in the list
                skip = self.shouldSkipFakeEgg(name)
                installedLibs.append(FakeLibInfo(name, skip=skip))
        return installedLibs

    def update(self):
        options = self.options
        location = options['location']
        shared = options.get('shared-zope')
        if os.path.exists(location):
            # Don't do anything in offline mode
            if self.buildout['buildout'].get('offline') == 'true' or \
               self.buildout['buildout'].get('newest') == 'false':
                if self.fake_zope_eggs:
                    print 'Updating fake eggs'
                    self.fakeEggs()
                if options.get('shared-zope') == 'true':
                    return []
                return location

            # If we downloaded a tarball, we don't need to do anything while
            # updating, otherwise we have a svn checkout and should run
            # 'svn up' and see if there has been any changes so we recompile
            # the c extensions
            if self.location or self.url:
                if self.fake_zope_eggs:
                    print 'Updating fake eggs'
                    self.fakeEggs()
                if options.get('shared-zope') == 'true':
                    return []
                return location

            if (self._compiled(location) and
                options.get('smart-recompile') == 'true'):
                return location

            os.chdir(location)
            stdin, stdout, stderr = os.popen3('svn up')
            stdin.close()
            for line in stderr.readlines():
                sys.stderr.write(line)
            stderr.close()
            change = re.compile('[AUM] ').match
            for l in stdout:
                if change(l):
                    stdout.read()
                    stdout.close()
                    break
                else:
                    # No change, so all done
                    stdout.close()
                    return location

            assert os.spawnl(
                os.P_WAIT, options['executable'], options['executable'],
                'setup.py',
                'build_ext', '-i',
                ) == 0

            if self.fake_zope_eggs:
                print 'Updating fake eggs'
                self.fakeEggs()

        return location
