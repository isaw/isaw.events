##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
""" Mounted database support

A MountedTemporaryFolder is an object that is a mount point.  It mounts a
TemporaryStorage-backed database and masquerades as its root object.
When you traverse one of these things, the __of__ method of the mount
point object is called, and that returns a Folder object that actually
lives in another ZODB.

To understand this fully, you'll need to read the source of
Products.TemporaryFolder.mount.MountPoint.

$Id: TemporaryFolder.py 100882 2009-06-11 17:57:50Z tseaver $
"""
__version__='$Revision: 1.12 $'[11:-2]

from App.special_dtml import DTMLFile
from App.special_dtml import HTMLFile
from OFS.Folder import Folder
from OFS.SimpleItem import Item
from tempstorage.TemporaryStorage import TemporaryStorage
from ZODB.DB import DB

from Products.TemporaryFolder.mount import MountPoint

ADD_TEMPORARY_FOLDER_PERM="Add Temporary Folder"


def constructTemporaryFolder(self, id, title=None, REQUEST=None):
    """ """
    ms = MountedTemporaryFolder(id, title)
    self._setObject(id, ms)
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

constructTemporaryFolderForm=HTMLFile('dtml/addTemporaryFolder', globals())


class SimpleTemporaryContainer(Folder):
    # dbtab-style container class
    meta_type = 'Temporary Folder'
    icon = 'misc_/TemporaryFolder/tempfolder.gif'


class MountedTemporaryFolder(MountPoint, Item):
    """
    A mounted RAM database with a basic interface for displaying the
    reason the database did not connect.

    XXX this is only here for backwards compatibility purposes:
    DBTab uses the SimpleTemporaryContainer class instead.
    """
    icon = 'p_/broken'
    manage_options = ({'label':'Traceback', 'action':'manage_traceback'},)
    meta_type = 'Broken Temporary Folder'

    def __init__(self, id, title='', params=None):
        self.id = str(id)
        self.title = title
        MountPoint.__init__(self, path='/') # Eep

    manage_traceback = DTMLFile('dtml/mountfail', globals())

    def _createDB(self, db=None): # huh?  db=db was original
        """ Create a mounted RAM database """
        db = DB(TemporaryStorage())
        # the connection in 2.5.X - 2.6.1 was a "low conflict connection",
        # but this caused synchronization problems.  For 2.6.2, we want
        # to reenable read conflict errors, so we use a default connection
        # type.
        #db.klass = LowConflictConnection
        return db

    def _getMountRoot(self, root):
        sdc = root.get('folder', None)
        if sdc is None:
            sdc = root['folder'] = Folder()
            self._populate(sdc, root)

        return sdc

    def mount_error_(self):
        return self._v_connect_error

    def _populate(self, folder, root):
        # Set up our folder object
        folder.id = self.id                     # be a chameleon
        folder.title = self.title
        folder.icon = "misc_/TemporaryFolder/tempfolder.gif"
        s=folder.manage_options[1:]
        folder.manage_options = (
            {'label':'Contents', 'action':'manage_main',
             'help':('TemporaryFolder','TemporaryFolder.stx')},
            )+s
