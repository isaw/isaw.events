from persistent import Persistent

from zope.interface import implements, implementer
from zope.component import adapter, queryUtility

from zope.annotation.interfaces import IAnnotations
from zope.app.container.ordered import OrderedContainer
from zope.app.container.contained import Contained

from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.engine.interfaces import IRuleAssignable
from plone.contentrules.engine.interfaces import IRuleAssignment
from plone.contentrules.engine.interfaces import IRuleAssignmentManager

from BTrees.OOBTree import OOBTree

KEY = 'plone.contentrules.localassignments'
    
class RuleAssignment(Contained, Persistent):
    """An assignment of a rule to a context
    """
    implements(IRuleAssignment)
    
    def __init__(self, ruleid, enabled=True, bubbles=False):
        super(RuleAssignment, self).__init__()
        self.__name__ = ruleid
        self.enabled = enabled
        self.bubbles = bubbles
    
class RuleAssignmentManager(OrderedContainer):
    """A context-specific container for rule assignments
    """
    implements(IRuleAssignmentManager)
    
    def __init__(self):
        # XXX: This depends on implementation detail in OrderedContainer,
        # but it uses a PersistentDict, which sucks :-/
        OrderedContainer.__init__(self)
        self._data = OOBTree()

    def getRules(self, event, bubbled=False):
        rules = []
        storage = queryUtility(IRuleStorage)
        if storage is not None:
            for a in self.values():
                if a.enabled and (bubbled == False or a.bubbles):
                    r = storage.get(a.__name__, None)
                    if r is not None and r.enabled and r.event.providedBy(event):
                        rules.append(r)
        return rules

@adapter(IRuleAssignable)
@implementer(IRuleAssignmentManager)
def ruleAssignmentManagerAdapterFactory(context):
    """When adapting an IRuleAssignable, get an IRuleAssignmentManager by 
    finding one in the object's annotations. The container will be created 
    if necessary.
    """
    annotations = IAnnotations(context)
    manager = annotations.get(KEY, None)
    if manager is None:
        manager = annotations[KEY] = RuleAssignmentManager()
    return manager