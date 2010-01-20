import os.path

from Products.MimetypesRegistry import MimeTypesRegistry
from Products.MimetypesRegistry.common import skins_dir

GLOBALS = globals()
PKG_NAME = 'MimetypesRegistry'

tools = (
    MimeTypesRegistry.MimeTypesRegistry,
    )

from Products.MimetypesRegistry import mime_types

# TODO: figure out if this is used/needed anywhere
import sys
from Products.MimetypesRegistry import MimeTypeItem
sys.modules['Products.MimetypesRegistry.zope.MimeTypeItem'] = MimeTypeItem
# end TODO

def initialize(context):
    from Products.CMFCore import utils
    utils.ToolInit("%s Tool" % PKG_NAME, 
                   tools=tools,
                   icon="tool.gif",
                   ).initialize(context)
