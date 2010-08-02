"""Definition of the Exhibition content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from isaw.events.interfaces import IExhibition
from isaw.events.config import PROJECTNAME

ExhibitionSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ExhibitionSchema['title'].storage = atapi.AnnotationStorage()
ExhibitionSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ExhibitionSchema,
    folderish=True,
    moveDiscussion=False
)


class Exhibition(folder.ATFolder):
    """Exhibition Event"""
    implements(IExhibition)

    meta_type = "Exhibition"
    schema = ExhibitionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Exhibition, PROJECTNAME)
