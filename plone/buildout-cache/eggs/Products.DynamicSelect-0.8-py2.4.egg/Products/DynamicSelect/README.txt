1. Description

The DynamicSelectWidget is a implementation of the dojo selectbox (combobox).

A combobox is like a text <input> field (ie, you can input any value you want), but it also has a list of suggested values that you can choose from. The drop down list is filtered by the data you have already typed in. (text from http://archive.dojotoolkit.org/nightly/widget/tests/widget/test_Select.html)

Get an idea by visiting  a 'demo' (http://archive.dojotoolkit.org/nightly/widget/tests/widget/test_Select.html) of the dojo widget itself.

2. Installation

Just unpack the tarball, add it to your products directory, restart zope and install (quickinstaller) the package.

Import it into your product:


    from Products.DynamicSelect.DynamicSelectWidget import DynamicSelectWidget


Use it in your Schema:

    StringField(
        name='TestField',
        widget=DynamicSelectWidget(
                width="300px",
                label="Test",
                description="just a test",
               ) ,
        vocabulary=DisplayList((
                            ('at', u'Austria'),
                            ('gr', u'Greece'),
                            ('de', u'Germany'),
                            ('it', u'Italy'),
                        )),
        required=1
    ),


width: a style defenition of the widgets width in px.

3. Reporting bugs / feature requests

author: gabriel.pendl(at)dek.at
