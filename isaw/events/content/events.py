"""Definition of the events content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from isaw.events import eventsMessageFactory as _
from isaw.events.interfaces import Ievents
from isaw.events.config import PROJECTNAME

eventsSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

eventsSchema['title'].storage = atapi.AnnotationStorage()
eventsSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    eventsSchema,
    folderish=True,
    moveDiscussion=False
)

class events(folder.ATFolder):
    """ISAW Events Module"""
    implements(Ievents)

    meta_type = "events"
    schema = eventsSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(events, PROJECTNAME)
