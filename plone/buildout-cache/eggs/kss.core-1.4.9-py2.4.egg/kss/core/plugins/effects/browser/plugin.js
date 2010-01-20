
// Scriptaculous Effects

if (typeof(Effect) != "undefined") {
    kukit.HASEFFECTS = 1;
} else {
    kukit.HASEFFECTS = 0;
}

if (kukit.HASEFFECTS && typeof(Effect.Transitions) != "undefined") {
    kukit.actionsGlobalRegistry.register("effect", function (oper) {
        oper.evaluateParameters([], {'type': 'fade'}, 'scriptaculous effect');
        var node = oper.node;
        if (oper.parms.type == 'fade') {
        new Effect.Fade(node);
        } else if (oper.parms.type == 'appear') {
        new Effect.Appear(node);
        } else if (oper.parms.type == 'puff') {
        new Effect.Puff(node);
        } else if (oper.parms.type == 'blinddown') {
        new Effect.BlindDown(node);
        } else if (oper.parms.type == 'blindup') {
        new Effect.BlindUp(node);
        }
    });

    kukit.commandsGlobalRegistry.registerFromAction('effect', kukit.cr.makeSelectorCommand);

    // This is terrible. We needed to copy this part
    // from prototype. Notice that I put this.$ =
    // in the beginning. Without that the function
    // declarations in IE won't overwrite each others,
    // and one of them (first or last occurence) comes
    // in. Now, we have a contradicting $ declaration
    // in Mochikit, causing the problem.

    this.$ = function $() {
      var results = [], element;
      for (var i = 0; i < arguments.length; i++) {
        element = arguments[i];
        if (typeof element == 'string')
          element = document.getElementById(element);
        results.push(Element.extend(element));
      }
      return results.length < 2 ? results[0] : results;
    };
}
