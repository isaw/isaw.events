# -*- coding: utf-8 -*-
# Copyright (c) 2006
# Authors:
#   Jean-Paul Ladage <j.ladage@zestsoftware.nl>, jladage
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

# from zope.component import getMultiAdapter
#from zope.viewlet.interfaces import IViewletManager
from zope.component import queryMultiAdapter

from archetypes.kss.interfaces import IInlineEditingEnabled

from plone.app.kss.plonekssview import PloneKSSView
from plone.app.kss.interfaces import IPloneKSSView
from plone.app.kss.interfaces import IPortalObject

from plone.locking.interfaces import ILockable

from zope.interface import implements
from zope import lifecycleevent, event
from zope.publisher.interfaces.browser import IBrowserView

from Acquisition import aq_inner, aq_base
from Products.Archetypes.event import ObjectEditedEvent
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CMFCore.utils import getToolByName

from zope.deprecation import deprecated

import events
from utils import get_econtext

missing_uid_deprecation = \
"This view does not provide a KSS instance UID as required. Falling back to "
"the global context on inline-editing will be removed in Plone 4.0. Please "
"update your templates."

class FieldsView(PloneKSSView):
    
    implements(IPloneKSSView)

    ## KSS methods
   
    view_field_wrapper = ZopeTwoPageTemplateFile('browser/view_field_wrapper.pt')
    edit_field_wrapper = ZopeTwoPageTemplateFile('browser/edit_field_wrapper.pt')

    def renderViewField(self, fieldname, templateId, macro, uid=None):
        """
        renders the macro coming from the view template
        """

        context = self._getFieldContext(uid)
        template = self.getTemplate(templateId, context)

        viewMacro = template.macros[macro]
        res = self.view_field_wrapper(viewMacro=viewMacro,
                                      context=context,
                                      templateId=templateId,
                                      fieldName=fieldname)
        return res

    def getTemplate(self, templateId, context=None):
        """
        traverse/search template
        """

        if not context:
            context = self.context

        template = context.restrictedTraverse(templateId)
        
        if IBrowserView.providedBy(template):
            view = template
            for attr in ('index', 'template', '__call__'):
                template = getattr(view, attr, None)
                if template is not None and hasattr(template, 'macros'):
                    break
            if template is None:
                raise KeyError("Unable to find template for view %s" % templateId)
        return template


    def renderEditField(self, fieldname, templateId, macro, uid=None):
        """
        renders the edit widget inside the macro coming from the view template
        """

        context = self._getFieldContext(uid)
        template = self.getTemplate(templateId, context)
        containingMacro = template.macros[macro]
        fieldname = fieldname.split('archetypes-fieldname-')[-1]
        field = context.getField(fieldname)
        widget = field.widget
        widgetMacro = widget('edit', context)
        
        res = self.edit_field_wrapper(containingMacro=containingMacro,
                                      widgetMacro=widgetMacro,
                                      field=field, instance=context,
                                      mode='edit',
                                      templateId=templateId)

        return res


    # XXX XXX TODO for 3.0.1: see if we really need edit at all or we can remoce it (ree)

    def replaceField(self, fieldname, templateId, macro, uid=None, target=None, edit=False):
        """
        kss commands to replace the field value by the edit widget

        The edit parameter may be used if we are coming from something else
        than an edit view.
        """
        ksscore = self.getCommandSet('core')
        zopecommands = self.getCommandSet('zope')
        plonecommands = self.getCommandSet('plone')

        instance = self._getFieldContext(uid)        

        if edit:
            locking = ILockable(instance, None)
            if locking:
                if not locking.can_safely_unlock():
                    selector = ksscore.getHtmlIdSelector('plone-lock-status')
                    zopecommands.refreshViewlet(selector,
                                                'plone.abovecontent',
                                                'plone.lockinfo')
                    plonecommands.refreshContentMenu()

                    return self.render()
                else: # were are locking the content
                    locking.lock()

        plonecommands.issuePortalMessage('')

        html = self.renderEditField(fieldname, templateId, macro, uid)
        html = html.strip()

        field_id = target or "parent-fieldname-%s" % fieldname
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(field_id), html)
        ksscore.focus("#%s .firstToFocus" % field_id)

        return self.render()

    def replaceWithView(self, fieldname, templateId, macro, uid=None, target=None, edit=False):
        """
        kss commands to replace the edit widget by the field view
        """

        ksscore = self.getCommandSet('core')
        
        instance = self._getFieldContext(uid)        
        locking = ILockable(instance, None)
        if locking and locking.can_safely_unlock():
            locking.unlock()

        html = self.renderViewField(fieldname, templateId, macro, uid)
        html = html.strip()

        field_id = target or "parent-fieldname-%s" % fieldname
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(field_id), html)

        return self.render()

    def saveField(self, fieldname, value=None, templateId=None, macro=None, uid=None, target=None):
        """
        This method saves the current value to the field. and returns the rendered
        view macro.
        """
        # We receive a dict or nothing in value.
        #
        if value is None:
            value = self.request.form.copy()
        instance = self._getFieldContext(uid)        
        field = instance.getField(fieldname)
        value, kwargs = field.widget.process_form(instance, field, value)
        error = field.validate(value, instance, {}, REQUEST=self.request)
        if not error and field.writeable(instance):
            setField = field.getMutator(instance)
            setField(value, **kwargs)

            # send event that will invoke versioning
            events.fieldsModified(instance, fieldname)

            instance.reindexObject() #XXX: Temp workaround, should be gone in AT 1.5

            descriptor = lifecycleevent.Attributes(IPortalObject, fieldname)
            event.notify(ObjectEditedEvent(instance, descriptor))
            
            return self.replaceWithView(fieldname, templateId, macro, uid, target)
        else:
            if not error:
                # XXX This should not actually happen...
                error = 'Field is not writeable.'
            # Send back the validation error
            self.getCommandSet('atvalidation').issueFieldError(fieldname, error)
            return self.render()

    def _getFieldContext(self, uid):
        if uid is not None:
            rc = getToolByName(aq_inner(self.context), 'reference_catalog')
            return rc.lookupObject(uid)
        else:
            deprecated(FieldsView, missing_uid_deprecation)
            return aq_inner(self.context)
        
class ATDocumentFieldsView(FieldsView):

    def isTableOfContentsEnabled(self):
        getTableContents = getattr(self.context, 'getTableContents', None)
        result = False
        if getTableContents is not None:
            result = getTableContents()
        return result

    def replaceField(self, fieldname, templateId, macro, uid=None, target=None, edit=False):
        if fieldname == "text" and self.isTableOfContentsEnabled():  
            self.getCommandSet('core').setStyle("#document-toc", name="display", value="none")
        FieldsView.replaceField(self, fieldname, templateId, macro, uid=uid, target=target, edit=edit)
        return self.render()

    def replaceWithView(self, fieldname, templateId, macro, uid=None, target=None, edit=False):
        FieldsView.replaceWithView(self, fieldname, templateId, macro, uid=uid, target=target, edit=edit)
        if fieldname == "text" and self.isTableOfContentsEnabled(): 
            self.getCommandSet('core').setStyle("#document-toc", name="display", value="block")
            self.getCommandSet('plone-legacy').createTableOfContents()
        return self.render()
    
    def saveField(self, fieldname, value=None, templateId=None, macro=None, uid=None, target=None):
        FieldsView.saveField(self, fieldname,
                value = value,
                templateId = templateId,
                macro = macro,
                uid = uid,
                target = target,
                )
        if fieldname == "text" and self.isTableOfContentsEnabled(): 
            self.getCommandSet('plone-legacy').createTableOfContents() 
            #manager = getMultiAdapter((self.context, self.request, self),
            #                          IViewletManager,
            #                          name='plone.abovecontentbody')
            #self.getCommandSet('refreshviewlet').refreshViewlet('document-toc',
            #                                                    manager,
            #                                                    'plone.tableofcontents')
        return self.render()


class InlineEditingEnabledView(BrowserView):
    implements(IInlineEditingEnabled)

    def __call__(self):
        """With a nasty although not unusual hack, we reach
        out to the caller template, and examine the global
        tal variable kss_inline_editable. If it is defined,
        and if it is defined to false, we will prohibit
        inline editing everywhere in the template.
        We apply this 'magic' because the signature to getKssClasses
        is already too complex, and it would be undesirable to
        complicate it some more.
        """
        econtext = get_econtext()
        if econtext is None:
            # tests, probably
            return True
        # kss_inline_editable can be set to false in a template, and this
        # will prohibit inline editing in the page
        kss_inline_editable = econtext.vars.get('kss_inline_editable', None)
        # check the setting in site properties
        context = aq_inner(self.context)
        portal_properties = getToolByName(context, 'portal_properties')
        enable_inline_editing = None
        if getattr(aq_base(portal_properties), 'site_properties', None) is not None:
            site_properties = portal_properties.site_properties
            if getattr(aq_base(site_properties), 'enable_inline_editing', None) is not None:
                enable_inline_editing = site_properties.enable_inline_editing
        # If none of these is set, we enable inline editing. The global
        # site_property may be overwritten by the kss_inline_editable variable
        if kss_inline_editable is None:
            inline_editable = enable_inline_editing
        else:
            inline_editable = kss_inline_editable
        if inline_editable is None:
            inline_editable = True
        # In addition we also check suppress_preview.
        # suppress_preview is set by CMFEditions, when version preview is shown
        # This means inline editing should be disabled globally
        suppress_preview = econtext.vars.get('suppress_preview', False)
        return inline_editable and not suppress_preview


# --
# (Non-ajax) browser view for decorating the field
# --

class ATFieldDecoratorView(BrowserView):

    def getKssUIDClass(self):
        """
        This method generates a class-name from the current context UID.
        """
        uid = aq_inner(self.context).UID()
        
        return "kssattr-atuid-%s" % uid

    def _global_kss_inline_editable(self):
        inline_editing = queryMultiAdapter((self.context, self.request),
                                           IInlineEditingEnabled)
        if inline_editing is None:
            return False
        return inline_editing()

    def getKssClasses(self, fieldname, templateId=None, macro=None, target=None):
        context = aq_inner(self.context)
        field = context.getField(fieldname)
        # field can be None when widgets are used without fields
        # check whether field is valid
        if field is not None and field.writeable(context):
            classstring = ' kssattr-atfieldname-%s' % fieldname
            if templateId is not None:
                classstring += ' kssattr-templateId-%s' % templateId
            if macro is not None:
                classstring += ' kssattr-macro-%s' % macro
            if target is not None:
                classstring += ' kssattr-target-%s' % target
            # XXX commented out to avoid macro showing up twice
            # not removed since it might be needed in a use case I forgot about
            # __gotcha
            #else:
            #    classstring += ' kssattr-macro-%s-field-view' % fieldname
        else:
            classstring = ''
        return classstring
    
    def getKssClassesInlineEditable(self, fieldname, templateId, macro=None, target=None):
        classstring = self.getKssClasses(fieldname, templateId, macro, target)
        global_kss_inline_editable = self._global_kss_inline_editable()
        if global_kss_inline_editable and classstring:
            classstring += ' inlineEditable'
        return classstring
