# a rudimentary Plone controller that works through
# subprocesses operating the zope instance command line.
# Should work on any platform.

import os, sys, subprocess, copy
import config

from states import *

class OperatePlatform():
    def _runCmd(self, cmd):
        ctl = config.getZope().getInstanceCtl()
        cmd = '%s %s' % (ctl, cmd)
        print cmd

        # The current python has probably set some
        # environment variables that may interfere
        # with calling our own python
        env = copy.deepcopy(os.environ)
        del env['PYTHONPATH']
        del env['PYTHONEXECUTABLE']
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
        out, err = p.communicate()
        print "status: %s, output: %s, error: %s" % (p.returncode, out, err)
        return out
    
    def start(self):
        return self._runCmd('start')
    
    def stop(self):
        return self._runCmd('stop')

    def isRunning(self):
        output = self._runCmd('status')
        # first status attempt seems to often fail;
        # so a little superstitious coding:
        output = self._runCmd('status')
        if output.find('program running') >= 0:
            return STARTED
        else:
            return STOPPED

if __name__ == '__main__':
    print config.getZope().getInstanceName()
    if len(sys.argv) > 1:
        print OperatePlatform()._runCmd(sys.argv[1])
    else:
        print OperatePlatform()._runCmd('status')