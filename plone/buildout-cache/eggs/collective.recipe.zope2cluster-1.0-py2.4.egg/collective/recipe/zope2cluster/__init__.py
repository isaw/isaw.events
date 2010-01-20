# -*- coding: utf-8 -*-
"""Recipe collective.recipe.zope2cluster"""
import os
import plone.recipe.zope2instance

class Recipe:
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        to_clone = options['instance-clone']
        instance_clone = buildout[to_clone]
        # find the options we want to copy
        # XXX this seems morally wrong...
        clone_opts = instance_clone._raw.keys()
        # now let's loop through and make a clone
        for option in clone_opts:
            if option == 'recipe' or not option in options:
                self.options[option] = instance_clone[option]
        options['location'] = os.path.join(
            buildout['buildout']['parts-directory'],
            self.name,
        )
        self.options['scripts'] = ''
        # create our cluster object using zope2instnace
        self.cluster = plone.recipe.zope2instance.Recipe(buildout, name, self.options)

    def install(self):
        """Installer"""
        options = self.options
        location = options['location']
        self.cluster.install()
        return location

    def update(self):
        """Updater"""
        options = self.options
        location = options['location']
        self.cluster.update()
        return location
