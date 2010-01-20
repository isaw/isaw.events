
import os.path
from kss.core.pluginregistry.interfaces import ICommand
from kss.core.pluginregistry.command import Command
from kss.core.pluginregistry.plugin import registerPlugin
from kss.core.deprecated import deprecated_directive
from kss.core.pluginregistry import configure as _configure

def registerCommand(_context, name, jsfile=None):
    'Directive that registers a command' 
    # check to see if the file exists
    if jsfile is not None:
        file(jsfile, 'rb').close()

    _context.action(
        discriminator = ('registerKssCommand', name, jsfile),
        callable = registerPlugin,
        args = (Command, ICommand, name, jsfile),
        )
registerCommand = deprecated_directive(registerCommand, 'azax:registerCommand',
        'use kss:registerAction with command_factory="selector" or "global"')

registerEventType = deprecated_directive(_configure.registerEventType, 'azax:registerEventType', 'use kss:registerEventType instead')
registerAction = deprecated_directive(_configure.registerAction, 'azax:registerAction', 'use kss:registerAction instead')
registerSelectorType = deprecated_directive(_configure.registerSelectorType, 'azax:registerSelectorType', 'use kss:registerSelectorType instead')
registerCommandSet = deprecated_directive(_configure.registerCommandSet, 'azax:registerCommandSet', 'use kss:registerCommandSet instead')
