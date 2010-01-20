# For Zope 2.9 we don't want to have a zope.deferredimport dependency,
# if only we could start using real dependencies
try:
    import zope.deferredimport

    zope.deferredimport.deprecated(
        "The convenience import confuses the test coverage tools. "
        "Please use the fully qualified name instead.",
        FormFieldsets = 'plone.fieldsets.fieldsets:FormFieldsets',
        )
except ImportError:
    pass
