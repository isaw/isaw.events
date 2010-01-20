from zope.app.pagetemplate import ViewPageTemplateFile
from plone.app.content.batching import Batch
from plone.memoize import instance

try:
    from kss.core import KSSView
except ImportError:
    from Products.Five import BrowserView as KSSView


class Table(object):
    """   
    The table renders a table with sortable columns etc.

    It is meant to be subclassed to provide methods for getting specific table info.
    """                

    def __init__(self, request, base_url, view_url, items, show_sort_column=False,
                 buttons=[], pagesize=20):
        self.request = request
        self.context = None # Need for view pagetemplate

        self.base_url = base_url
        self.view_url = view_url
        self.url = view_url
        self.items = items
        self.show_sort_column = show_sort_column
        self.buttons = buttons
        self.default_page_size = 20
        self.pagesize = pagesize
        self.show_all = request.get('show_all', '').lower() == 'true'

        selection = request.get('select')
        if selection == 'screen':
            self.selectcurrentbatch=True
        elif selection == 'all':
            self.selectall = True

        self.pagenumber =  int(request.get('pagenumber', 1))

    @property
    def within_batch_size(self):
        return len(self.items) < self.pagesize

    def set_checked(self, item):
        selected = self.selected(item)
        item['checked'] = selected and 'checked' or None
        item['table_row_class'] = item.get('table_row_class', '')
        if selected:
            item['table_row_class'] += ' selected'

    @property
    @instance.memoize
    def batch(self):
        pagesize = self.pagesize
        if self.show_all:
            pagesize = len(self.items)
        b = Batch(self.items,
                  pagesize=pagesize,
                  pagenumber=self.pagenumber)
        map(self.set_checked, b)
        return b

    render = ViewPageTemplateFile("table.pt")
    batching = ViewPageTemplateFile("batching.pt")

    # options
    _selectcurrentbatch = False
    _select_all = False

    def _get_select_currentbatch(self):
        return self._selectcurrentbatch

    def _set_select_currentbatch(self, value):
        self._selectcurrentbatch = value
        if self._selectcurrentbatch and self.show_all or (
            len(self.items) <= self.pagesize):
            self.selectall = True

    selectcurrentbatch = property(_get_select_currentbatch,
                                  _set_select_currentbatch)

    def _get_select_all(self):
        return self._select_all

    def _set_select_all(self, value):
        self._select_all = bool(value)
        if self._select_all:
            self._selectcurrentbatch = True

    selectall = property(_get_select_all, _set_select_all)

    @property
    def show_select_all_items(self):
        return self.selectcurrentbatch and not self.selectall

    def get_nosort_class(self):
        """
        """
        return "nosort"

    @property
    def selectall_url(self):
        return self.selectnone_url+'&select=all'

    @property
    def selectscreen_url(self):
        return self.selectnone_url+'&select=screen'

    @property
    def selectnone_url(self):
        base = self.view_url + '?pagenumber=%s' % (self.pagenumber)
        if self.show_all:
            base += '&show_all=true'
        return base

    @property
    def show_all_url(self):
        return self.view_url + '?show_all=true'

    def selected(self, item):
        if self.selectcurrentbatch:
            return True
        return False

    @property
    def viewname(self):
        return self.view_url.split('?')[0].split('/')[-1]

class TableKSSView(KSSView):
    '''Base class which can be used from a KSS view

    Subclasses only need to set the table property to a different
    class.'''
    
    table = None

    def update_table(self, pagenumber='1', sort_on='getObjPositionInParent', show_all=False):
        self.request.set('sort_on', sort_on)
        self.request.set('pagenumber', pagenumber)
        table = self.table(self.context, self.request,
                                    contentFilter={'sort_on':sort_on})
        core = self.getCommandSet('core')
        core.replaceHTML('#folderlisting-main-table', table.render())
        return self.render()
