# -*- coding: utf-8 -*-
# Copyright (c) 2006
# Authors:
#   Christian Klinger <cklinger@novareto.de>, goschtl
#   Balazs Ree <ree@greenfinity.hu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

from zope.interface import implements

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

from plone.app.kss.plonekssview import PloneKSSView
from plone.app.kss.interfaces import IPloneKSSView

SKIP_KSSVALIDATION_FIELDTYPES = ('image', 'file')

from zope.deprecation import deprecated

missing_uid_deprecation = \
"This view does not provide a KSS instance UID as required. Falling back to "
"the global context on inline-editing will be removed in Plone 4.0. Please "
"update your templates."

class ValidationView(PloneKSSView):

    implements(IPloneKSSView)
    
    # --
    # Kss methods
    # --

    def kssValidateField(self, fieldname, value, uid=None):
        '''Validate a given field
        '''
        # validate the field, actually

        if uid is not None:
            rc = getToolByName(aq_inner(self.context), 'reference_catalog')
            instance = rc.lookupObject(uid)
        else:
            deprecated(ValidationView, missing_uid_deprecation)
            instance = aq_inner(self.context)

        field = instance.getField(fieldname)
        if field.type in SKIP_KSSVALIDATION_FIELDTYPES:
            return self.render()
        error = field.validate(value, instance, {})
        # XXX
        if isinstance(error, str):
            error = error.decode('utf', 'replace')
        # replace the error on the page
        self.getCommandSet('atvalidation').issueFieldError(fieldname, error)
        return self.render()

    # XXX full form validation
    def kssValidateForm(self, data):
        # Put the form vars on the request, as AT cannot work
        # from data
        self.request.form.update(data)
        # Check for Errors
        #errors = self.context.aq_inner.validate(self.request, errors={}, data=1, metadata=0)
        # this will skip some events but we don't care
        # the predicates should be passed from BaseObject.validate too
        instance = aq_inner(self.context)
        schema = instance.Schema()
        errors = validate(schema, instance, self.request, errors={}, data=1, metadata=0,
                predicates=(lambda field: field.type not in SKIP_KSSVALIDATION_FIELDTYPES, ))
        ksscore = self.getCommandSet('core')
        if errors:
            # give the portal message
            self.getCommandSet('plone').issuePortalMessage(
                _(u'Please correct the indicated errors.'))
            # reset all error fields (as we only know the error ones.)
            ksscore.clearChildNodes(ksscore.getCssSelector('div.field div.fieldErrorBox'))
            # Set error fields
            for fieldname, error in errors.iteritems():
                # XXX
                if isinstance(error, str):
                    error = error.decode('utf', 'replace')
                self.getCommandSet('atvalidation').issueFieldError(fieldname, error)
        else:
            # I just resubmit the form then
            # XXX of course this should be handled from here, save the
            # content and redirect already to the result page - I guess
            # I just don't want to clean up AT form submit procedures
            self.commands.addCommand('plone-submitCurrentForm', ksscore.getSelector('samenode', ''))
        return self.render()


# This is modified from Archetypes.Schema.validate

class _marker:
    ''

def validate(self, instance=None, REQUEST=None,
             errors=None, data=None, metadata=None, predicates=()):
    """Validate the state of the entire object.

    The passed dictionary ``errors`` will be filled with human readable
    error messages as values and the corresponding fields' names as
    keys.

    If a REQUEST object is present, validate the field values in the
    REQUEST.  Otherwise, validate the values currently in the object.
    """
    if REQUEST:
        fieldset = REQUEST.form.get('fieldset', None)
    else:
        fieldset = None
    fields = []

    if fieldset is not None:
        schemata = instance.Schemata()
        fields = [(field.getName(), field)
                  for field in schemata[fieldset].fields() 
                      if not [pred for pred in predicates if not pred(field)]
                 ]

    else:
        if data:
            fields.extend([(field.getName(), field)
                           for field in self.filterFields(isMetadata=0, *predicates)])
        if metadata:
            fields.extend([(field.getName(), field)
                           for field in self.filterFields(isMetadata=1, *predicates)])

    if REQUEST:
        form = REQUEST.form
    else:
        form = None
    for name, field in fields:
        error = 0
        value = None
        widget = field.widget
        if form:
            result = widget.process_form(instance, field, form,
                                         empty_marker=_marker)
        else:
            result = None
        if result is None or result is _marker:
            accessor = field.getEditAccessor(instance) or field.getAccessor(instance)
            if accessor is not None:
                value = accessor()
            else:
                # can't get value to validate -- bail
                continue
        else:
            value = result[0]

        res = field.validate(instance=instance,
                             value=value,
                             errors=errors,
                             REQUEST=REQUEST)
        if res:
            errors[field.getName()] = res
    return errors
