import logging
import os

class Recipe:
    def __init__(self, buildout, name, options):
        self.options = options
        self.logger = logging.getLogger(name)

    def install(self):
        command = self.options['command']
        self.logger.info("Running %s" % command)
        os.system(command)
        location = self.options.get('location')
        if location is not None:
            return location.split()
        else:
            return ()

    def update(self):
        command = self.options.get('update-command')
        if command is not None:
            self.logger.info("Running %s" % command)
            os.system(command)
