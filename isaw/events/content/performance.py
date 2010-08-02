"""Definition of the Performance content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from isaw.events.interfaces import IPerformance
from isaw.events.config import PROJECTNAME

PerformanceSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

PerformanceSchema['title'].storage = atapi.AnnotationStorage()
PerformanceSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    PerformanceSchema,
    folderish=True,
    moveDiscussion=False
)


class Performance(folder.ATFolder):
    """Performance Event"""
    implements(IPerformance)

    meta_type = "Performance"
    schema = PerformanceSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Performance, PROJECTNAME)
