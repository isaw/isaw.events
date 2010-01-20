import itertools
from zope.interface import implements, classProvides
from zope.schema.interfaces import ISource, IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

class UsersSource(object):
    """
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> context = DummyContext()

      >>> tool = DummyTool('acl_users')
      >>> users = ('user1', 'user2')
      >>> def getUserById(value, default):
      ...     return value in users and value or default
      >>> tool.getUserById = getUserById
      >>> def searchUsers(fullname=None):
      ...     return [dict(userid=u) for u in users]
      >>> tool.searchUsers = searchUsers
      >>> context.acl_users = tool

      >>> source = UsersSource(context)
      >>> source
      <plone.app.vocabularies.users.UsersSource object at ...>

      >>> len(source.search(None))
      2

      >>> 'user1' in source, 'noone' in source
      (True, False)

      >>> source.get('user1'), source.get('noone')
      ('user1', None)
    """
    implements(ISource)
    classProvides(IContextSourceBinder)

    def __init__(self, context):
        self.context = context
        self.users = getToolByName(context, "acl_users")

    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if self.get(value) is None:
            return False
        return True

    def search(self, query):
        return [u['userid'] for u in self.users.searchUsers(fullname=query)]
        
    def get(self, value):
        return self.users.getUserById(value, None)


class UsersSourceQueryView(object):
    """
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool
      >>> from plone.app.vocabularies.tests.base import Request

      >>> context = DummyContext()

      >>> class User(object):
      ...     def __init__(self, id):
      ...         self.id = id
      ...
      ...     def getProperty(self, value, default):
      ...         return self.id
      ...
      ...     getId = getProperty

      >>> tool = DummyTool('acl_users')
      >>> users = ('user1', 'user2')
      >>> def getUserById(value, default):
      ...     return value in users and User(value) or None
      >>> tool.getUserById = getUserById
      >>> def searchUsers(fullname=None):
      ...     return [dict(userid=u) for u in users]
      >>> tool.searchUsers = searchUsers
      >>> context.acl_users = tool

      >>> source = UsersSource(context)
      >>> source
      <plone.app.vocabularies.users.UsersSource object at ...>

      >>> view = UsersSourceQueryView(source, Request())
      >>> view
      <plone.app.vocabularies.users.UsersSourceQueryView object at ...>

      >>> view.getTerm('user1')
      <zope.schema.vocabulary.SimpleTerm object at ...>

      >>> view.getValue('user1')
      'user1'

      >>> view.getValue('noone')
      Traceback (most recent call last):
      ...
      LookupError: noone

      >>> template = view.render(name='t')

      >>> u'<input type="text" name="t.query" value="" />' in template
      True

      >>> u'<input type="submit" name="t.search" value="Search" />' in template
      True

      >>> request = Request(form={'t.search' : True, 't.query' : 'value'})
      >>> view = UsersSourceQueryView(source, request)
      >>> view.results('t')
      ['user1', 'user2']
    """

    implements(ITerms,
               ISourceQueryView)

    template = ViewPageTemplateFile('searchabletextsource.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getTerm(self, value):
        user = self.context.get(value)
        token = value
        title = value
        if user is not None:
            title = user.getProperty('fullname', None) or user.getId()
        return SimpleTerm(value, token=token, title=title)

    def getValue(self, token):
        if token not in self.context:
            raise LookupError(token)
        return token

    def render(self, name):
        return self.template(name=name)

    def results(self, name):
        # check whether the normal search button was pressed
        if name+".search" in self.request.form:
            query_fieldname = name+".query"
            if query_fieldname in self.request.form:
                query = self.request.form[query_fieldname]
                if query != '':
                    return self.context.search(query)
