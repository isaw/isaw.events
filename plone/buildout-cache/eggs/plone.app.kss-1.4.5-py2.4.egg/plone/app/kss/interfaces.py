
from zope.interface import Interface
from kss.core.interfaces import IKSSView

# Important for 2.1, in 2.5 these are defined alreadyy
# XXX IMO AT's IBaseContent should inherit IContentish and
# AT's IBaseFolder IFolderish but it's not so, however we
# provide our contentish and folderish interfaces in a way
# to include these already

# Products.CMFPlone.interfaces.siteroot.IPloneSiteRoot
class IPloneSiteRoot(Interface):
    'The portal root'
        
#Products.CMFCore.interfaces._content.IFolderish
#Products.Archetypes.interfaces._base.IBaseFolder
class IFolderish(Interface):
    'All folderish objects including AT ones'

#Products.CMFCore.interfaces._content.IContentish
#Products.Archetypes.interfaces._base.IBaseContent
class IContentish(Interface):
    'All contentish objects including AT ones'

# this is not found in 2.5

# contentish + folderish (incl. site root)
class IPortalObject(Interface):
    'All portal objects including AT ones'

class IPloneKSSView(IKSSView):
    '''View for Plone'''
