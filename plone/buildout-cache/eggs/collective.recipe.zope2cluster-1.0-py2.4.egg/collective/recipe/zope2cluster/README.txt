Supported options
=================

The recipe supports the following options:

instance-clone
    The name of the part that you want to 'clone'.  Typically instance.

Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = instance instance2
    ... index = http://pypi.python.org/simple
    ... 
    ... [instance]
    ... recipe = plone.recipe.zope2instance
    ... zope2-location = %(zope2_location)s
    ... user = admin:admin
    ... ip-address = 192.168.0.1
    ... http-address = 8080
    ... effective-user = zope
    ... event-log-level = CRITICAL
    ... 
    ... [instance2]
    ... recipe = collective.recipe.zope2cluster
    ... instance-clone = instance
    ... ip-address = 192.168.0.2
    ... http-address = 8081
    ... event-log-level = WARN
    ... """ % globals())

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start...
    Installing instance2.
    ...

First let's check to see that the original instance has the correct options::

    >>> instance = os.path.join(sample_buildout, 'parts', 'instance')
    >>> zc = open(os.path.join(instance, 'etc', 'zope.conf')).read()
    >>> print zc
    instancehome /sample-buildout/parts/instance
    ...
    effective-user zope
    ip-address 192.168.0.1
    ...
    <eventlog>
      level CRITICAL
    ...
    </eventlog>
    ...
    <http-server>
    ...
      address 8080
    ...
    </http-server>
    ...

Now let's check our instance2 part to see if it is setup correctly::

    >>> instance = os.path.join(sample_buildout, 'parts', 'instance2')
    >>> zc = open(os.path.join(instance, 'etc', 'zope.conf')).read()
    >>> print zc
    instancehome /sample-buildout/parts/instance2
    ...
    effective-user zope
    ip-address 192.168.0.2
    ...
    <eventlog>
      level WARN
    ...
    </eventlog>
    ...
    <http-server>
    ...
      address 8081
    ...
    </http-server>
    ...
