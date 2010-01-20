from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate

from Acquisition import aq_get

from Products.CMFCore.utils import getToolByName
_ = MessageFactory('plone')

class WorkflowsVocabulary(object):
    """Vocabulary factory for workflows.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.Workflows'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> class Workflow(object):
      ...     def __init__(self, id, title):
      ...         self.id = id
      ...         self.title = title

      >>> tool = DummyTool('portal_workflow')
      >>> def objectValues():
      ...     return (Workflow('default', 'Default Workflow'),
      ...             Workflow('intranet', 'Intranet Workflow'))
      >>> tool.objectValues = objectValues
      >>> context2.portal_workflow = tool

      >>> workflows = util(context1)
      >>> workflows
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(workflows.by_token)
      2

      >>> intranet = workflows.by_token['intranet']
      >>> intranet.title, intranet.token, intranet.value
      ('Intranet Workflow', 'intranet', 'intranet')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        wtool = getToolByName(context, 'portal_workflow', None)
        if wtool is None:
            return None
        items = [(w.title, w.id) for w in wtool.objectValues()]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)

WorkflowsVocabularyFactory = WorkflowsVocabulary()

class WorkflowStatesVocabulary(object):
    """Vocabulary factory for workflow states.

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.WorkflowStates'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> tool = DummyTool('portal_workflow')
      >>> def listWFStatesByTitle(filter_similar=None):
      ...     return (('Private', 'private'), ('Published', 'published'))
      >>> tool.listWFStatesByTitle = listWFStatesByTitle
      >>> context2.portal_workflow = tool

      >>> states = util(context1)
      >>> states
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(states.by_token)
      2

      >>> pub = states.by_token['published']
      >>> pub.title, pub.token, pub.value
      (u'Published [published]', 'published', 'published')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        # XXX This is evil. A vocabulary shouldn't be request specific.
        # The sorting should go into a separate widget.
        request = aq_get(context, 'REQUEST', None)
        wtool = getToolByName(context, 'portal_workflow', None)
        if wtool is None:
            return None
        items = wtool.listWFStatesByTitle(filter_similar=True)
        items_dict = dict([(i[1], translate(_(i[0]), context=request)) for i in items])
        items_list = [(k, v) for k, v in items_dict.items()]
        items_list.sort(lambda x, y: cmp(x[1], y[1]))
        terms = [SimpleTerm(k, title=u'%s [%s]' % (v, k)) for k, v in items_list]
        return SimpleVocabulary(terms)

WorkflowStatesVocabularyFactory = WorkflowStatesVocabulary()


class WorkflowTransitionsVocabulary(object):
    """Vocabulary factory for workflow transitions

      >>> from zope.component import queryUtility
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> name = 'plone.app.vocabularies.WorkflowTransitions'
      >>> util = queryUtility(IVocabularyFactory, name)
      >>> context1 = DummyContext()
      >>> context2 = DummyContext()
      >>> context1.context = context2

      >>> util(context1) is None
      True

      >>> class Transition(object):
      ...     def __init__(self, id, actbox_name):
      ...         self.id = id
      ...         self.actbox_name = actbox_name

      >>> class TransitionsFolder(object):
      ...     def __init__(self, values):
      ...         self.values = values
      ...
      ...     def objectValues(self):
      ...         return self.values

      >>> class Workflow(object):
      ...     def __init__(self, id, title, values):
      ...         self.id = id
      ...         self.title = title
      ...         self.transitions = TransitionsFolder(values)

      >>> tool = DummyTool('portal_workflow')
      >>> t1 = Transition('publish', 'Publish')
      >>> t2 = Transition('reject', 'Reject')

      >>> wf1 = Workflow('default', 'Default Workflow', (t1, t2))
      >>> wf2 = Workflow('intranet', 'Intranet Workflow', (t1, ))

      >>> def objectValues():
      ...     return (wf1, wf2)
      >>> tool.objectValues = objectValues
      >>> context2.portal_workflow = tool

      >>> transitions = util(context1)
      >>> transitions
      <zope.schema.vocabulary.SimpleVocabulary object at ...>

      >>> len(transitions.by_token)
      2

      >>> pub = transitions.by_token['Publish [publish]']
      >>> pub.title, pub.token, pub.value
      (None, 'Publish [publish]', 'publish')
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        wtool = getToolByName(context, 'portal_workflow', None)
        if wtool is None:
            return None

        transitions = {}
        for wf in wtool.objectValues():
            transition_folder = getattr(wf, 'transitions', None)
            wf_name = wf.title or wf.id
            if transition_folder is not None:
                for transition in transition_folder.objectValues():
                    transition_title = transition.actbox_name
                    transitions.setdefault(transition.id, []).append(dict(title=transition_title,
                                                                        wf_name=wf_name))
        items = []
        for transition_id, info in transitions.items():
            titles = set([i['title'] for i in info])
            item_title = ' // '.join(sorted(titles))
            items.append(("%s [%s]" % (item_title, transition_id,), transition_id),)

        return SimpleVocabulary.fromItems(sorted(items))

WorkflowTransitionsVocabularyFactory = WorkflowTransitionsVocabulary()
