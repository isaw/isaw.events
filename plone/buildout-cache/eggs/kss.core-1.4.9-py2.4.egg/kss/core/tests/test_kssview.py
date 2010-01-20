# -*- coding: latin-1 -*-
# Copyright (c) 2005-2007
# Authors: KSS Project Contributors (see docs/CREDITS.txt)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

import unittest

from kss.core.interfaces import IKSSView, IKSSCommands
from kss.core.plugins.core.interfaces import IKSSCoreCommands
from kss.core.plugins.core.commands import KSSCoreCommands
from kss.core.pluginregistry.interfaces import IAction, ICommandSet
from kss.core.pluginregistry.action import Action
from kss.core.pluginregistry.plugin import registerPlugin
from kss.core.pluginregistry.commandset import CommandSet
from kss.core.tests.commandinspector import CommandInspectorView

import zope.component.event
from zope.testing import doctest, cleanup
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.component.hooks import setHooks

def setUpAjaxView(test=None):
    setHooks()
    zope.component.provideAdapter(CommandInspectorView,
                                  adapts=(IKSSCommands, IBrowserRequest))
    registerPlugin(Action, IAction, 'replaceInnerHTML', None,
                   'selector', 'html', [], None)
    zope.component.provideAdapter(KSSCoreCommands,
                                  adapts=(IKSSView,),
                                  provides=IKSSCoreCommands)
    registerPlugin(CommandSet, ICommandSet, 'core', IKSSCoreCommands)

def tearDownAjaxView(test=None):
    cleanup.cleanUp()

def test_suite():
    return unittest.TestSuite([
        doctest.DocTestSuite('kss.core.kssview'),
        doctest.DocFileSuite('kssview.txt',
                             package='kss.core',
                             setUp=setUpAjaxView,
                             tearDown=tearDownAjaxView),
        ])
