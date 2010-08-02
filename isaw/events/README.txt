Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True


-*- extra stuff goes here -*-
The Performance content type
===============================

In this section we are tesing the Performance content type by performing
basic operations like adding, updadating and deleting Performance content
items.

Adding a new Performance content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Performance' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Performance').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Performance' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Performance Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Performance' content item to the portal.

Updating an existing Performance content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Performance Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Performance Sample' in browser.contents
    True

Removing a/an Performance content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Performance
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Performance Sample' in browser.contents
    True

Now we are going to delete the 'New Performance Sample' object. First we
go to the contents tab and select the 'New Performance Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Performance Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Performance
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Performance Sample' in browser.contents
    False

Adding a new Performance content item as contributor
------------------------------------------------

Not only site managers are allowed to add Performance content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Performance' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Performance').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Performance' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Performance Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Performance content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Exhibition content type
===============================

In this section we are tesing the Exhibition content type by performing
basic operations like adding, updadating and deleting Exhibition content
items.

Adding a new Exhibition content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Exhibition' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Exhibition').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Exhibition' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Exhibition Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Exhibition' content item to the portal.

Updating an existing Exhibition content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Exhibition Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Exhibition Sample' in browser.contents
    True

Removing a/an Exhibition content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Exhibition
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Exhibition Sample' in browser.contents
    True

Now we are going to delete the 'New Exhibition Sample' object. First we
go to the contents tab and select the 'New Exhibition Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Exhibition Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Exhibition
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Exhibition Sample' in browser.contents
    False

Adding a new Exhibition content item as contributor
------------------------------------------------

Not only site managers are allowed to add Exhibition content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Exhibition' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Exhibition').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Exhibition' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Exhibition Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Exhibition content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Sponsored content type
===============================

In this section we are tesing the Sponsored content type by performing
basic operations like adding, updadating and deleting Sponsored content
items.

Adding a new Sponsored content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Sponsored' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Sponsored').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Sponsored' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Sponsored Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Sponsored' content item to the portal.

Updating an existing Sponsored content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Sponsored Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Sponsored Sample' in browser.contents
    True

Removing a/an Sponsored content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Sponsored
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Sponsored Sample' in browser.contents
    True

Now we are going to delete the 'New Sponsored Sample' object. First we
go to the contents tab and select the 'New Sponsored Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Sponsored Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Sponsored
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Sponsored Sample' in browser.contents
    False

Adding a new Sponsored content item as contributor
------------------------------------------------

Not only site managers are allowed to add Sponsored content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Sponsored' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Sponsored').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Sponsored' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Sponsored Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Sponsored content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Conference content type
===============================

In this section we are tesing the Conference content type by performing
basic operations like adding, updadating and deleting Conference content
items.

Adding a new Conference content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Conference' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Conference').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Conference' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Conference Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Conference' content item to the portal.

Updating an existing Conference content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Conference Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Conference Sample' in browser.contents
    True

Removing a/an Conference content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Conference
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Conference Sample' in browser.contents
    True

Now we are going to delete the 'New Conference Sample' object. First we
go to the contents tab and select the 'New Conference Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Conference Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Conference
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Conference Sample' in browser.contents
    False

Adding a new Conference content item as contributor
------------------------------------------------

Not only site managers are allowed to add Conference content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Conference' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Conference').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Conference' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Conference Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Conference content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Seminar content type
===============================

In this section we are tesing the Seminar content type by performing
basic operations like adding, updadating and deleting Seminar content
items.

Adding a new Seminar content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Seminar' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Seminar').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Seminar' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Seminar Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Seminar' content item to the portal.

Updating an existing Seminar content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Seminar Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Seminar Sample' in browser.contents
    True

Removing a/an Seminar content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Seminar
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Seminar Sample' in browser.contents
    True

Now we are going to delete the 'New Seminar Sample' object. First we
go to the contents tab and select the 'New Seminar Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Seminar Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Seminar
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Seminar Sample' in browser.contents
    False

Adding a new Seminar content item as contributor
------------------------------------------------

Not only site managers are allowed to add Seminar content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Seminar' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Seminar').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Seminar' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Seminar Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Seminar content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Lecture content type
===============================

In this section we are tesing the Lecture content type by performing
basic operations like adding, updadating and deleting Lecture content
items.

Adding a new Lecture content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Lecture' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Lecture').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Lecture' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Lecture Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Lecture' content item to the portal.

Updating an existing Lecture content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Lecture Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Lecture Sample' in browser.contents
    True

Removing a/an Lecture content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Lecture
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Lecture Sample' in browser.contents
    True

Now we are going to delete the 'New Lecture Sample' object. First we
go to the contents tab and select the 'New Lecture Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Lecture Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Lecture
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Lecture Sample' in browser.contents
    False

Adding a new Lecture content item as contributor
------------------------------------------------

Not only site managers are allowed to add Lecture content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Lecture' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Lecture').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Lecture' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Lecture Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Lecture content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The events content type
===============================

In this section we are tesing the events content type by performing
basic operations like adding, updadating and deleting events content
items.

Adding a new events content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'events' and click the 'Add' button to get to the add form.

    >>> browser.getControl('events').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'events' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'events Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'events' content item to the portal.

Updating an existing events content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New events Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New events Sample' in browser.contents
    True

Removing a/an events content item
--------------------------------

If we go to the home page, we can see a tab with the 'New events
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New events Sample' in browser.contents
    True

Now we are going to delete the 'New events Sample' object. First we
go to the contents tab and select the 'New events Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New events Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New events
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New events Sample' in browser.contents
    False

Adding a new events content item as contributor
------------------------------------------------

Not only site managers are allowed to add events content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'events' and click the 'Add' button to get to the add form.

    >>> browser.getControl('events').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'events' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'events Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new events content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



