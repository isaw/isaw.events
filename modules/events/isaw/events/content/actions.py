from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from datetime import datetime as dt
import time
import xmlrpclib

# TODO Add more error checking for each type of possible error
# Eventually remove all print statements when finally complete
# Need to add REMOVE post if an event is removed

proxy = xmlrpclib.ServerProxy("http://blogs.nyu.edu/movabletype/mt-xmlrpc.cgi")
username = 'te20'
password = 'jvexa3dk'
blog_id = '1463'

def event_blogpublish(post, event):
    workflow_tool = getToolByName(post, 'portal_workflow')
    publish_state = workflow_tool.getInfoFor(post, 'review_state')

    if (publish_state == 'published'): 
        print post.title + '\n' + 'STATE: %s has been changed' % publish_state        
        # Creation of blog formatting is as follows
        #
        # eg:
        # Visiting Research Scholar Lecture
        # Title: Temple Treasury Records and Local Politics in Ur III Mesopotamia
        # Speaker: Xiaon Ouyang
        # Location: 2nd Floor Lecture Room
        # Date: Tuesday, Febuary 16 2010
        # Time: 6:00 p.m.
        # *reception to follow; event is free and open to the public
        # <a href=URL>Click here for more information</a>
        
        
        # TODO: Check post attributes to ensure they exist
        if post.event_Reception == 1:
            # replace this with a string or annotation on the object so this can be changed
            reception = '*reception to follow; event is free and open to the public'
        else:
            reception = None
        
        event_date = dt.fromtimestamp(post.event_StartDateTime).strftime('%A, %B %d %Y')
        event_time = dt.fromtimestamp(post.event_StartDateTime).strftime('%I:%M %p')
        # replace "Click here for more information with a string or annotation on the object so this can be changed"    
        url = "<a href=\"%s\">Click here for more information.</a>" % post.absolute_url()
        formatted_post = "Title: %s\nSpeaker: %s\nLocation: %s\n<b>Date: %s</b>\nTime: %s\n%s\n%s" % (post.title, post.event_Speaker, 
                                                                                            post.event_Location, 
                                                                                            event_date, 
                                                                                            event_time, reception, url)
        
        
        content = {'title': post.title, 
        'description': formatted_post,
        }
        
        # We always publish a new blog entry for track 1
        publish = 1
        
        try:
            res = proxy.metaWeblog.newPost(blog_id, username, password, content, 1)
            post.plone_utils.addPortalMessage(_(u'This event has been published on the live website as well as the blog website'))
            # Update category information; there is currently no xml-rpc I can see for this so i'm not sure the below works
            # to be safe i've commented it out
            # cat = proxy.metaWeblog.setPostCategories(res, username, password, )
        except xmlrpclib.Error, x:
            print "Error occured %s" % x
    else:
        print 'doing nothing'