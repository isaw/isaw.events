
/* Event plugins for the more_selector demo */
kukit.more_selectors = {};

kukit.more_selectors.AnnoyClickerEvent = function() {

this.__bind_click__ = function(name, func_to_bind, oper) {
    // validate and set parameters
    oper.evaluateParameters([], {'count': '3'}, 'annoyClicker event binding');
    oper.evalInt('count', 'annoyClicker event binding');
    if (oper.parms.count < 1)
        throw 'Parameter count must be > 0, "' + oper.parms.count + '"';
    // overwrite countsomuch
    this.countsomuch = oper.parms.count;
    this.count = this.countsomuch;
    // register this as a "click" browser event
    oper.parms = {};
    kukit.pl.registerBrowserEvent(oper, null, 'click');
};

this.__default_click__ = function(name, oper) {
    oper.evaluateParameters([], {}, 'annoyClicker event binding');
    this.count -= 1;
    if (this.count == 0) {
        // Continue with the real action.
        this.count = this.countsomuch;
        this.continueEvent('doit', oper.node, {});
    } else {
        this.continueEvent('annoy', oper.node, {});
    }
};

};

kukit.eventsGlobalRegistry.register('annoyclicker', 'click', kukit.more_selectors.AnnoyClickerEvent, '__bind_click__', '__default_click__');
kukit.eventsGlobalRegistry.register('annoyclicker', 'annoy', kukit.more_selectors.AnnoyClickerEvent, null, null);
kukit.eventsGlobalRegistry.register('annoyclicker', 'doit', kukit.more_selectors.AnnoyClickerEvent, null, null);

