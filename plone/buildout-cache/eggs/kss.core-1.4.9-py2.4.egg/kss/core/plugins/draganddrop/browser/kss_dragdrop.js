kukit.draganddrop = {};

kukit.draganddrop.DragAndDropEvent = function() {
};

kukit.draganddrop.DragAndDropEvent.prototype.isNotBoundDraggable = function(oper) {
    var info = kukit.engine.binderInfoRegistry.getBinderInfoById(this.__binder_id__);
    return ! (info.bound.getBoundOperForNode('drop', oper.node) || 
           info.bound.getBoundOperForNode('hover', oper.node));
};

kukit.draganddrop.DragAndDropEvent.prototype.isNotBoundDroppable = function(oper) {
    var info = kukit.engine.binderInfoRegistry.getBinderInfoById(this.__binder_id__);
    return ! (info.bound.getBoundOperForNode(this, 'drag', oper.node) || 
           info.bound.getBoundOperForNode(this, 'start', oper.node) || 
           info.bound.getBoundOperForNode(this, 'end', oper.node));
};

kukit.draganddrop.DragAndDropEvent.prototype.__bind_drop__ = function(name, func_to_bind, oper) {
    // validate and set parameters
    oper.completeParms([], {}, 'dad-drop event binding');
    self = this;
    if (this.isNotBoundDroppable(oper)) {
        var options = {
            onDrop : this.__make_func_to_bind__('drop', oper.node),
            onHover: this.__make_func_to_bind__('hover', oper.node)
        };        
        Droppables.add(oper.node, options);
        kukit.logDebug('Droppable bound');
    }
};

kukit.draganddrop.DragAndDropEvent.prototype.__bind_drag__ = function(name, func_to_bind, oper) {
    // validate and set parameters
    oper.completeParms([], {'constraint' : 'not-set'}, 'dad-drag event binding');
    if (this.isNotBoundDraggable(oper)) {
        var options = {
            onDrag : this.__make_func_to_bind__('drag', oper.node),
            onStart : this.__make_func_to_bind__('start', oper.node),
            onEnd : this.__make_func_to_bind__('end', oper.node)
        };
        if (oper.parms.constraint == 'horizontal' || oper.parms.constraint == 'vertical') {
            kukit.logDebug('constraint: ' + oper.parms.constraint + "|" + name);
            options['constraint'] = oper.parms.constraint;
        }
        new Draggable(oper.node, options);
        kukit.logDebug('Draggable bound');
    }
};

kukit.eventsGlobalRegistry.register('dad', 'drop', kukit.draganddrop.DragAndDropEvent, '__bind_drop__', null);
kukit.eventsGlobalRegistry.register('dad', 'hover', kukit.draganddrop.DragAndDropEvent, '__bind_drop__', null);
kukit.eventsGlobalRegistry.register('dad', 'drag', kukit.draganddrop.DragAndDropEvent, '__bind_drag__', null);
kukit.eventsGlobalRegistry.register('dad', 'start', kukit.draganddrop.DragAndDropEvent, '__bind_drag__', null);
kukit.eventsGlobalRegistry.register('dad', 'end', kukit.draganddrop.DragAndDropEvent, '__bind_drag__', null);

/*

// This is how it should look like:

kukit.draganddrop.DragAndDropEvent.prototype.__bind_drag__ = function(opers) {
    kukit.log('Binding DRAG started');
    for (var i=0; i<opers.length; i++) { opers[i].logDebug(); }
};

kukit.draganddrop.DragAndDropEvent.prototype.__bind_drop__ = function(opers) {
    kukit.log('Binding DROP started');
    for (var i=0; i<opers.length; i++) { opers[i].logDebug(); }
};


kukit.eventsGlobalRegistry.registerForAllEvents('dad', ['drag', 'start', 'end'], kukit.draganddrop.DragAndDropEvent, '__bind_drag__', null, 'opers');
kukit.eventsGlobalRegistry.registerForAllEvents('dad', ['drop', 'hover'], kukit.draganddrop.DragAndDropEvent, '__bind_drop__', null, 'opers');

*/
