#########################################
# zopectl run script to create a Plone site
# and create some root plone-specific content.
#
# $LastChangedDate: 2008-08-06 09:08:31 -0700 (Wed, 06 Aug 2008) $ $LastChangedRevision: 22028 $
#
# insertStandardTemplate derived from Jarn's "Bones" -- Thanks!

import sys, os

import transaction

from AccessControl.SecurityManagement import \
    newSecurityManager, noSecurityManager

from Testing.makerequest import makerequest

from Products.PageTemplates.PageTemplateFile import PageTemplateFile


def insertStandardContent(app, templatedir):

    if os.path.exists(templatedir):
        for fn in os.listdir(templatedir):
            base, ext = os.path.splitext(fn)

            if fn.startswith('.'):
                continue
            elif ext in ('.pt', '.zpt'):
                if hasattr(app, base):
                    app._delObject(base, suppress_events=True)
                ob = PageTemplateFile(fn, templatedir, __name__=base)
                app.manage_addProduct['PageTemplates'].manage_addPageTemplate(
                    id=base, title='', text=open(ob.filename))
            elif ext in ('.ico', '.gif', '.png', '.jpg'):
                if hasattr(app, fn):
                    app._delObject(fn, suppress_events=True)
                app.manage_addProduct['OFSP'].manage_addImage(
                    id=fn, title='', file=open(os.path.join(templatedir, fn)))

        app._plone_standard_content=True
        transaction.get().note("Installed Plone standard content")
        print "Installed Plone standard content"
        transaction.commit()

def createSite(app):

    if "Plone" in app.objectIds():
        print "A Plone site already exists"
        return 0 # not an error

    app = makerequest(app)

    acl_users = app.acl_users
    user = acl_users.getUser("admin")
    if user:
        user = user.__of__(acl_users)
        newSecurityManager(None, user)
    else:
        print "Retrieving admin user failed"
        return 1

    app.manage_addProduct['CMFPlone'].addPloneSite("Plone", title='Portal')

    transaction.get().note("Created a default Plone site")
    transaction.commit()
    noSecurityManager()
    
    print "Finished adding Plone site"
    return 0


if len(sys.argv) == 2:
    insertStandardContent(app, sys.argv[1])

sys.exit( createSite(app) )

