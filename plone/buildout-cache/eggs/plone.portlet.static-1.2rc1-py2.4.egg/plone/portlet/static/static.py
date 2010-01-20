from zope.interface import implements
from zope.component import getUtility

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from plone.i18n.normalizer.interfaces import IIDNormalizer

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlet.static import PloneMessageFactory as _

from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget


class IStaticPortlet(IPortletDataProvider):
    """A portlet which renders predefined static HTML.

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    text = schema.Text(
        title=_(u"Text"),
        description=_(u"The text to render"),
        required=True)

    omit_border = schema.Bool(
        title=_(u"Omit portlet border"),
        description=_(u"Tick this box if you want to render the text above "
                      "without the standard header, border or footer."),
        required=True,
        default=False)

    footer = schema.TextLine(
        title=_(u"Portlet footer"),
        description=_(u"Text to be shown in the footer"),
        required=False)

    more_url = schema.ASCIILine(
        title=_(u"Details link"),
        description=_(u"If given, the header and footer "
                      "will link to this URL."),
        required=False)

    hide = schema.Bool(
        title=_(u"Hide portlet"),
        description=_(u"Tick this box if you want to temporarily hide "
                      "the portlet without losing your text."),
        required=True,
        default=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IStaticPortlet)

    header = _(u"title_static_portlet", default=u"Static text portlet")
    text = u""
    omit_border = False
    footer = u""
    more_url = ''
    hide = False

    def __init__(self, header=u"", text=u"", omit_border=False, footer=u"",
                 more_url='', hide=False):
        self.header = header
        self.text = text
        self.omit_border = omit_border
        self.footer = footer
        self.more_url = more_url
        self.hide = hide

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('static.pt')

    @property
    def available(self):
        return not self.data.hide

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portlet-static-%s" % normalizer.normalize(header)

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IStaticPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _(u"title_add_static_portlet",
              default=u"Add static text portlet")
    description = _(u"description_static_portlet",
                    default=u"A portlet which can display static HTML text.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IStaticPortlet)
    form_fields['text'].custom_widget = WYSIWYGWidget
    label = _(u"title_edit_static_portlet",
              default=u"Edit static text portlet")
    description = _(u"description_static_portlet",
                    default=u"A portlet which can display static HTML text.")
