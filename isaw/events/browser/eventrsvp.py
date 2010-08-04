# coding=utf-8
from zope import interface, schema
from zope.formlib import form
from Products.Five.formlib import formbase

from zope.schema import ValidationError
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from Acquisition import aq_parent, aq_inner

class InvalidEmailAddress(ValidationError):
    "Invalid email address"

# email validation
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from isaw.events import eventsMessageFactory as _

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

class IEventRsvpSchema(interface.Interface):
    name = schema.TextLine(
        title=u'Name',
        description=u'Please provide your full name',
        required=True,
        readonly=False,
        )

    email = schema.TextLine(
        title=u'Email',
        description=u'Please enter a valid email address',
        required=True,
        readonly=False,
        constraint=validateaddress,
        )


class EventRsvp(formbase.PageForm):
    form_fields = form.FormFields(IEventRsvpSchema)
    label = _(u'Please fill out our RSVP form')
    description = _(u' Répondez s\'il vous plaît ')

    @form.action('Submit')
    def actionSubmit(self, action, data):
        # Get event parent url
        #
        event_folder_obj = aq_inner(self.context)
        parent_url = event_folder_obj.absolute_url()
        self.request.response.redirect(parent_url)
        pass

