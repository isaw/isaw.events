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
    atapi.TextField(
    name='event_ShortDescription',
    widget=atapi.TextAreaWidget(
        label=u'Event Short Description',
        label_msgid='ISAW_Event_shortdescription',
        il8n_domain='ISAW_Event',
        size=50,
        ),

    required=False,
    searchable=True),

    atapi.DateTimeField(
    name='event_StartDateTime',
    widget=atapi.CalendarWidget(
        label=u'Event Start Date and Time',
        label_msgid='ISAW_Event_StartDateTime',
        il8n_domain='ISAW_Event',
        show_hm=True,
        format='%A, %B %d %Y'
        ),

    required=True,
    searchable=True),

    atapi.DateTimeField(
    name='event_EndDateTime',
    widget=atapi.CalendarWidget(
        label=u'Event End Date and Time',
        label_msgid='ISAW_Event_EndDateTime',
        il8n_domain='ISAW_Event',
        ),

    required=True,
    searchable=True),

    atapi.StringField(
    name='event_Speaker',
    widget=atapi.StringWidget(
        label=u'Event Speaker',
        label_msgid='ISAW_Event_Speaker',
        il8n_domain='ISAW_Event',
        maxlength=255,
        size=50,
        ),
        
    required=False,
    searchable=True),
    
    atapi.StringField(
    name='event_Location',
    # I don't like the dependence on this widget
    # will think about either extending DynamicSelectWidget
    # or releasing a new version of it
    widget=atapi.StringWidget(
        label=u'Event Location',
        label_msgid='ISAW_Event_location',
        il8n_domain='ISAW_Event',
        maxlength=255,
        size=50,
        ),
        
#    vocabulary=DisplayList((
#    ('Library', u'Oak Library'),
#    ('Lecture', u'Lecture Hall'),
#    ('Seminar', u'Seminar Room'),
#    ('Gallery 1', u'Gallery 1'),
#    ('Gallery 2', u'Gallery 2'),
#    ('Lunch', u'Lunch Room (basement)'),
#    ('Garden', u'Garden')
#    )),
    
    required=False,
    searchable=True),

    atapi.LinesField(
    name='event_Type',
    vocabulary = DisplayList((
        ('lecture', 'An event lecture'),
        ('conference', 'An event conference'),
        ('film', 'An event where a film will be shown'),
        ('concert', 'An event where a concert will be held'),
        )),
        
        widget=atapi.PicklistWidget(
        label=u'What type of Event is this?',
        label_msgid='ISAW_Event_Type',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    atapi.BooleanField(
    name='event_Sponsor',
    schemata='Sponsor',
    widget=atapi.BooleanWidget(
        label=u'Is this event sponsored?',
        label_msgid='ISAW_Event_Sponsor',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    atapi.StringField(
    name='event_Sponsor_Name',
    schemata='Sponsor',
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
    name='event_Sponsor_Url',
    schemata='Sponsor',
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
    name='event_Sponsor_Logo',
    schemata='Sponsor',
    widget=atapi.ImageWidget(
        label=u'Event Sponsor Logo',
        label_msgid='ISAW_Event_Sponsor_Logo',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    atapi.BooleanField(
    name='event_Reception',
    widget=atapi.BooleanWidget(
        label=u'Will there be a reception?',
        label_msgid='ISAW_Event_reception',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    atapi.BooleanField(
    name='event_VRS',
    widget=atapi.BooleanWidget(
        label=u'Is this event being held by a Visiting Research Scholar?',
        label_msgid='ISAW_Event_vrs',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    atapi.BooleanField(
    name='event_exhibition',
    widget=atapi.BooleanWidget(
        label=u'Is this an exhibition event?',
        label_msgid='ISAW_Event_exhibit',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    atapi.BooleanField(
    name='event_Rsvp',
    widget=atapi.BooleanWidget(
        label=u'Does one need to RSVP for this event?',
        label_msgid='ISAW_Event_rsvp',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    # Please use Products.ImageEditor
    # It will be added to the project buildout
    # This is here in the event (no-pun intended) that you're using a standalone binary instance

    # The behavior we would really want is to allow image editor to modify events content type
    # I can make products.imageeditor do this; it would mean keeping our own branch with the 
    # events module
    atapi.ImageField(
    name='event_Image',
    widget=atapi.ImageWidget(
        label=u'Optional Image associated with the Event',
        label_msgid='ISAW_Event_image',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=False),
    

#    atapi.TextField(
#    name='event_Leadin',
#    widget=atapi.TextAreaWidget(
#        label=u'Event Leadin',
#        label_msgid='ISAW_Event_leadin',
#        il8n_domain='ISAW_Event',
#        size=50,
#        ),
#        
#    required=False,
#   searchable=True),

    
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
    schemata='Social',
    name='event_Twitter',
    widget=atapi.BooleanWidget(
        label=u'Apply this event to Twitter?',
        label_msgid='ISAW_Event_twitter',
        il8n_domain='ISAW_Event',
        ),
        
    required=False,
    searchable=True),
    
    atapi.BooleanField(
    schemata='Social',
    name='event_Facebook',
    widget=atapi.BooleanWidget(
        label=u'Apply this event to Facebook?',
        label_msgid='ISAW_Event_facebook',
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
    content_icon = 'images/appointment-new.png'

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(events, PROJECTNAME)
