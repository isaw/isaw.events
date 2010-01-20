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

# ZC Buildout recipe for precompiling Python in product directories

# The compile_non_skip function is derived from Zope's compilezpy.py,
# which is licensed under the ZPL.


DefaultSkipDirs = """tests
skins
doc
kupu_plone_layer
Extensions
.svn"""

DefaultRX = r"/\."


import os, re, shutil, logging, compileall, re
import zc.buildout
import zc.recipe.egg

def compile_non_skip(dir, skip, rx):
    """Byte-compile all modules except those in skip directories."""
    
    # compile current directory
    compileall.compile_dir(dir, maxlevels=0, quiet=1, rx=rx)
    # get a list of child directories
    try:
        names = os.listdir(dir)
    except os.error:
        print "Can't list", dir
        names = []
    # visit subdirectories, calling self recursively
    # skip os artifacts and skip list.
    for name in names:
        fullname = os.path.join(dir, name)
        if (name != os.curdir and name != os.pardir and
            os.path.isdir(fullname) and not os.path.islink(fullname) and
            name not in skip):
            compile_non_skip(fullname, skip, rx)

class Recipe:

    def __init__(self, buildout, name, options):
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.buildout, self.options, self.name = buildout, options, name

        options['scripts'] = '' # suppress script generation.

        if not options.has_key('dirs'):
            dirs = set(self.findValuesByRecipe('plone.recipe.zope2instance', 'products'))
            options['dirs'] = '\n'.join( dirs )

        options.setdefault('skip', DefaultSkipDirs)
        options.setdefault('rx', DefaultRX)
        

    def install(self):
        self.compileAll()
        return []


    def update(self):
        self.compileAll()
        return []


    def findValuesByRecipe(self, recipe, key):
        """
        Find all the values matching key in all the recipes matching recipe
        """
        return set( [ part[key] for part in self.buildout.values() if (part.get('recipe') == recipe) and part.has_key(key) ] )
        

    def compileAll(self):
        
        dirs = self.options['dirs'].split()
        skip = self.options['skip'].split()
        rexp = self.options['rx']

        if rexp:
            rx = re.compile(rexp)
        else:
            rx = None
        for dir in dirs:
            print '  precompiling python scripts in %s' % dir
            compile_non_skip(dir, skip, rx)
