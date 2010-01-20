"""Definition of the Events content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from isaw.events import eventsMessageFactory as _
from isaw.events.interfaces import IEvents
from isaw.events.config import PROJECTNAME

EventsSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

EventsSchema['title'].storage = atapi.AnnotationStorage()
EventsSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    EventsSchema,
    folderish=True,
    moveDiscussion=False
)

class Events(folder.ATFolder):
    """ISAW Events Module"""
    implements(IEvents)

    meta_type = "Events"
    schema = EventsSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Events, PROJECTNAME)
