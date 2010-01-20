
/*
 * Event plugins for the binderclasses demo
 *
 * We test several things here:
 *
 * - Inheritence can be used to set up the event binder class.
 *   The __bind_click__ method is accessable from the subclass.
 *
 * - The event binder can have a constructor, and what is set up in the constructor
 *   will become a property of the instance, not of the class.
 *
 * - Event names defined on the same class, will be bound to the same
 *   class, not different ones. This means if the events bind to the same
 *   instance id, they share a common state.
 */

(function () {           // BEGIN CLOSURE

var AlphaBinder = function() {
    this.counter = [50];

    this.customBind = function(name, func_to_bind, oper) {
        // validate and set parameters
        oper.evaluateParameters([], {}, 'testbinderclasses event binding');
        // Apply a filter before the execute actions hook.
        // It always returns true, causing the actions to execute
        // always.
        // It sets up the counter on it, which can be used
        // from action parameters as pass(counter).
        var self = this;
        var filter = function(oper) {
            oper.defaultParameters = {
                    counter:  '[' + self.counter[0] + ']'};
            self.counter[0]++;
            return true;
        }
        // register this as a "click" browser event
        kukit.pl.registerBrowserEvent(oper, filter, 'click');

    };

    this._prepareExecuteActions = function(oper) {
        // Set up the execution of the actions.
        // Make counter available from action parameters 
        // as pass(counter).
    };

};

kukit.eventsGlobalRegistry.register('testbinderclass', 'alphaone', AlphaBinder, 'customBind', null);


var BetaBinder = function(name, func_to_bind, oper) {
    this.counter = [100];
};
// inherited from AlphaBinder
BetaBinder.prototype = new AlphaBinder();

kukit.eventsGlobalRegistry.register('testbinderclass', 'betaone', BetaBinder, 'customBind', null);
kukit.eventsGlobalRegistry.register('testbinderclass', 'betatwo', BetaBinder, 'customBind', null);

})();            // END CLOSURE
