# statusPage.py -- Plone status and browser launchers 

import wx

import config, status, webBrowser

def create(parent):
    return statusPage(parent)

# times in milliseconds
TIMERSLOW = 30000
TIMERMED  = 20000
TIMERFAST = 1000
TIMERVFAST = 100

from states import STARTING, STOPPING, STARTED, STOPPED, UNKNOWN
from status import EVT_UPDATE_STATUS


class statusPage(wx.Window):

    def __init__(self, *args, **kwargs):
        wx.Window.__init__(self, *args, **kwargs)
        
        parent = args[0]
        panel = wx.Panel(self)

        self.staticBoxState = wx.StaticBox(
              label='Status', name='staticBoxState', parent=panel)

        self.buttonChange = wx.Button(label='Start Plone', name='buttonChange', parent=panel)
        self.Bind(wx.EVT_BUTTON, self.OnStatusChange, self.buttonChange)

        self.staticTextState = wx.StaticText(
              label="Unknown state, determining...", name='staticTextState', parent=panel)

        self.staticBoxWebControls = wx.StaticBox(
              label='Site Management', name='staticBoxWebControls', parent=panel)

        self.ViewPlone = wx.Button(label='View Plone...', name='ViewPlone', parent=panel)
        self.Bind(wx.EVT_BUTTON, self.OnViewPlone, self.ViewPlone)

        self.ManageRoot = wx.Button(label='Zope Management Interface...',
              name='ManageRoot',
              parent=panel)
        self.Bind(wx.EVT_BUTTON, self.OnManageRoot, self.ManageRoot)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        ssizer1 = wx.StaticBoxSizer(self.staticBoxState, wx.VERTICAL)
        ssizer1.Add(self.staticTextState, 0, wx.ALL, 10)
        ssizer1.Add(self.buttonChange, 0, wx.ALL, 10)
        sizer.Add(ssizer1, 0, wx.ALL + wx.EXPAND, 10)

        ssizer2 = wx.StaticBoxSizer(self.staticBoxWebControls, wx.VERTICAL)
        ssizer2.Add(self.ViewPlone, 0, wx.ALL, 10)
        ssizer2.Add(self.ManageRoot, 0, wx.ALL, 10)
        sizer.Add(ssizer2, 0, wx.ALL + wx.EXPAND, 10)

        panel.SetSizer(sizer)
        panel.Layout()
        panel.Fit()
        self.Fit()

        self._zope = status.Operate()
        
        # self.parent = parent

        self._lastStatus = None

        # connect EVT_UPDATE_STATUS to OnUpdate
        self.Connect(-1, -1, EVT_UPDATE_STATUS, self.OnUpdate)

        # set up timer, connect to OnUpdate
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnUpdate, self.timer)
        self.DoChangeStatus(UNKNOWN)
        
        
    def OnStatusChange(self, event):
        print "Status button pushed"
        
        if self._zope.getStatus(self) == STARTED:
            wx.PostEvent(self, status.UpdateEvent(STOPPING))
            self._zope.stop()
        else:
            wx.PostEvent(self, status.UpdateEvent(STARTING))
            self._zope.start()
        
        event.Skip()


    def OnManageRoot(self, event):
        print "OnManageRoot"
        webBrowser.launchurl(config.getZope().getManageURL())


    def OnViewPlone(self, event):
        print "OnViewPlone"
        webBrowser.launchurl(config.getZope().getURL())


    def postInitialize(self):
        """ this page is being shown """
        
        print "postInitialize"
        # XXX: cursor set is not working.
        self.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
        self.OnUpdate()
        self.timer.Start()
        self.SetCursor(wx.STANDARD_CURSOR)


    def postDeactivate(self):
        """ this page is being hidden """
        
        print "postDeactivate"
        self.timer.Stop()


    def ChangeTimer(self, time=TIMERSLOW):
        print "ChangeTimer: %s" % time
        self.timer.Stop()
        self.timer.Start(time)


    def OnNotExpected(self, err_msg=None):
        print "OnNotExpected"
        msg = """An error occured when changing the state of this service
and it is now in a state that was not expected. This likely means that an
error occured in the service.
||
You could also try running this Plone instance in debug mode. To do
this go to the bin directory of its folder and the service manually.
This normally provides you with detailed feedback of the problem.""".replace('/n', ' ').replace('|', '\n')
        if err_msg:
            msg += """

Error message: %s""" % err_msg
        wx.GetApp().Error(msg)


    def DoChangeStatus(self, action, msg=None):
        """ When you fire off a request... """
        
        e = getattr(self, "_expected", [])
        print "DoChangeStatus: action %s, expected %s" % (action, e)

        self.staticTextState.SetLabel(self._getMessage(action))
        self.buttonChange.SetLabel(self._getLabel(action))

        if e and action not in e:
            self.OnNotExpected(msg)
            self._expected = []

        if action == STOPPING:
            self.buttonChange.Enable(False)
            self.ChangeTimer(TIMERMED)
            self._expected = [STOPPED, STOPPING]
            self.ManageRoot.Enable(False)
            self.ViewPlone.Enable(False)

        elif action == STARTING:
            self.buttonChange.Enable(False)
            self.ChangeTimer(TIMERMED)
            self._expected = [STARTED, STARTING]

        elif action == STARTED:
            self.buttonChange.Enable(True)
            self.ChangeTimer()
            self._expected = []
            self.ManageRoot.Enable(True)
            self.ViewPlone.Enable(True)

        elif action == STOPPED:
            self.buttonChange.Enable(True)
            self.ChangeTimer()
            self._expected = []
            self.ManageRoot.Enable(False)
            self.ViewPlone.Enable(False)

        elif action == UNKNOWN:
            self.buttonChange.Enable(False)
            self.ChangeTimer(TIMERVFAST)
            self._expected = []

        else:
            raise ValueError, "Unknown error"

        self._lastStatus = action


    def OnUpdate(self, evt=None):
        print "OnUpdate, evt: %s" % getattr(evt, 'status', None)

        if evt is not None and hasattr(evt, "status"):
            newStatus = evt.status
        else:
            newStatus = self._zope.getStatus()
        print "old status: %s, new status: %s" % (self._lastStatus, newStatus)

        if self._lastStatus != newStatus:
            self.DoChangeStatus(newStatus)


    def _getLabel(self, action):
        return {
            STARTING:"Starting...",
            STOPPING:"Stopping...",
            STARTED:"Stop Plone",
            STOPPED:"Start Plone",
            UNKNOWN:"Unknown",
            }[action]


    def _getMessage(self, action):
        return {
            STARTING:"Starting Plone...",
            STOPPING:"Stopping Plone...",
            STARTED:"Plone is running",
            STOPPED:"Plone is not running",
            UNKNOWN:"Unknown state, determining...",
            }[action]
