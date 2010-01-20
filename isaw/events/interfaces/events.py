from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from isaw.events import eventsMessageFactory as _

class IEvents(Interface):
    """ISAW Events Module"""
    
    # -*- schema definition goes here -*-
