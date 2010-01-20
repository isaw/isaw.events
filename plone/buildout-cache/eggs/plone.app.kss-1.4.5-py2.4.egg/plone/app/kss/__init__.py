from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from config import SKINS_DIR, GLOBALS, PROJECTNAME, ADD_CONTENT_PERM
from Products.CMFCore.DirectoryView import registerDirectory, registerFileExtension
from Products.CMFCore.FSFile import FSFile

__all__ = ()

def initialize(context):

    # register directory views
    registerDirectory(SKINS_DIR, GLOBALS)
    
    # Register kss extension to allow it used from fs skins
    registerFileExtension('kss', FSFile)

    # content initialization
    content_types, constructors, ftis = process_types( 
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERM,
        extra_constructors = constructors,
        ).initialize(context)
