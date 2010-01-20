# Notebook.py -- contains functional pages
# in a tabbed notebook


import  sys

import  wx

import statusPage, configPage

class ColoredPanel(wx.Window):
   def __init__(self, parent, color):
       wx.Window.__init__(self, parent, -1, style = wx.SIMPLE_BORDER)
       self.SetBackgroundColour(color)
       if wx.Platform == '__WXGTK__':
           self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

#----------------------------------------------------------------------------

class TestNB(wx.Notebook):
    def __init__(self, parent, id):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT)

        self.parent = parent
        self.pages = []
                             
        win = statusPage.statusPage(self)
        self.AddPage(win, "Status")
        self.pages.append(win)

        win = configPage.configPage(self)
        self.AddPage(win, "Configuration Details")
        self.pages.append(win)

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

        self.Fit()

        


    def makeColorPanel(self, color):
        p = wx.Panel(self, -1)
        win = ColoredPanel(p, color)
        p.win = win
        def OnCPSize(evt, win=win):
            win.SetPosition((0,0))
            win.SetSize(evt.GetSize())
        p.Bind(wx.EVT_SIZE, OnCPSize)
        return p


    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        
        if hasattr(self.pages[old], "postDeactivate"):
            self.pages[old].postDeactivate()
        if hasattr(self.pages[new], "postInitialize"):
            self.pages[new].postInitialize()
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        print('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

#----------------------------------------------------------------------------

def runTest(frame, nb):
    testWin = TestNB(nb, -1)
    return testWin
