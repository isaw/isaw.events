from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from datetime import datetime as dt
import xmlrpclib, twitter, tinyurl

# TODO Add more error checking for each type of possible error
# Eventually remove all print statements when finally complete
# Add facebook support (please note; that Facebook architecture is crappy)

proxy = xmlrpclib.ServerProxy("http://blogs.nyu.edu/movabletype/mt-xmlrpc.cgi")
username = 'te20'
password = 'jvexa3dk'
blog_id = '1463'
twit = twitter.Api(username='isawnyu', password='r06!2010t')

# Rewrite this later; it's ugly - christopher.warner@nyu.edu
# The orignal iteration published to blog/twitter etc
# This method is changing to encompass all types

def event_publish(post, event):
    workflow_tool = getToolByName(post, 'portal_workflow')
    publish_state = workflow_tool.getInfoFor(post, 'review_state')
    print post.title + '\n' + 'STATE: %s has been changed' % publish_state        

    if (publish_state == 'published'): 
        
        # Post title to twitter
        if post.event_Twitter == True:
            try:
                event_tlink = tinyurl.create_one(post.absolute_url())
            except IOError:
                print "Can't connect to TinyURL service"
                pass
                
            status = twit.PostUpdate("Event - "+ post.title + " " + event_tlink)
            print status.GetId()
            f = post.getField("event_TwitterId")
            f.set(post, status.GetId())
        # TODO: Check post attributes to ensure they exist
       
        if post.event_Reception == True:
            # replace this with a string or annotation on the object so this can be changed
            reception = '*reception to follow; event is free and open to the public'
        else:
            reception = None
            
        if post.event_Sponsor_Name:
            sponsor = "Sponsored by <a href=\"%s\">%s</a>" % (post.event_Sponsor_Url, 
                                                              post.event_Sponsor_Name)
        else:
            sponsor = None
        
        event_date = dt.fromtimestamp(post.event_StartDateTime).strftime('%A, %B %d %Y')
        event_time = dt.fromtimestamp(post.event_StartDateTime).strftime('%I:%M %p')
        url = "<a href=\"%s\">Click here for more information.</a>" % post.absolute_url()
        formatted_post = """Title: <i>%s</i>\n
                          Speaker: %s\nLocation: %s\n
                          <b>Date: %s</b>\n
                          Time: %s\n%s\n%s\n%s""" % (post.title, post.event_Speaker, 
                                                   post.event_Location, 
                                                   event_date, 
                                                   event_time, reception, url, sponsor)
        
        content = {'title': post.title, 
        'description': formatted_post,
        }
        
        # We always publish a new blog entry for track 1
        #publish = True

        if post.event_Blog == True:
            try:
           
            # Res returns the blog id for the new post and then we set event_BlogId 
            # So that we know the id should we have to retract or make the event private

                #res = proxy.metaWeblog.newPost(blog_id, username, password, content, True)
                #f = post.getField("event_BlogId")
                #f.set(post, res)
                print post.event_BlogId
                post.plone_utils.addPortalMessage(_(u'This event has been published on the live website as well as the blog website'))
                # Update category information; there is currently no xml-rpc I can see for this so i'm not sure the below works
                # to be safe i've commented it out
                # cat = proxy.metaWeblog.setPostCategories(res, username, password, )
            except xmlrpclib.Error, x:
                # Change workflow state to retract and notify user a communication error has occured
                print "Error occured %s" % x

        ####################################
        elif (publish_state == 'private'):
            print 'Removing %s from social networks' % post.title
            try:
                if post.event_Twitter == True:
                    twit.DestroyStatus(post.event_TwitterId)

                if post.event_Blog == True:
                    print 'Retracting %s with blogid %s' % (post.title, post.event_BlogId)
                    res = proxy.metaWeblog.deletePost(blog_id, post.event_BlogId, username, password, True)
                    if (res == True):
                        post.plone_utils.addPortalMessage(_(u'This event has been removed from the ISAW weblog'))
                    else:
                        post.plone_utils.addPortalMessage(_(u'There was a problem removing this from http://blogs.nyu.edu please contact an Administrator immediately'))
            except xmlrpclib.Fault, x:
                if (x == True):
                    print "The blog id was already removed!"
                else:    
                    print 'Workflow state not recognized'
