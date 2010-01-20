## Script (Python) "revertversion"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=version_id
##title=Revert version
##

from Products.CMFEditions import CMFEditionsMessageFactory as _
from Products.CMFEditions.interfaces.IModifier import FileTooLargeToVersionError

RESPONSE = context.REQUEST.RESPONSE
putils = container.plone_utils
pr = container.portal_repository
pr.revert(context, version_id)
view_url = '%s/%s' % (context.absolute_url(),
                      context.getTypeInfo().getActionInfo('object/view')['url']
                     )

title = context.title_or_id()
if not isinstance(title, unicode):
    title = unicode(title, 'utf-8', 'ignore')

msg = _(u'${title} has been reverted to version ${version}.',
        mapping={'title' : context.title_or_id(), 'version' : version_id})

if pr.supportsPolicy(context, 'version_on_revert'):
    try:
        pr.save(obj=context, comment=_(u"Reverted to version ${version}",
                                       mapping={'version': version_id}))
    except FileTooLargeToVersionError:
        putils.addPortalMessage(
  _("The most current version of the file could not be saved before reverting "
    "because the file is too large."),
       type="warn"
       )

context.plone_utils.addPortalMessage(msg)
return RESPONSE.redirect(view_url)
