#
# A generic control script for Zope
#
# Copyright (c) 2008, Plone Foundation
# Created by Steve McMahon
#

import sys, os, os.path, time, shutil, subprocess, plone.recipe.unifiedinstaller

WIN32 = False
if sys.platform[:3].lower() == "win":
    WIN32 = True

INIT_COMMAND = 'init'
# commands that might make sense issued to multiple targets in a ZEO context
SERVER_COMMANDS = ("start", "stop", "status", "restart",)
if WIN32:
     SERVER_COMMANDS = SERVER_COMMANDS + ("install", "remove")
# commands that make sense issued to a single target
CLIENT_COMMANDS = SERVER_COMMANDS + ("fg", "debug", 'run', 'test', 'adduser')
ALL_COMMANDS = SERVER_COMMANDS + CLIENT_COMMANDS + (INIT_COMMAND,)


class Control(object):
    
    def __init__(self, server=None, clients=[], location=None, binDirectory=None, fileStorage=None):
        self.server = server
        self.clients = clients
        self.location = location
        self.binDirectory = binDirectory
        self.fileStorage = fileStorage
        self.fileStorageDir = os.path.dirname(fileStorage)
        self.firstTime = not os.path.exists(self.fileStorage)
        self.modulePath = plone.recipe.unifiedinstaller.__path__[0]
        # put initial components and commands into self.commands,
        # the rest into self.arguments
        self.commands = []
        self.arguments = []
        afound = False
        acommands = (self.server, 'server', 'clients') + tuple(self.clients) + ALL_COMMANDS
        for item in sys.argv[1:]:
            if not afound:
                if item in acommands:
                    self.commands.append(item)
                else:
                    afound = True
            if afound:
                self.arguments.append(item)


    def usage(self):
        if self.server:
            print "usage: plonectl %s [component]\n" % ' | '.join(SERVER_COMMANDS)
            print "Available components:"
            print "    Server : %s" % self.server
            print "    Clients: %s" % ' '.join(self.clients)
            print "\nIf no component is specified, command will be applied to all."
            print 'You may also use "clients" to refer to all clients.\n'
        else:
            print "usage: plonectl %s\n" % ' | '.join(CLIENT_COMMANDS)
        sys.exit(1)


    def runCommand(self, command, arg=''):
        # run a shell command, return error code

        # make sure output is synchronized with prints
        sys.stdout.flush()
        
        if isinstance(arg, (tuple, list)):
            args = list(arg) + self.arguments
        else:
            args = [arg,] + self.arguments
        
        command_script = os.path.join(self.binDirectory, 
                                      "%s-script.py" % command)
        if os.path.exists(command_script):
            args = [sys.executable, command_script] + args
        else:
            args = [os.path.join(self.binDirectory, command)] + args
            
        po = subprocess.Popen(args)
        try:
            po.communicate()
        except KeyboardInterrupt:
            return 1
        return po.returncode
        


    def init_storage(self):
        if self.firstTime:
            component = self.clients[0]
            print 'This is the first start of this instance.'
            print 'Creating Data.fs and a Plone site.'
            print 'We only need to do this once, but it takes some time.'
            print 'Creating Plone site at /Plone in ZODB...'
            self.runCommand(
                component,
                ['run',
                 os.path.join(self.modulePath, 'mkPloneSite.py'),
                 os.path.join(self.modulePath, 'plone_init_content')])
            self.firstTime = False
    

def main(server=None, clients=[], location=None, binDirectory=None, fileStorage=None):

    controller = Control(server, clients, location, binDirectory, fileStorage)
    
    if not os.path.exists(controller.fileStorageDir):
        print >> sys.stderr, "%s doesn't exist. Run bin/buildout to configure your installation." % controller.fileStorageDir
        sys.exit(1)

    if not os.access(controller.fileStorageDir, os.W_OK):
        print >> sys.stderr, "You lack the rights necessary to run this script; Try sudo %s" % sys.argv[0]
        sys.exit(1)

    if len(controller.commands) == 1:
        command = controller.commands[0].lower()
        if controller.server:
            # we're going to restrict ourselves to the
            # subset of commands that make sense
            # when starting both a server and clients.
            validCommands = SERVER_COMMANDS
        else:
            validCommands = CLIENT_COMMANDS
        if command in validCommands:
            if controller.server:
                sys.stdout.write("%s: " % controller.server)
                returncode = controller.runCommand(controller.server, command)
                if returncode: sys.exit(returncode)
            if command in ('start', 'fg'):                    
                controller.init_storage()
            for component in controller.clients:
                time.sleep(1)
                sys.stdout.write("%s: " % component)
                returncode = controller.runCommand(component, command)
                if returncode: sys.exit(returncode)                    
        elif command == INIT_COMMAND:
            controller.init_storage()
        else:
            print "Invalid command: %s" % command
            print "Valid commands in this context are: %s\n" % ', '.join(validCommands)
            controller.usage()
    elif len(controller.commands) == 2:
        command = controller.commands[0].lower()
        target = controller.commands[1].lower()
        if target in CLIENT_COMMANDS:
            # swap target and command
            s = target
            target = command
            command = s
        if command in CLIENT_COMMANDS:
            if target in ('zeoserver', 'zeo', 'server', controller.server) and \
               controller.server and \
               command in SERVER_COMMANDS:
                sys.stdout.write("%s: " % controller.server)
                returncode = controller.runCommand(controller.server, command)
                if returncode: sys.exit(returncode)                    
                if command in ('start', 'fg'):                    
                    controller.init_storage()
            elif target in controller.clients:
                sys.stdout.write("%s: " % target)
                returncode = controller.runCommand(target, command)
                if returncode: sys.exit(returncode)                    
            elif target == 'clients':
                for component in controller.clients:
                    time.sleep(1)
                    sys.stdout.write("%s: " % component)
                    returncode = controller.runCommand(component, command)
                    if returncode: sys.exit(returncode)                    
            else:
                print "No such component: %s\n" % target
                controller.usage()
        else:
            print "Invalid command: %s\n" % command
            controller.usage()
    else:
        controller.usage()
