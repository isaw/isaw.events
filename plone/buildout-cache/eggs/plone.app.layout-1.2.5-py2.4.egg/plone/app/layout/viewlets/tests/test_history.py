import unittest
from plone.app.layout.viewlets.tests.base import ViewletsTestCase
from plone.app.layout.viewlets.content import WorkflowHistoryViewlet
from plone.app.layout.viewlets.content import ContentHistoryViewlet
from DateTime import DateTime

class TestWorkflowHistoryViewlet(ViewletsTestCase):
    """
    Test the workflow history viewlet
    """
    def afterSetUp(self):
        # add document, perform transition, set history for non-existent
        # member and also None (anonymous)
        self.folder.invokeFactory('Document', 'd1')

    def addMember(self, username, roles=('Member',)):
        self.portal.portal_membership.addMember(username, 'secret', roles, [])

    def delMember(self, username):
        self.portal.portal_membership.deleteMembers([username])

    def test_emptyHistory(self):
        request = self.app.REQUEST
        context = getattr(self.folder, 'd1')
        viewlet = WorkflowHistoryViewlet(context, request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.workflowHistory(), [])

    def test_transitionHistory(self):
        wf_tool = self.portal.portal_workflow
        request = self.app.REQUEST
        context = getattr(self.folder, 'd1')
        self.loginAsPortalOwner()
        wf_tool.doActionFor(context, 'publish')

        viewlet = WorkflowHistoryViewlet(context, request, None, None)
        viewlet.update()

        history = viewlet.workflowHistory()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['action'], 'publish')

        # add a temporary user to perform a transition
        self.addMember('tempuser', roles=('Member', 'Manager'))
        self.login('tempuser')
        wf_tool.doActionFor(context, action='retract', actor=None)
        self.logout()

        self.loginAsPortalOwner()

        # remove the user
        self.delMember('tempuser')

        # if the user that performed the transition no longer exists, the link
        # shouldn't be included.
        viewlet = WorkflowHistoryViewlet(context, request, None, None)
        viewlet.update()
        history = viewlet.workflowHistory()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['actor_home'], '')


class TestContentHistoryViewlet(ViewletsTestCase):
    """
    Test the workflow history viewlet
    """
    def afterSetUp(self):
        # add document, perform transition, set history for non-existent
        # member and also None (anonymous)
        self.folder.invokeFactory('Document', 'd1')

    def test_emptyHistory(self):
        request = self.app.REQUEST
        context = getattr(self.folder, 'd1')
        viewlet = ContentHistoryViewlet(context, request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.revisionHistory(), [])

    def test_revisionHistory(self):
        repo_tool = self.portal.portal_repository
        request = self.app.REQUEST
        context = getattr(self.folder, 'd1')
        self.loginAsPortalOwner()
        repo_tool.save(context, comment='Initial Revision')

        viewlet = ContentHistoryViewlet(context, request, None, None)
        viewlet.update()

        history = viewlet.revisionHistory()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['comments'], 'Initial Revision')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWorkflowHistoryViewlet))
    suite.addTest(unittest.makeSuite(TestContentHistoryViewlet))
    return suite
