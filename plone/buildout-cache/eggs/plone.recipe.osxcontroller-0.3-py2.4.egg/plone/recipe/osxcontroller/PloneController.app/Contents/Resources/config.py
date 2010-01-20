# Pull Zope configuration from .installed.cfg.
# It's a convenient place to get all the data
# for a buildout configuration because all the
# buildout variables are expanded already.


import sys, os, os.path, ConfigParser

class Zope:
    """ represents Zope configuration """

    def __init__(self, path='.', configFile='.installed.cfg'):
        self.reload = 1
        self.path = path
        self.cfgFile = os.path.realpath( os.path.join(path, configFile) )

        self.load()

    def isEmergencyUser(self):
        raise "Not implemented"
        return os.path.exists(self.getFilePath("Emergency User"))

    def removeEmergencyUser(self):
        raise "Not implemented"
        os.remove(self.getFilePath("Emergency User"))

    def createEmergencyUser(self, username, pw1, pw2):
        raise "Not implemented"

        if not username:
            raise ValueError, "No username"
        if not pw1:
            raise ValueError, "No password"
        if pw1 != pw2:
            raise ValueError, "Passwords do not match"
        pw = "{SHA}" + binascii.b2a_base64(sha.new(pw1).digest())[:-1]
        fh = open(self.getFilePath("Emergency User"), 'w')
        fh.write('%s:%s\n' % (username, pw))
        fh.close()

    def getInstanceName(self):
        return self.zopeCfg['name']

    def getInstanceHome(self):
        return self.zopeCfg['location']
    
    def getBinDir(self):
        return self.zopeCfg['bin-directory']
    
    def getInstanceCtl(self):
        return os.path.join(self.zopeCfg['bin-directory'], self.zopeCfg['name'])

    def getFilePath(self, file):
        f = filesDict[file]
        f = os.sep.join(f)
        return f

    def setPort(self, name, value):
        raise "Not implemented"

    def getPort(self, name):
        pname = "%s-address" % name
        res = self.zopeCfg.get(pname)
        if res is None:
            raise ValueError, "Unknown port"
        return res

    def getURL(self):
        return "http://localhost:%s/Plone" % self.getPort("http")

    def getManageURL(self):
        return "http://localhost:%s/manage" % self.getPort("http")

    def getConfig(self):
        if self.reload:
            self.load()
        return self.zopeCfg

    def save(self):
        raise "Not implemented"

    def load(self):
        if self.reload:
            config = ConfigParser.ConfigParser()
            print "cwd: %s" % os.getcwd()
            print "Loading config file: %s" % self.cfgFile
            config.read(self.cfgFile)
            print "Sections found: %s" % config.sections()

            # find first zope2 instance
            options = {}
            for section in config.sections():
                if config.has_option(section, 'recipe') and \
                   config.get(section, 'recipe') == 'plone.recipe.zope2instance':
                    options['name'] = section
                    for opt in config.options(section):
                        try:
                            options[opt] = config.get(section, opt)
                        except ConfigParser.InterpolationMissingOptionError:
                            # we can't interpolate buildout % vars
                            pass
                    break

            self.zopeCfg = options
            self.reload = 0

Z = None
def getZope(path='.', configFileName='.installed.cfg'):
    global Z
    if Z is None:
        Z = Zope(path=path, configFile=configFileName)
    return Z

if __name__=='__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '.'
    z = getZope(path)
    print z
    print z.getInstanceName()
    print z.getPort("http")
    print z.getInstanceCtl()
    print z.getURL()
    print z.getManageURL()
