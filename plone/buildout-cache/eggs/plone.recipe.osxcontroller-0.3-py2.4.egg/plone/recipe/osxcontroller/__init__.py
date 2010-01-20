# -*- coding: utf-8 -*-
"""Recipe osxcontroller"""

import os, os.path, shutil

appname = 'PloneController.app'

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        location = self.buildout['buildout']['directory']

        app = os.path.join(os.path.dirname(__file__), appname)
        bin1 = os.path.join(location, appname)
        if os.path.islink(bin1):
            os.unlink(bin1)
        elif os.path.isdir(bin1):
            shutil.rmtree(bin1)
        if not os.path.exists(bin1):
            shutil.copytree(app, bin1)
            os.chmod(os.path.join(bin1,'Contents','MacOS','PloneController'), 0755)
            os.chmod(os.path.join(bin1,'Contents','MacOS','Python'), 0755)

        return (bin1,)


    def update(self):
        pass
