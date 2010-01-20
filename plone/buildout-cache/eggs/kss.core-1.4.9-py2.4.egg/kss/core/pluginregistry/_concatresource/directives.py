from zope.interface import Interface
from zope.configuration.fields import GlobalObject, Tokens, Path, \
     PythonIdentifier, MessageID
from zope.schema import TextLine, Text, Id, Choice, Float
from fields import PathList
from zope.app.component.metadirectives import IBasicViewInformation
from zope.app.publisher.browser.metadirectives import IBasicResourceInformation

try:
    from zope.security.zcml import Permission
except ImportError:
    # Zope < 2.10
    from zope.app.security.fields import Permission


class IConcatResourceDirective(IBasicResourceInformation):
    """
    Defines a concatenated browser resource
    """

    name = TextLine(
        title=u"The name of the resource",
        description=u"""
        This is the name used in resource urls. Resource urls are of
        the form site/@@/resourcename, where site is the url of
        "site", a folder with a service manager.

        We make resource urls site-relative (as opposed to
        content-relative) so as not to defeat caches.""",
        required=True
        )

    files = PathList(
        title=u"Files",
        description=u"A space separated list of resource files",
        required=True
        )

    compress_level = Choice(
        title=u"Compress level",
        description=u"Level of compression applied, by default 'safe'.",
        values=(u'none', u'safe', u'full', u'stripped', u'devel', u'safe-devel', u'full-devel'),
        required=False,
        )

    caching = Choice(
        title=u"Caching strategy",
        description=u"Enables caching in memory for faster debugging, by default not enabled.",
        values=(u'default', u'memory'),
        required=False,
        )

    lmt_check_period = Float(
        title=u"Last modification time checking",
        description=u"""Sets a grace period in seconds, until which the last modification times
                        are never fetched again from the filesystem. In other words, the system will
                        react after this time for recent changes. For debugging, it is best
                        to set this to 0, for production it can be left to the default 60.0""",
        required=False,
        )


