import wx, wx.html
import config

class configPage(wx.html.HtmlWindow):
    
    def __init__(self, *args, **kwargs):
        wx.html.HtmlWindow.__init__(self, *args, **kwargs)
        
        s = ''
        zconfig = config.getZope().getConfig()
        keys = zconfig.keys()
        keys.sort()
        for key in keys:
            val = zconfig[key].replace('\n', '<br />')
            if val and (key != 'name') and not key.startswith('_'):
                if key == 'user':
                    val = val.split(':')[0]
                s = "%s\n<dt><b>%s</b></dt><dd><div>%s</div><br /></dd>" % (s, key, val)
        
        self.SetPage("<html><body><h1>name: %s</h1><dl>%s</dl></body></html>" % (zconfig['name'], s))
