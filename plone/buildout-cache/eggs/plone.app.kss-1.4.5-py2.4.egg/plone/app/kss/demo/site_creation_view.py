import logging

# XXX Make this package to run with the earlier version
# of kss.demo (<=1.4.0)
# where this module does not exist and this test won't
# be used anyway
try:
    from kss.demo.browser.setupbase import SetupBase
    SetupBase = SetupBase       # to satisfy pyflakes
except:
    # No problem.
    class SetupBase(object):
        pass

from Products.CMFPlone.factory import addPloneSite

logger=logging.getLogger('kss')

class SiteCreationView(SetupBase):

    # objects_tree defines the tree of kss contents used in our tests
    # You can add your objects used in kss tests and generic attributes
    objects_tree = [{'id':'kssfolder', 
                 'portal_type':'Folder',
                 'attrs':{
                          'title':'KssFolder',
                          'description':'Folder for KSS contents',
                         },
                 'transitions': ('publish',),
                 'children': [{'id':'documentitem',
                              'portal_type':'Document',
                              'children':[],
                              'transitions': ('publish',),
                              'attrs':{
                                       'title':'KssDocument',
                                       'text':"""
                                              KSS is a javascript framework that aims to allow Ajax development 
                                              without javascript. It uses stylesheets with CSS-compliant syntax 
                                              to setup behaviours in the client and a set of well-defined commands 
                                              that are marshalled back from the server to manipulate the DOM.
                                              We'll also add an external link also (<a href="http://www.plone.org">
                                              [bug #6343] click here to test if the external link works!</a>).
                                              """,
                                       'description':"""
                                                     KSS is a javascript framework that aims to allow Ajax development 
                                                     without javascript.
                                                     """,
                                      }
                             },
                             {'id':'newsitem',
                              'portal_type':'News Item',
                              'children':[],
                              'attrs':{
                                       'title':'KssNews',
                                       'text':"""
                                              An early spring sprint at a beautiful location on the Italian coast. 
                                              The sprint will focus on topics of interest for Plone 4.0. Potential 
                                              topics include custom membership, extending Plone's use of AJAX, 
                                              content export-import, and much more.
                                              """,
                                       'description':"""
                                                 a    Sorrento sprint
                                                     """,
                                      }
                             },
                            ],
                }]

    users = [ { 'username': 'testuser',
                'password': 'secret',
                'roles': [ 'Member' ]
              },
              { 'username': 'testmanager',
                'password': 'secret',
                'roles': [ 'Manager', 'Member' ]
              } ]

    def addUsers(self, portal):
        for user in self.users:
            portal.acl_users._doAddUser(user['username'], user['password'], user['roles'], [])
 
    def createSite(self, root):
        site_id = 'ksstestportal'
        if hasattr(root, site_id):
            logger.info('Deleting previous site "%s".' % (site_id, ))
            root.manage_delObjects([site_id])
        logger.info('Adding new site "%s".' % (site_id, ))
        addPloneSite(dispatcher=root, id=site_id, extension_ids=())
        return root[site_id]

    def createNodes(self, node, objs_tree, portal):
        """Recursive method that create the tree structure of content types used for kss tests."""
        for item in objs_tree:
            obj_id = item.get('id')
            obj_pt = item.get('portal_type')
            obj_attrs = item.get('attrs')
            obj_children = item.get('children')
            obj_transitions = item.get('transitions', ())
            if hasattr(node, obj_id):
                # if the object exists, we'll delete it
                node.manage_delObjects([obj_id])
            node.invokeFactory(obj_pt, obj_id)
            new_obj = getattr(node, obj_id, None)
            # writing object attributes
            new_obj.update(**obj_attrs)
            # applying the transitions in order
            for transition in obj_transitions:
                portal.portal_workflow.doActionFor(new_obj, transition)
          
            # recursive call for creating other nodes
            self.createNodes(new_obj, obj_children, portal)

    def run(self, zoperoot):
        """This method invokes the recursive method createNodes which creates the tree structure of
        objects used by.
        """
        site = self.createSite(zoperoot)
        
        self.addUsers(site)
        
        self.createNodes(site, self.objects_tree, site)

        status_message='Selenium Test Site has been created'
        logger.info(status_message)

        # The method must return a tag with id "ok", containing the text "OK".
        # to signal success to the testsuite. 
        return '<html><body><div id="OK">OK</div><div>Site creation succesful.</div></body></html>'
