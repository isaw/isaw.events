import fnmatch
import logging
import os
from os.path import isdir
from os.path import join
from stat import ST_MTIME

from Products.PlacelessTranslationService.utils import log
from Products.PlacelessTranslationService.msgfmt import Msgfmt
from Products.PlacelessTranslationService.msgfmt import PoSyntaxError

# Restrict languages
PTS_LANGUAGES = None
if bool(os.getenv('PTS_LANGUAGES')):
    langs = os.getenv('PTS_LANGUAGES')
    langs = langs.strip().replace(',', '').split()
    PTS_LANGUAGES = tuple(langs)


def _checkLanguage(lang):
    if PTS_LANGUAGES is None:
        return True
    else:
        return bool(lang in PTS_LANGUAGES)


def _updateMoFile(name, msgpath, lang, domain, mofile):
    """
    Creates or updates a mo file in the locales folder. Returns True if a
    new file was created.
    """
    pofile = join(msgpath, name)
    create = False
    update = False

    try:
        po_mtime = os.stat(pofile)[ST_MTIME]
    except (IOError, OSError):
        po_mtime = 0

    if os.path.exists(mofile):
        # Update mo file?
        try:
            mo_mtime = os.stat(mofile)[ST_MTIME]
        except (IOError, OSError):
            mo_mtime = 0

        if po_mtime > mo_mtime:
            # Update mo file
            update = True
        else:
            # Mo file is current
            return
    else:
        # Create mo file
        create = True

    if create or update:
        try:
            mo = Msgfmt(pofile, domain).getAsFile()
            fd = open(mofile, 'wb')
            fd.write(mo.read())
            fd.close()

        except (IOError, OSError, PoSyntaxError):
            log('Error while compiling %s' % pofile, logging.WARNING)
            return

        if create:
            return True

    return None

def _compile_locales_dir(basepath):
    """
    Compiles all po files in a locales directory (Zope3 format) to mo files.
    Format:
        Products/MyProduct/locales/${lang}/LC_MESSAGES/${domain}.po
    Where ${lang} and ${domain} are the language and the domain of the po
    file (e.g. locales/de/LC_MESSAGES/plone.po)
    """
    basepath = str(os.path.normpath(basepath))
    if not isdir(basepath):
        return

    for lang in os.listdir(basepath):
        if not _checkLanguage(lang):
            continue
        langpath = join(basepath, lang)
        if not isdir(langpath):
            # it's not a directory
            continue
        msgpath = join(langpath, 'LC_MESSAGES')
        if not isdir(msgpath):
            # it doesn't contain a LC_MESSAGES directory
            continue
        names = fnmatch.filter(os.listdir(msgpath), '*.po')
        for name in names:
            domain = name[:-3]
            mofile = join(msgpath, name[:-2] + 'mo')
            result = _updateMoFile(name, msgpath, lang, domain, mofile)
