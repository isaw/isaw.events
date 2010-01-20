

Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = controller
    ...
    ... [controller]
    ... recipe = plone.recipe.osxcontroller
    ... """)

Running the buildout gives us::

    >>> print 'start', system(buildout) 
    start...
    Installing controller.
    <BLANKLINE>

Let's look for the symlinks to our app::

    >>> ls(sample_buildout)
    -  .installed.cfg
    d  PloneController.app
    d  bin
    -  buildout.cfg
    d  develop-eggs
    d  eggs
    d  parts

