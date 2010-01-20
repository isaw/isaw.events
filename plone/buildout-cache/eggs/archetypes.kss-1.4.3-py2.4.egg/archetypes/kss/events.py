
from zope.component.interfaces import ObjectEvent
from interfaces import IVersionedFieldModifiedEvent
from zope.interface import implements
from zope.event import notify

class VersionedFieldModifiedEvent(ObjectEvent):
    """A field has been modified, versioning needed"""

    implements(IVersionedFieldModifiedEvent)

    def __init__(self, ob, *fieldnames) :
        """
        Init with a list of (AT) field names.

        >>> from zope.interface import Interface, implements
        >>> class Sample(object):
        ...     implements(Interface)

        >>> obj = Sample()
        >>> obj.field = 42
        >>> notify(VersionedFieldModifiedEvent(obj, "field"))

        """
        super(VersionedFieldModifiedEvent, self).__init__(ob)
        self.fieldnames = fieldnames

def fieldsModified(ob, *fieldnames):
    notify(VersionedFieldModifiedEvent(ob, *fieldnames))


