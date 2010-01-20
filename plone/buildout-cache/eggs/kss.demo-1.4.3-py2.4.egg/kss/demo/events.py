
import zope.component
from zope.component.interfaces import (
    IUtilityRegistration,
    IRegistrationEvent,
    )
from interfaces import (
    IKSSDemoResource,
    IKSSSeleniumTestResource,
    IKSSDemoRegistrationEvent,
    IKSSDemoRegistryEvent,
    IKSSDemoRegistry
    )
from zope.interface import implements

class KSSDemoRegistrationEvent(object):
    """Redispatch of registration for demo resource utilities"""
    implements(IKSSDemoRegistrationEvent)

class KSSDemoRegistryEvent(object):
    """Redispatch of registration for demo registry utilities"""
    implements(IKSSDemoRegistryEvent)

@zope.component.adapter(IUtilityRegistration, IRegistrationEvent)
def dispatchRegistration(registration, event):
    """When a demo utility is registered, add it to the registry.
    When a demo utility is registered,  
    event handler registered for the particular component registered,
    the registration and the event.
    """
    component = registration.component
    # Only dispatch registration of the interesting utilities.
    if IKSSDemoResource.providedBy(component) or \
            IKSSSeleniumTestResource.providedBy(component):
        new_event = KSSDemoRegistrationEvent()
        handlers = zope.component.subscribers((component, registration, event, new_event), None)
        for handler in handlers:
            pass # getting them does the work
    if IKSSDemoRegistry.providedBy(component):
        new_event = KSSDemoRegistryEvent()
        handlers = zope.component.subscribers((component, registration, event, new_event), None)
        for handler in handlers:
            pass # getting them does the work
