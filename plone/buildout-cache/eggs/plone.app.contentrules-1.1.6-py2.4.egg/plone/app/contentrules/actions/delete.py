from OFS.SimpleItem import SimpleItem
from persistent import Persistent 

from zope.interface import implements, Interface
from zope.component import adapts
from zope.formlib import form
from zope import schema

from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData

from plone.app.contentrules.browser.formhelper import NullAddForm

import transaction
from Acquisition import aq_inner, aq_parent
from ZODB.POSException import ConflictError
from Products.CMFPlone import PloneMessageFactory as _

from Products.CMFPlone import utils
from Products.statusmessages.interfaces import IStatusMessage

class IDeleteAction(Interface):
    """Interface for the configurable aspects of a delete action.
    """
             
class DeleteAction(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(IDeleteAction, IRuleElementData)
    
    element = 'plone.actions.Delete'
    summary = _(u"Delete object")
    
class DeleteActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IDeleteAction, Interface)
         
    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        obj = self.event.object
        parent = aq_parent(aq_inner(obj))
        
        transaction.savepoint()        
        
        try:
            parent.manage_delObjects(obj.getId())
        except ConflictError, e:
            raise e
        except Exception, e:
            self.error(obj, str(e))
            return False
        
        return True 

    def error(self, obj, error):
        request = getattr(self.context, 'REQUEST', None)
        if request is not None:
            title = utils.pretty_title_or_id(obj, obj)
            message = _(u"Unable to move ${name} as part of content rule 'move' action: ${error}",
                          mapping={'name' : title, 'error' : error})
            IStatusMessage(request).addStatusMessage(message, type="error")
        
class DeleteAddForm(NullAddForm):
    """A degenerate "add form"" for delete actions.
    """
    
    def create(self):
        return DeleteAction()