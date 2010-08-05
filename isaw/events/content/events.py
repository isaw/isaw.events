"""Definition of the events content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.Archetypes.public import DisplayList

#from Products.DynamicSelect.DynamicSelectWidget import DynamicSelectWidget


from isaw.events import eventsMessageFactory as _
from isaw.events.interfaces import Ievents
from isaw.events.config import PROJECTNAME

"""EVENTS SAMPLE DATA

Date - datetime
Time - datetime
Speaker - string/user profile
Location - string
Reception - bool (reception to follow?)
Leadin - string (short description)
Short description - text
Long description - text
Sample pulled from http://www.nyu.edu/isaw/events/fernandez-2010-01-19.htm
Visiting Research Scholar Lecture
Living in the Heights: Hilltop settlement and the changing landscape of northern Hispania during late antiquity.

Speaker: Damian Fernandez
Location: 2nd Floor Lecture Room
Date: Tuesday, January 19 2010
Time: 6:00 p.m.
*reception to follow

Bookmark and Share

Hilltop settlement was one of the most prominent characteristics in the landscape of the northern
Iberian Peninsula until the Roman conquest. With the establishment of Roman rule in the decades
around the turn of the era, several of the pre-Roman hilltop forts were abandoned in favor of a
developed network of lowland cities that became the backbone of the regional settlement hierarchy.
This process was somewhat reversed after the late-third century CE, when archaeologists have dated
the beginning of the occupation of hilltops (and, sometimes, the re-occupation of Iron Age sites).
The movement towards the highlands has traditionally been interpreted either as reemergence of
indigenous social structures that had survived the Roman conquest or as the result of the
insecurity provoked by the presence of barbarian armies in the third and fifth centuries.

In the last two decades, piecemeal archaeological research in the northern Iberian Peninsula has
begun to provide us with new information about these sites. Their material culture and the more
accurate chronology indicate that traditional interpretations about the phenomenon of hilltop
occupation are no longer valid. After reviewing some paradigmatic sites, this lecture will offer an
alternative model to understanding the change in settlement patterns. It will be argued that
occupation of hilltops must be understood in the context of the administrative reforms of the late
Roman Empire and the economic changes that occurred in northern Iberia during late antiquity."""

eventsSchema = folder.ATFolderSchema.copy() + atapi.Schema((

# -*- Events Schema -*- #
    atapi.ImageField(
    name='event_Image',
    widget=atapi.ImageWidget(
        label=u'Event Image',
        description=_(u'event_image', default=u'Optional image associated with the event.'),
        label_msgid='ISAW_Event_image',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=False),
    


    atapi.TextField(
    name='event_Abstract',
    widget=atapi.TextAreaWidget(
        label=u'Event Abstract',
        description=_(u'event_abstract', default=u'A short description of the event.'),
        label_msgid='ISAW_Event_abstract',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=True),

    atapi.StringField(
    name='event_Speaker',
    widget=atapi.StringWidget(
        description=_(u'event_Speaker', default=u'The person speaking or holding the event.'),
        label=u'Event Speaker',
        label_msgid='ISAW_Event_Speaker',
        il8n_domain='ISAW_Event',
        maxlength=255,
        size=50,
        ),
        
    required=False,
    searchable=True),

    # Organizers/Contributors
    
#    atapi.StringField(
#    name='event_Location',
    # I don't like the dependence on this widget
    # will think about either extending DynamicSelectWidget
    # or releasing a new version of it
#    widget=atapi.StringWidget(
#        label=u'Event Location',
#        label_msgid='ISAW_Event_location',
#        il8n_domain='ISAW_Event',
#        maxlength=255,
#        size=50,
#        ),
        
#    vocabulary=DisplayList((
#    ('Library', u'Oak Library'),
#    ('Lecture', u'Lecture Hall'),
#    ('Seminar', u'Seminar Room'),
#    ('Gallery 1', u'Gallery 1'),
#    ('Gallery 2', u'Gallery 2'),
#    ('Lunch', u'Lunch Room (basement)'),
#    ('Garden', u'Garden')
#    )),
    
#    required=False,
#    searchable=True),

    atapi.DateTimeField(
    name='event_StartDateTime',
    widget=atapi.CalendarWidget(
        description=_(u'event_startdatetime', default=u'The date and/or time when the event starts.'),
        label=u'Event Start Date and Time',
        label_msgid='ISAW_Event_StartDateTime',
        il8n_domain='ISAW_Event',
        show_hm=True,
        format='%A, %B %d %Y %X %p %z'
        ),

    required=True,
    searchable=True),

    atapi.DateTimeField(
    name='event_EndDateTime',
    widget=atapi.CalendarWidget(
        description=_(u'event_enddatetime', default=u'The date and/or time when the event ends.'),
        label=u'Event End Date and Time',
        label_msgid='ISAW_Event_EndDateTime',
        il8n_domain='ISAW_Event',
        show_hm=True,
        format='%A, %B %d %Y %X %p %z'
        ),

    required=True,
    searchable=True),


#    atapi.LinesField(
#    name='event_Type',
#    vocabulary = DisplayList((
#        ('lecture', 'An event lecture'),
#        ('conference', 'An event conference'),
#        ('film', 'An event where a film will be shown'),
#        ('concert', 'An event where a concert will be held'),
#        )),
#        
#        widget=atapi.PicklistWidget(
#        label=u'What type of Event is this?',
#        label_msgid='ISAW_Event_Type',
#        il8n_domain='ISAW_Event',
#        ),
#        
#    required=False,
#    searchable=True),
    
    atapi.BooleanField(
    name='event_Private',
    schemata='options',
    widget=atapi.BooleanWidget(
        description=_(u'event_private', default=u'If selected, only ISAW faculty/admin/staff will be able to view this event.'),
        label=u'Private Event',
        label_msgid='ISAW_Event_Private',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=False),

    atapi.BooleanField(
    name='event_Reception',
    schemata='options',
    widget=atapi.BooleanWidget(
        description=_(u'event_reception', default=u'If selected, the event will have a reception following.'),
        label=u'Reception',
        label_msgid='ISAW_Event_reception',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=False),
    
    atapi.BooleanField(
    name='event_Rsvp',
    schemata='options',
    widget=atapi.BooleanWidget(
        label=u'Does one need to RSVP for this event?',
        description=_(u'event_rsvp', default=u'If selected, one will need to RSVP for this event.'),
        label_msgid='ISAW_Event_rsvp',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    # After about 10 minutes deliberation
    # instead of making this an Annotation i've added it to the object itself
    # the reason being is all data should be stored/managed in the object if it's small enough
    
    atapi.IntegerField(
    name='event_BlogId',
    widget=atapi.IntegerWidget(
        label=u'Event Blog id',
        label_msgid='ISAW_Event_blogid',
        il8n_domain='ISAW_Event',
        size=10,
        visible={'view': 'visible', 
                'edit': 'hidden'},
        ),
    
    # Does isMetadata work anymore?
    isMetadata=True,
    required=False),
    

    atapi.BooleanField(
    schemata='options',
    name='event_Twitter',
    widget=atapi.BooleanWidget(
        description=_(u'event_twitter', default=u'If selected, this event will appear on Twitter @ http://twitter.com/isawnyu'),
        label=u'Post this event on Twitter?',
        label_msgid='ISAW_Event_twitter',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    atapi.BooleanField(
    schemata='options',
    name='event_Facebook',
    widget=atapi.BooleanWidget(
        description=_(u'event_facebook', default=u'If selected, this event will appear on Facebook.'),
        label=u'Post this event on Facebook?',
        label_msgid='ISAW_Event_facebook',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=True),

    atapi.BooleanField(
    schemata='options',
    name='event_Blog',
    widget=atapi.BooleanWidget(
        description=_(u'event_blog', default=u'If selected, this event will appear on the news blog.'),
        label=u'Post this event on the news blog?',
        label_msgid='ISAW_Event_blog',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=True),

    atapi.BooleanField(
    schemata='options',
    name='event_Invite',
    widget=atapi.BooleanWidget(
        description=_(u'event_invite', default=u'If selected, this event will be invitation only.'),
        label=u'Invitation only',
        label_msgid='ISAW_Event_isaw',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=True),

    atapi.IntegerField(
    name='event_TwitterId',
    widget=atapi.IntegerWidget(
        label=u'Event Twitter id',
        label_msgid='ISAW_Event_twitterid',
        il8n_domain='ISAW_Event',
        size=10,
        visible={'view': 'visible', 
                'edit': 'hidden'},
        ),
    
    # Does isMetadata work anymore?
    isMetadata=True,
    required=False),
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

eventsSchema['title'].storage = atapi.AnnotationStorage()
eventsSchema['description'].storage = atapi.AnnotationStorage()

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

    schema.moveField('event_Image', after='title')

    # Categorization
    if schema.has_key('subject'):
        schema.changeSchemataForField('subject', 'tags')
    if schema.has_key('relatedItems'):
        schema.changeSchemataForField('relatedItems', 'tags')
    if schema.has_key('location'):
        schema.changeSchemataForField('location', 'default')
        schema.moveField('location', after='event_Speaker')
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
    eventsSchema,
    folderish=True,
    moveDiscussion=False
)

class events(folder.ATFolder):
    """Isaw Events Module"""
    implements(Ievents)

    meta_type = "General"
    schema = eventsSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(events, PROJECTNAME)
