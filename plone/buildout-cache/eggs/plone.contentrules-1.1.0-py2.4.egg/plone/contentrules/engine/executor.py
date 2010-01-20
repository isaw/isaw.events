from zope.interface import implements
from zope.component import adapts, getMultiAdapter

from plone.contentrules.engine.interfaces import IRuleExecutor
from plone.contentrules.engine.interfaces import IRuleAssignable
from plone.contentrules.engine.interfaces import IRuleAssignmentManager

from plone.contentrules.engine.interfaces import StopRule

from plone.contentrules.rule.interfaces import IExecutable

class RuleExecutor(object):
    """An object that can execute rules in its context.
    """
    
    implements(IRuleExecutor)
    adapts(IRuleAssignable)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, event, bubbled=False, rule_filter=None):
        assignments = IRuleAssignmentManager(self.context)
        for rule in assignments.getRules(event, bubbled=bubbled):
            if rule_filter is None or rule_filter(self.context, rule, event) == True:
                executable = getMultiAdapter((self.context, rule, event), IExecutable)
                executable()
                if rule.stop:
                    raise StopRule(rule)
