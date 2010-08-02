"""Definition of the Sponsored content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from isaw.events.interfaces import ISponsored
from isaw.events.config import PROJECTNAME

SponsoredSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

SponsoredSchema['title'].storage = atapi.AnnotationStorage()
SponsoredSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    SponsoredSchema,
    folderish=True,
    moveDiscussion=False
)


class Sponsored(folder.ATFolder):
    """Sponsored Event"""
    implements(ISponsored)

    meta_type = "Sponsored"
    schema = SponsoredSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Sponsored, PROJECTNAME)
