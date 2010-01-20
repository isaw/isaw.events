#!/usr/bin/env pythonw

import sys, wx


class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, app):
        self.app = app
        wx.Frame.__init__(self, parent, -1, app.caption,
                          pos=(-1, -1), size=(35, 20),
                          style= wx.CAPTION )        

        panel = wx.Panel(self)

        title = wx.StaticText(panel, -1, app.title)
        title.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        title.SetSize(title.GetBestSize())
        description = wx.StaticText(panel, -1, app.message)
        description.SetSize(description.GetBestSize())

        self.guage = wx.Gauge(self, -1, 100, (110, 50), (250, 25))

        self.status = wx.StaticText(panel, -1, '')
        self.status.SetSize(self.status.GetBestSize())

        btn = wx.Button(panel, -1, app.okText)
        btn.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnClose, btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer.Add(description, 0, wx.LEFT | wx.RIGHT, 10)
        sizer.Add(self.guage, 0, wx.LEFT | wx.RIGHT, 10)
        sizer.Add(self.status, 0, wx.LEFT | wx.RIGHT, 10)
        sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        panel.SetSizer(sizer)
        panel.Layout()
        panel.Fit()
        self.Fit()
        

    def OnClose(self, evt):
        self.Close()


class GuageApp(wx.App):
    
    def __init__(self, message, title, caption, okText='Cancel'):
        self.message=message
        self.title=title
        self.caption=caption
        self.okText =okText
        wx.App.__init__(self, redirect=False)
    
    def OnInit(self):
        self.result = None
        
        self.frame = MyFrame(None, self)
        self.SetTopWindow(self.frame)

        self.frame.Center(wx.BOTH)
        self.frame.Show(True)
        
        self.doWork()
        
        return True

    def Close(self):
        self.frame.Close()
        
    def setGuage(self, count, statusmsg=''):
        self.frame.guage.SetValue(count)
        self.frame.status.SetLabel(statusmsg)
        self.frame.Update()

    def doWork(self):
        """ Override me """
        pass

if __name__ == '__main__':

    class TestApp(GuageApp):
        def doWork(self):
            self.setGuage(5, 'Five')
            wx.Yield()
            wx.Sleep(1)
            wx.Yield()
            self.setGuage(25, 'Twentyfive')
            wx.Yield()
            wx.Sleep(1)
            wx.Yield()
            self.setGuage(50, 'Fifty')
            wx.Yield()
            wx.Sleep(1)
            wx.Yield()
            self.setGuage(75, 'Seventyfive')
            wx.Yield()
            wx.Sleep(1)
            wx.Yield()
            self.setGuage(100, 'One Hundred')
            wx.Yield()
            wx.Sleep(1)
            wx.Yield()
            self.Close()

    app = TestApp('message', 'title', 'caption')
    app.MainLoop()
