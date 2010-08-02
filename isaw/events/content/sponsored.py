"""Definition of the Sponsored content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from isaw.events.content import events
from isaw.events.interfaces import ISponsored
from isaw.events.config import PROJECTNAME

SponsoredSchema = events.eventsSchema.copy() + atapi.Schema((

    ###################
    # SPONSOR
    ###################
    atapi.StringField(
    schemata='sponsor',
    name='event_Sponsor_Name',
    widget=atapi.StringWidget(
        label=u'Event Sponsor Name',
        label_msgid='ISAW_Event_Sponsor_Name',
        il8n_domain='ISAW_Event',
        maxlength=255,
        size=50,
        ),
        
    required=False,
    searchable=True),
    
    atapi.StringField(
    schemata='sponsor',
    name='event_Sponsor_Url',
    validators = ('isURL'),
    widget=atapi.StringWidget(
        label=u'Event Sponsor Url',
        label_msgid='ISAW_Event_Sponsor_Url',
        il8n_domain='ISAW_Event',
        maxlength=255,
        size=50,
        ),
        
    required=False,
    searchable=True),
    
    atapi.ImageField(
    schemata='sponsor',
    name='event_Sponsor_Logo',
    widget=atapi.ImageWidget(
        label=u'Event Sponsor Logo',
        label_msgid='ISAW_Event_Sponsor_Logo',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),


))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

SponsoredSchema['title'].storage = atapi.AnnotationStorage()
SponsoredSchema['description'].storage = atapi.AnnotationStorage()

#override finalizeATCTSchema
def finalizeATCTSchema(schema, folderish=False, moveDiscussion=True):
    """Finalizes an ATCT type schema to alter some fields
       for the event type. This had to be overrided - cwarner
    """
    schema.moveField('relatedItems', pos='bottom')
    if folderish:
        schema['relatedItems'].widget.visible['edit'] = 'invisible'
    schema.moveField('excludeFromNav', after='allowDiscussion')
    if moveDiscussion:
        schema.moveField('allowDiscussion', after='relatedItems')

    # Categorization
    if schema.has_key('subject'):
        schema.changeSchemataForField('subject', 'tags')
    if schema.has_key('relatedItems'):
        schema.changeSchemataForField('relatedItems', 'tags')
    if schema.has_key('location'):
        schema.changeSchemataForField('location', 'default')
    if schema.has_key('language'):
        schema.changeSchemataForField('language', 'default')

    # Dates
    if schema.has_key('effectiveDate'):
        schema.changeSchemataForField('effectiveDate', 'default')
        schema.moveField('effectiveDate', after='event_EndDateTime')
    if schema.has_key('expirationDate'):
        schema.changeSchemataForField('expirationDate', 'default')    
        schema.moveField('expirationDate', after='effectiveDate')
    if schema.has_key('creation_date'):
        schema.changeSchemataForField('creation_date', 'dates')    
    if schema.has_key('modification_date'):
        schema.changeSchemataForField('modification_date', 'dates')    

    # Ownership
    if schema.has_key('creators'):
        schema.changeSchemataForField('creators', 'organizers')
    if schema.has_key('contributors'):
        schema.changeSchemataForField('contributors', 'organizers')
    if schema.has_key('rights'):
        schema.changeSchemataForField('rights', 'organizers')

    # Settings
    if schema.has_key('allowDiscussion'):
        schema.changeSchemataForField('allowDiscussion', 'options')
    if schema.has_key('excludeFromNav'):
        schema.changeSchemataForField('excludeFromNav', 'options')
    if schema.has_key('nextPreviousEnabled'):
        schema.changeSchemataForField('nextPreviousEnabled', 'options')

    schemata.marshall_register(schema)
    return schema

finalizeATCTSchema(
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
