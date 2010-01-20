from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from borg.localrole.config import LOCALROLE_PLUGIN_NAME
from borg.localrole.workspace import manage_addWorkspaceLocalRoleManager

def setup_localrole_plugin(portal):
    """Install and prioritize the local-role PAS plug-in
    """
    out = StringIO()
    
    uf = getToolByName(portal, 'acl_users')

    existing = uf.objectIds()

    if LOCALROLE_PLUGIN_NAME not in existing:
        manage_addWorkspaceLocalRoleManager(uf, LOCALROLE_PLUGIN_NAME)
        activatePluginInterfaces(portal, LOCALROLE_PLUGIN_NAME, out)
    else:
        print >> out, "%s already installed" % LOCALROLE_PLUGIN_NAME
        
    return out.getvalue()
