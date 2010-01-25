"""Definition of the events content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

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

Speaker: Damián Fernández
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
The ‘movement towards the highlands’ has traditionally been interpreted either as reemergence of
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

    atapi.DateTimeField(
    name='event_StartDateTime',
    widget=atapi.CalendarWidget(
        label=u'Event Start Date and Time',
        label_msgid='ISAW_Event_StartDateTime',
        il8n_domain='ISAW_Event',
        ),

    required=False,
    searchable=True),

    atapi.DateTimeField(
    name='event_EndDateTime',
    widget=atapi.CalendarWidget(
        label=u'Event End Date and Time',
        label_msgid='ISAW_Event_EndDateTime',
        il8n_domain='ISAW_Event',
        ),

    required=False,
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
    widget=atapi.StringWidget(
        label=u'Event Location',
        label_msgid='ISAW_Event_location',
        il8n_domain='ISAW_Event',
        maxlength=255,
        size=50,
        ),
        
    required=False,
    searchable=True),

    atapi.BooleanField(
    name='event_Reception',
    widget=atapi.BooleanWidget(
        label=u'Event Reception',
        label_msgid='ISAW_Event_reception',
        il8n_domain='ISAW_Event',
        size=50,
        ),
        
    required=False,
    searchable=True),
    
    atapi.TextField(
    name='event_Leadin',
    widget=atapi.TextAreaWidget(
        label=u'Event Leadin',
        label_msgid='ISAW_Event_leadin',
        il8n_domain='ISAW_Event',
        size=50,
        ),
        
    required=False,
    searchable=True),
    
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
    toolicon = 'images/appointment-new.png'

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(events, PROJECTNAME)
