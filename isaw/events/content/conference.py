"""Definition of the Conference content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from isaw.events.interfaces import IConference
from isaw.events.config import PROJECTNAME

ConferenceSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ConferenceSchema['title'].storage = atapi.AnnotationStorage()
ConferenceSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    ConferenceSchema,
    folderish=True,
    moveDiscussion=False
)


class Conference(folder.ATFolder):
    """Conference Event"""
    implements(IConference)

    meta_type = "Conference"
    schema = ConferenceSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Conference, PROJECTNAME)
