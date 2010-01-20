# -*- coding: ISO-8859-15 -*-
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

import config
from zope.interface import Interface

if config.HAS_JSON:
    IJSONRPCRequest = config.IJSONRPCRequest
    IJSONStreamWriteable = config.IJSONStreamWriteable
    IJSONWriter = config.IJSONWriter
else:
    # If jsonserver is not present, we just define interfaces
    # that noone implements so the adapters will never be looked up.
    # This is because the zcml will try to import these.
    # XXX occasionally this should be done from the zcml, 
    # via features/conditionals!
    
    class IJSONRPCRequest(Interface):
        'Interface never to be implemented'

    class IJSONStreamWriteable(Interface):
        'Interface never to be implemented'
        
    class IJSONWriter(Interface):
        'Interface never to be implemented'
