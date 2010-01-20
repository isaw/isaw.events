
try:
    import Products.Five
except ImportError:
    pass
else:
    import simplecontent

    def initialize(context):

        context.registerClass(
            simplecontent.SimpleContent,
            constructors = (simplecontent.manage_addSimpleContentForm,
                            simplecontent.manage_addSimpleContent),
            )
