from zope.app.component.hooks import getSite, setSite
from zope import event
from zope.app.publication.zopepublication import BeforeTraverseEvent

from kss.core import KSSView
from kss.core.interfaces import IKSSView
from kss.core.unicode_quirks import force_unicode

def startKSSCommands(context, request):
    view = KSSView(context, request)
    # Alec suggested we should fire the BeforeTraverseEvent, but after
    # debugging for a while I stopped caring about the event and think
    # that setSite() is the only thing we're interested in.
    setSite(view)
    return view

def getKSSCommandSet(name):
    view = retrieveView()
    cs = view.getCommandSet(name)
    return cs

def renderKSSCommands():
    view = retrieveView()
    return view.render()

def retrieveView():
    #because the view registers itself as a site,
    #we can retrieve it...
    site = getSite()
    if not IKSSView.providedBy(site):
        raise LookupError(
            "You haven't initialized the KSS response yet, "
            "do so by calling startKSSCommands(context, request).")
    return site


