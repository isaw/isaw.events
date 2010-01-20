##################################################################
#
# (C) Copyright 2006-2007 ObjectRealms, LLC
# All Rights Reserved
#
# This file is part of iterate.
#
# iterate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# iterate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CMFDeployment; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################

"""
$Id: copier.py 1824 2007-02-08 17:59:41Z hazmat $
"""

from zope import interface, component
from zope.annotation.interfaces import IAnnotations

from Acquisition import aq_base, aq_parent, aq_inner
from ZODB.PersistentMapping import PersistentMapping

from Products.Archetypes.Referenceable import Referenceable
from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

import interfaces
from relation import WorkingCopyRelation
from interfaces import CheckinException

class ContentCopier( object ):

    interface.implements( interfaces.IObjectCopier )
    component.adapts( interfaces.IIterateAware )

    def __init__( self, context ):
        self.context = context

    def copyTo( self, container ):
        wc = self._copyBaseline( container )
        wc_ref = wc.addReference( self.context,
                                  relationship = WorkingCopyRelation.relationship,
                                  referenceClass = WorkingCopyRelation )
        self._handleReferences( self.context, wc, "checkout", wc_ref )
        return wc, wc_ref
    
    def merge( self ):
        baseline = self._getBaseline()

        # delete the working copy reference to the baseline
        wc_ref = self._deleteWorkingCopyRelation()
        
        # reassemble references on the new baseline         
        self._handleReferences( baseline, self.context, "checkin", wc_ref )

        # move the working copy to the baseline container, deleting the baseline 
        new_baseline = self._replaceBaseline( baseline )

        # patch the working copy with baseline info not preserved during checkout
        self._reassembleWorkingCopy( new_baseline, baseline )

        return new_baseline

    def _getBaseline( self ):
        # follow the working copy's reference back to the baseline
        refs = self.context.getRefs( WorkingCopyRelation.relationship )

        if not len(refs) == 1:
            raise CheckinException( "Baseline count mismatch" )

        if not refs or refs[0] is None:
            raise CheckinException( "Baseline has disappeared" )

        baseline = refs[0]
        return baseline


    def _replaceBaseline( self, baseline ):
        # move the working copy object to the baseline, returns the new baseline
        baseline_id = baseline.getId()
        
        # delete the baseline from the folder to make room for the committed working copy
        baseline_container = aq_parent( aq_inner( baseline ) )
        baseline_container._delOb( baseline_id )

        # delete the working copy from the its container
        wc_container =  aq_parent( aq_inner( self.context ) )

        # trick out the at machinery to not delete references
        self.context._v_cp_refs = 1
        self.context._v_is_cp = 0
        
        wc_container.manage_delObjects( [self.context.getId()] )
        
        # move the working copy back to the baseline container
        working_copy = aq_base( self.context )
        working_copy.setId( baseline_id )
        baseline_container._setOb( baseline_id, working_copy )

        new_baseline = baseline_container._getOb( baseline_id )
        
        # reregister our references with the reference machinery after moving
        Referenceable.manage_afterAdd( new_baseline, new_baseline, baseline_container)
        
        return new_baseline

    def _reassembleWorkingCopy( self, new_baseline, baseline ):
        # reattach the source's workflow history, try avoid a dangling ref 
        try:
            new_baseline.workflow_history = PersistentMapping( baseline.workflow_history.items() )
        except AttributeError:
            # No workflow apparently.  Oh well.
            pass

        # reset wf state security directly
        workflow_tool = getToolByName(self.context, 'portal_workflow')
        wfs = workflow_tool.getWorkflowsFor( self.context )
        for wf in wfs:
            if not isinstance( wf, DCWorkflowDefinition ):
                continue
            wf.updateRoleMappingsFor( new_baseline )

        # reattach the source's uid, this will update wc refs to point back to the new baseline
        new_baseline._setUID( baseline.UID() )

        # reattach the source's history id, to get the previous version ancestry
        histid_handler = getToolByName( self.context, 'portal_historyidhandler')
        huid = histid_handler.getUid( baseline )
        histid_handler.setUid( new_baseline, huid, check_uniqueness=False )

        return new_baseline

    def _deleteWorkingCopyRelation( self ):
        # delete the wc reference keeping a reference to it for its annotations
        refs = self.context.getReferenceImpl( WorkingCopyRelation.relationship )
        wc_ref = refs[0]
        self.context.deleteReferences( WorkingCopyRelation.relationship )
        return wc_ref

    #################################
    ## Checkout Support Methods
    
    def _copyBaseline( self, container ):
        # copy the context from source to the target container
        source_container = aq_parent( aq_inner( self.context ) )
        clipboard = source_container.manage_copyObjects( [ self.context.getId() ] )
        result = container.manage_pasteObjects( clipboard )

        # get a reference to the working copy
        target_id = result[0]['new_id']
        target = container._getOb( target_id )
        return target

    
    def _handleReferences( self, baseline, wc, mode, wc_ref ):

        annotations = IAnnotations( wc_ref )
        
        baseline_adapter = interfaces.ICheckinCheckoutReference( baseline )
        
        # handle forward references
        for relationship in baseline.getRelationships():
            # look for a named relation adapter first
            adapter = component.queryAdapter( baseline,
                                              interfaces.ICheckinCheckoutReference,
                                              relationship )
            
            if adapter is None: # default
                adapter = baseline_adapter
                
            references = baseline.getReferenceImpl( relationship )

            mode_method = getattr( adapter, mode )
            mode_method( baseline, wc, references, annotations )

        mode = mode + "BackReferences"
        
        # handle backward references
        for relationship in baseline.getBRelationships():
            adapter = component.queryAdapter( baseline,
                                              interfaces.ICheckinCheckoutReference,
                                              relationship )
            if adapter is None:
                adapter = baseline_adapter
                
            references = baseline.getBackReferenceImpl( relationship )
            
            mode_method = getattr( adapter, mode )
            mode_method( baseline, wc, references, annotations )
