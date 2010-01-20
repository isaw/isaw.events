
from zope.component import adapter
from kss.core.interfaces import IKSSView
from interfaces import IVersionedFieldModifiedEvent

from Products.CMFPlone.utils import base_hasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFEditions.interfaces.IArchivist import ArchivistUnregisteredError
from Products.CMFEditions.interfaces.IModifier import FileTooLargeToVersionError

# --
# As a temporary solution, we start a new version after a field is 
# instant edited. This is done similarly as on the formcontroller hook. 
# This hook, Products/CMFEditions/skins/update_version_on_edit.py, is
# set up from  Products/CMFEditions/VersionPolicies.py.
# --

@adapter(None, IKSSView, IVersionedFieldModifiedEvent)
def versionObjectBecauseFieldChanged(obj, view, event):
    # XXX I believe we don't need to check if CMFEditions has actually
    # set the hook or not?

    pr = getToolByName(view.context, 'portal_repository')
    isVersionable = pr.isVersionable(obj)
    
    changed = False
    if not base_hasattr(obj, 'version_id'):
        changed = True
    else:
        try:
            changed = not pr.isUpToDate(obj, obj.version_id)
        except ArchivistUnregisteredError:
            # XXX: The object is not actually registered, but a
            # version is set, perhaps it was imported, or versioning
            # info was inappropriately destroyed
            changed = True

    fieldnames = event.fieldnames
    txtfieldnames ='"%s"' % ('", "'.join(fieldnames), )
    # XXX I am not sure we actually want to translate _here_, but 
    # at the moment this seems to be the best policy.
    comment_msg = _('Instant edited field(s) ${fields}' , 
                    mapping=dict(fields=txtfieldnames))
    # XXX unicode is not possible here?
    comment = view.context.translate(comment_msg)
    comment = comment.encode('utf')

    if changed and comment is not None and \
           pr.supportsPolicy(obj, 'at_edit_autoversion') and isVersionable:
        try:
            pr.save(obj=obj, comment=comment)
        except FileTooLargeToVersionError:
            commands = view.getCommandSet('plone')
            commands.issuePortalMessage(
                _("Changes Saved. Versioning for this file has been disabled "
                  "because it is too large."),
                msgtype="warn")
