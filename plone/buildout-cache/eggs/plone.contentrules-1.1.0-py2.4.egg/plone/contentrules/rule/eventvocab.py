from zope.schema.interfaces import IVocabularyFactory
from zope.interface import classProvides

from zope.app.component.vocabulary import UtilityVocabulary
from plone.contentrules.rule.interfaces import IRuleEventType

class EventTypesVocabulary(UtilityVocabulary):
    """A vocabulary for event interfaces that can be selected for the 'event'
    attribute of an IRule.
    """
    interface = IRuleEventType
    classProvides(IVocabularyFactory)
