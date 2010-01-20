from zope.interface import implements

from kss.core import CommandSet
from interfaces import IPloneLegacyCommands

class PloneLegacyCommands(CommandSet):
    implements(IPloneLegacyCommands)
    
    def createTableOfContents(self):
        command = self.commands.addCommand('createTableOfContents')
