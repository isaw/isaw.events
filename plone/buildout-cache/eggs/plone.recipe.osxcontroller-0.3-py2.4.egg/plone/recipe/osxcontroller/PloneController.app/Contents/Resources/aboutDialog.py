import sys, os.path

import wx
import wx.html
import wx.lib.wxpTag

#---------------------------------------------------------------------------

class MyAboutBox(wx.Dialog):
    text = '''
<html>
<body>
<center>
<table width="100%%" cellspacing="0" cellpadding="20" border="1">
<tr>
    <td align="center">
    <img src="%s" />
    <h2>Plone Controller</h2>
    <h3>version %s</h3>
    <p>Plone Controller by Andy McKay and Alexander Limi, updated by Steve McMahon.</p>
    </td>
</tr>
</table>


<p><wxp module="wx" class="Button">
    <param name="label" value="Okay">
    <param name="id"    value="ID_OK">
</wxp></p>
</center>
</body>
</html>
'''
    def __init__(self, parent):

        mypath = os.path.dirname(__file__)
        version = open(os.path.join(mypath, 'version.txt')).read()
        iconpath = os.path.join(mypath, 'images', 'plone-icon.png')
        
        wx.Dialog.__init__(self, parent, -1, 'About the Plone Controller',)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        py_version = sys.version.split()[0]
        txt = self.text % (iconpath, version)
        html.SetPage(txt)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)

#---------------------------------------------------------------------------



if __name__ == '__main__':
    app = wx.PySimpleApp()
    dlg = MyAboutBox(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()

