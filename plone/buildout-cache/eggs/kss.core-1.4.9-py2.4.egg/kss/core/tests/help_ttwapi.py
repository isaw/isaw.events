from zope import event
from zope.lifecycleevent import ObjectModifiedEvent

def objectModified(context):
    event.notify(ObjectModifiedEvent(context))
