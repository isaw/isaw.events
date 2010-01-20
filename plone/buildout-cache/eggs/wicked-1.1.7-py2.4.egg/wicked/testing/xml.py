# ganked from zopt and sfive
import os
from StringIO import StringIO
USELIBXML = False

slug = """ <div><some tag="true">
               <other />            </some>
     </div>
     """
xslt = """
<xsl:stylesheet version='1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
  <xsl:output method="html" indent="yes"/>
  <xsl:strip-space elements="*"/>
  <xsl:template match="@*|node()">
    <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
  </xsl:template>
</xsl:stylesheet>
"""

#import libxml2, libxslt
xsltfile = os.path.join(os.path.dirname(__file__), 'strip.xsl')
 	
#use stylesheet as global

try:
    import libxml2, libxslt
    styledoc=libxml2.parseFile(xsltfile)
    style=libxslt.parseStylesheetDoc(styledoc)

    def libstrip(text):
        """
        strip out whitespace
        >>> print xstrip(slug)
        <div><some tag="true"><other></other></some></div>
        ...
        """
        encoding = 'UTF-8'
        INDENT = True
        try:
            doc = libxml2.parseDoc(text)
            res = style.applyStylesheet(doc, None)
            # XXX: this raises an unhandled c exception
            #res = style.saveResultToString(resdoc)
            out = res.serialize(encoding=encoding, format=INDENT)
        finally:
            try: doc.freeDoc()
            except: pass
            try: res.freeDoc()
            except: pass
        return out

except ImportError:
    libstrip = None


def lxmlstrip(text):
    """
    strip out whitespace
    >>> print xstrip(slug)
    <div><some tag="true"><other></other></some></div>
    ...
    """
    if not text:
        return ''
    
    from lxml import etree
    xslt_doc = etree.XML(xslt)
    stripper = etree.XSLT(xslt_doc)
    doc = etree.XML(text)
    result = stripper(doc)
    val = str(result)
    return val

if libstrip and USELIBXML:
    xstrip = libstrip
else:
    xstrip = lxmlstrip

import unittest
from zope.testing import doctest
optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS
def test_suite():

    return unittest.TestSuite((
        doctest.DocTestSuite('xml', optionflags=optionflags)
        ))

if __name__=="__main__":
    unittest.TextTestRunner().run(test_suite())
