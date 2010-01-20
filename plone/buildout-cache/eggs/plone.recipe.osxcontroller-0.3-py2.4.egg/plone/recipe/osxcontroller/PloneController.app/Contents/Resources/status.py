# Operate and UpdateEvent classes

from time import time, sleep
import wx

import sys

from states import *

if sys.platform in ('win32',):
    from statusWin32 import OperatePlatform
else:
    from statusPosix import OperatePlatform


class Operate(OperatePlatform):
    """ This class starts, stops our server and
    tests for the state """

    def getStatus(self, win=None):

        print "getStatus called"

        status = self.isRunning()
        
        if win:
            evt = UpdateEvent(status)
            wx.PostEvent(win, evt)

        return status


    def restart(self):
        self.stop()
        self.start()


EVT_UPDATE_STATUS = wx.NewEventType()

class UpdateEvent(wx.PyEvent):

    def __init__(self, status):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_UPDATE_STATUS)
        self.status = status


if __name__ == '__main__':
    print Operate().getStatus()