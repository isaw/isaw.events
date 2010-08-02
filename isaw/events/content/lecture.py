"""Definition of the Lecture content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from isaw.events.content.events import eventsSchema
from isaw.events.interfaces import ILecture
from isaw.events.config import PROJECTNAME

LectureSchema = folder.ATFolderSchema.copy() + eventsSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

LectureSchema['title'].storage = atapi.AnnotationStorage()
LectureSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(LectureSchema, moveDiscussion=False)


class Lecture(folder.ATFolder):
    """Lecture Event"""
    implements(ILecture)

    meta_type = "Lecture"
    schema = LectureSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Lecture, PROJECTNAME)
