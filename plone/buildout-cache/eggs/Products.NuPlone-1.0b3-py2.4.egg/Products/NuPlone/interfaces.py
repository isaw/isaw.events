from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer bound to a skin
    selection in portal_skins.
    """
