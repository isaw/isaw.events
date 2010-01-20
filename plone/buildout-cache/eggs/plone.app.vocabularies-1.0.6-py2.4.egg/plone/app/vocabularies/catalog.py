import itertools
from zope.interface import implements, classProvides
from zope.schema.interfaces import ISource, IContextSourceBinder

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from plone.app.vocabularies.terms import BrowsableTerm

from Products.ZCTextIndex.ParseTree import ParseError
from Products.CMFCore.utils import getToolByName


def parse_query(query, path_prefix=""):
    """ Parse the query string and turn it into a dictionary for querying the
        catalog.

        We want to find anything which starts with the given string, so we add
        a * at the end of words.

        >>> parse_query('foo')
        {'SearchableText': 'foo*'}

        If we have more than one word, each of them should have the * and
        they should be combined with the AND operator.

        >>> parse_query('foo bar')
        {'SearchableText': 'foo* AND bar*'}

        We also filter out some special characters. They are handled like
        spaces and seperate words from each other.

        >>> parse_query('foo +bar some-thing')
        {'SearchableText': 'foo* AND bar* AND some* AND thing*'}

        >>> parse_query('what? (spam) *ham')
        {'SearchableText': 'what* AND spam* AND ham*'}

        You can also limit searches to paths, if you only supply the path,
        then all contents of that folder will be searched. If you supply
        additional search words, then all subfolders are searched as well.

        >>> parse_query('path:/dummy')
        {'path': {'query': '/dummy', 'depth': 1}}

        >>> parse_query('bar path:/dummy')
        {'path': {'query': '/dummy'}, 'SearchableText': 'bar*'}

        >>> parse_query('path:/dummy foo')
        {'path': {'query': '/dummy'}, 'SearchableText': 'foo*'}

        If you supply more then one path, then only the last one is used.

        >>> parse_query('path:/dummy path:/spam')
        {'path': {'query': '/spam', 'depth': 1}}

        You can also provide a prefix for the path. This is useful for virtual
        hosting.

        >>> parse_query('path:/dummy', path_prefix='/portal')
        {'path': {'query': '/portal/dummy', 'depth': 1}}

    """
    query_parts = query.split()
    query = {'SearchableText': []}
    for part in query_parts:
        if part.startswith('path:'):
            path = part[5:]
            query['path'] = {'query': path}
        else:
            query['SearchableText'].append(part)
    text = " ".join(query['SearchableText'])
    for char in '?-+*()':
        text = text.replace(char, ' ')
    query['SearchableText'] = " AND ".join(x+"*" for x in text.split())
    if query.has_key('path'):
        if query['SearchableText'] == '':
            del query['SearchableText']
            query["path"]["depth"] = 1
        query["path"]["query"] = path_prefix + query["path"]["query"]
    return query


class SearchableTextSource(object):
    """
      >>> from plone.app.vocabularies.tests.base import Brain
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> context = DummyContext()

      >>> tool = DummyTool('portal_catalog')
      >>> rids = ('/1234', '/2345')
      >>> def getrid(value):
      ...     return value in rids and value or None
      >>> tool.getrid = getrid
      >>> def call(**values):
      ...     if values['SearchableText'].startswith('error'):
      ...         raise ParseError
      ...     return [Brain(r) for r in rids]
      >>> tool.__call__ = call
      >>> context.portal_catalog = tool

      >>> tool = DummyTool('portal_url')
      >>> def getPortalPath():
      ...     return '/'
      >>> tool.getPortalPath = getPortalPath
      >>> context.portal_url = tool

      >>> source = SearchableTextSource(context)
      >>> source
      <plone.app.vocabularies.catalog.SearchableTextSource object at ...>

      >>> '1234' in source, '1' in source
      (True, False)

      >>> source.search('')
      []

      >>> source.search('error')
      []

      >>> source.search('foo')
      <generator object ...>

      >>> list(source.search('foo'))
      ['1234', '2345']

      >>> list(source.search('bar path:/dummy'))
      ['/dummy', '1234', '2345']

      >>> source = SearchableTextSource(context, default_query='default')
      >>> list(source.search(''))
      ['1234', '2345']
    """
    implements(ISource)
    classProvides(IContextSourceBinder)

    def __init__(self, context, base_query={}, default_query=None):
        self.context = context
        self.base_query = base_query
        self.default_query = default_query
        self.catalog = getToolByName(context, "portal_catalog")
        self.portal_tool = getToolByName(context, "portal_url")
        self.portal_path = self.portal_tool.getPortalPath()
        try:
            self.encoding = getToolByName(
                context, "portal_properties").site_properties.default_charset
        except AttributeError:
            self.encoding = 'ascii'

    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if self.catalog.getrid(self.portal_path + value) is None:
            return False
        return True

    def search(self, query_string):
        query = self.base_query.copy()
        if query_string == '':
            if self.default_query is not None:
                query.update(parse_query(self.default_query, self.portal_path))
            else:
                return []
        else:
            query.update(parse_query(query_string, self.portal_path))
        
        try:
            results = (x.getPath()[len(self.portal_path):] for x in self.catalog(**query))
        except ParseError:
            return []
        
        if query.has_key('path'):
            path = query['path']['query'][len(self.portal_path):]
            if path != '':
                return itertools.chain((path,), results)
        return results

class SearchableTextSourceBinder(object):
    """Use this to instantiate a new SearchableTextSource with custom
    parameters. For example:
    
    target_folder = schema.Choice(
        title=_(u"Target folder"),
        description=_(u"As a path relative to the portal root"),
        required=True,
        source=SearchableTextSourceBinder({'is_folderish' : True}),
        )

    This ensures that the is_folderish=True is always in the query used.

      >>> query = {'query': 'query'}

      >>> binder = SearchableTextSourceBinder(query)
      >>> binder
      <plone.app.vocabularies.catalog.SearchableTextSourceBinder object at ...>

      >>> binder.query == query
      True

      >>> from plone.app.vocabularies.tests.base import Brain
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool

      >>> context = DummyContext()

      >>> tool = DummyTool('portal_catalog')
      >>> context.portal_catalog = tool

      >>> tool = DummyTool('portal_url')
      >>> def getPortalPath():
      ...     return '/'
      >>> tool.getPortalPath = getPortalPath
      >>> context.portal_url = tool

      >>> source = binder(context)
      >>> source
      <plone.app.vocabularies.catalog.SearchableTextSource object at ...>

      >>> source.base_query == query
      True
    """
    
    implements(IContextSourceBinder)
    
    def __init__(self, query, default_query=None):
        self.query = query
        self.default_query = default_query
        
    def __call__(self, context):
        return SearchableTextSource(context, base_query=self.query.copy(),
                                    default_query=self.default_query)
    

class QuerySearchableTextSourceView(object):
    """
      >>> from plone.app.vocabularies.tests.base import DummyCatalog
      >>> from plone.app.vocabularies.tests.base import DummyContext
      >>> from plone.app.vocabularies.tests.base import DummyTool
      >>> from plone.app.vocabularies.tests.base import Request

      >>> context = DummyContext()

      >>> rids = ('/1234', '/2345', '/dummy/1234')
      >>> tool = DummyCatalog(rids)
      >>> context.portal_catalog = tool

      >>> tool = DummyTool('portal_url')
      >>> def getPortalPath():
      ...     return '/dummy'
      >>> tool.getPortalPath = getPortalPath
      >>> context.portal_url = tool

      >>> source = SearchableTextSource(context)
      >>> source
      <plone.app.vocabularies.catalog.SearchableTextSource object at ...>

      >>> view = QuerySearchableTextSourceView(source, Request())
      >>> view
      <plone.app.vocabularies.catalog.QuerySearchableTextSourceView object ...>

      >>> view.getValue('a')
      Traceback (most recent call last):
      ...
      LookupError: a

      >>> view.getValue('/1234')
      '/1234'

      >>> view.getTerm(None) is None
      True

      >>> view.getTerm('1234')
      <plone.app.vocabularies.terms.BrowsableTerm object at ...>

      >>> view.getTerm('/1234')
      <plone.app.vocabularies.terms.BrowsableTerm object at ...>

      >>> template = view.render(name='t')
      >>> u'<input type="text" name="t.query" value="" />' in template
      True

      >>> u'<input type="submit" name="t.search" value="Search" />' in template
      True

      >>> request = Request(form={'t.search' : True, 't.query' : 'value'})
      >>> view = QuerySearchableTextSourceView(source, request)
      >>> list(view.results('t'))
      ['', '/1234', '']

      >>> request = Request(form={'t.search' : True, 't.query' : 'value',
      ...                         't.browse.foo' : '/foo'})
      >>> view = QuerySearchableTextSourceView(source, request)
      >>> list(view.results('t'))
      ['foo', '', '/1234', '']
      
      Titles need to be unicode:
      >>> view.getTerm(list(view.results('t'))[0]).title
      u'/foo'      
    """

    implements(ITerms,
               ISourceQueryView)

    template = ViewPageTemplateFile('searchabletextsource.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getTerm(self, value):
        if not value:
            return None
        if (not self.context.portal_path.endswith('/')) \
               and (not value.startswith('/')):
            value = '/' + value
        # get rid for path
        rid = self.context.catalog.getrid(self.context.portal_path + value)
        # first some defaults
        token = value
        title = value
        browse_token = None
        parent_token = None
        if rid is not None:
            # fetch the brain from the catalog
            brain = self.context.catalog._catalog[rid]
            title = brain.Title
            #title = brain.Title
            if brain.is_folderish:
                browse_token = value
            parent_token = "/".join(value.split("/")[:-1])
        return BrowsableTerm(value, token=token, 
                             title=title.decode(self.context.encoding), 
                             description=value,
                             browse_token=browse_token,
                             parent_token=parent_token)

    def getValue(self, token):
        if token not in self.context:
            raise LookupError(token)
        return token

    def render(self, name):
        return self.template(name=name)

    def results(self, name):
        query = ''

        # check whether the normal search button was pressed
        if name+".search" in self.request.form:
            query_fieldname = name+".query"
            if query_fieldname in self.request.form:
                query = self.request.form[query_fieldname]

        # check whether a browse button was pressed
        browse_prefix = name+".browse."
        browse = tuple(x for x in self.request.form
                       if x.startswith(browse_prefix))
        if len(browse) == 1:
            path = browse[0][len(browse_prefix):]
            query = "path:" + path
            results = self.context.search(query)
            if name+".omitbrowsedfolder" in self.request.form:
                results = itertools.ifilter(lambda x: x != path, results)
        else:
            results = self.context.search(query)

        return results