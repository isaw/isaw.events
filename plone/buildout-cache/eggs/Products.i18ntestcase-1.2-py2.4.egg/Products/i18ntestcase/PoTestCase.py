import os, re
import I18NTestCase
from I18NTestCase import getFileFromPath, getLanguageFromPath, \
                         getLanguageFromLocalesPath

from gettext import GNUTranslations
from Products.PlacelessTranslationService import msgfmt
from i18ndude import catalog

class PoTestCase(I18NTestCase.I18NTestCase):
    po = None
    product = None
    pot_cat = None
    pot_len = None

    def testPoFile(self):
        """ Testing po file """
        po = self.po
        product = self.product
        pot_cat = self.pot_cat
        pot_len = self.pot_len
        poName = getFileFromPath(po)
        localesLayout = False
        if 'LC_MESSAGES' in po:
            localesLayout = True

        file = open(po, 'r')
        try:
            lines = file.readlines()
        except IOError, msg:
            self.fail('Can\'t read po file %s:\n%s' % (poName,msg))
        file.close()
        try:
            mo = msgfmt.Msgfmt(lines)
        except msgfmt.PoSyntaxError, msg:
            self.fail('PoSyntaxError: Invalid po data syntax in file %s:\n%s' % (poName, msg))
        except SyntaxError, msg:
            self.fail('SyntaxError: Invalid po data syntax in file %s (Can\'t parse file with eval():\n%s' % (poName, msg))
        except Exception, msg:
            self.fail('Unknown error while parsing the po file %s:\n%s' % (poName, msg))
        try:
            tro = GNUTranslations(mo.getAsFile())
        except UnicodeDecodeError, msg:
            self.fail('UnicodeDecodeError in file %s:\n%s' % (poName, msg))
        except msgfmt.PoSyntaxError, msg:
            self.fail('PoSyntaxError: Invalid po data syntax in file %s:\n%s' % (poName, msg))

        domain = tro._info.get('domain', None)
        if localesLayout:
            self.failIf(domain, 'Po file %s has a domain set inside the file!' % po)
        else:
            self.failUnless(domain, 'Po file %s has no domain!' % po)

        language = tro._info.get('language-code', None)
        if localesLayout:
            self.failIf(language, 'Po file %s has a language set inside!' % po)
        else:
            self.failUnless(language, 'Po file %s has no language!' % po)

        if localesLayout:
            fileLang = getLanguageFromLocalesPath(po)
        else:
            fileLang = getLanguageFromPath(po)
            language = language.replace('_', '-')
            self.failUnless(fileLang == language,
                'The file %s has the wrong name or wrong language code. expected: %s, got: %s' % (poName, language, fileLang))

        if fileLang != 'en':
            po_cat = catalog.MessageCatalog(filename=po)

            if pot_len != len(po_cat):
                missing = [msg for msg in pot_cat if msg not in po_cat]
                additional = [msg for msg in po_cat if msg not in pot_cat]

                self.fail('%s missing and %s additional messages in %s:\nmissing: %s\nadditional: %s'
                          % (len(missing), len(additional), poName, missing, additional))

        msgcatalog = [(msg, tro._catalog.get(msg)) for msg in tro._catalog if msg]

        for msg, msgstr in msgcatalog:
            # every ${foo} is properly closed
            if '${' in msgstr:
                status, error = self.isMalformedMessageVariable(msgstr)
                self.failIf(status, '%s in file %s:\n %s' % (error, poName, msg))
            # no html-entities in msgstr
            if '&' in msgstr and ';' in msgstr:
                status, error = self.isEntity(msgstr)
                self.failIf(status, '%s in file %s:\n %s' % (error, poName, msg))
            # all ${foo}'s from the default should be present in the translation
            default = pot_cat.getDefault(msg)
            default_vars = self.getMessageVariables(msg, default)
            if not default_vars is []:
                status, error = self.isMessageVariablesMissing(msgstr, default_vars=default_vars)
                self.failIf(status, '%s in file %s: %s' % (error, poName, msg))

