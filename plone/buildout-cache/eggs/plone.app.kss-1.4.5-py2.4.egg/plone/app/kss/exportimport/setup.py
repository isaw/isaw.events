'''\
Procedural methods of site setup
'''

from Products.CMFCore.utils import getToolByName

def setupMimetype(context):
    '''This setup step is needed after Archetypes has been installed.
    '''
    site = context.getSite()
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('plone-app-kss.txt') is None:
        return
    # register mimetype
    mt = getToolByName(site, 'mimetypes_registry')
    mt.manage_addMimeType('KSS (Kinetic Style Sheet)', ('text/kss', ), ('kss', ), 'text.png',
                       binary=0, globs=('*.kss', ))
