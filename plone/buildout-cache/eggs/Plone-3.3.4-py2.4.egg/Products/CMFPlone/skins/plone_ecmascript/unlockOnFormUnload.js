/* Unlock the object on form unload, and refresh the lock every 5 minutes */
if (typeof(plone)=='undefined')
    var plone = {};

plone.UnlockHandler = {
    init: function() {
        // set up the handler, if there are any forms
        if (jq('form.enableUnlockProtection').length) {
            jq(window).unload(plone.UnlockHandler.execute);
            plone.UnlockHandler._refresher = setInterval(plone.UnlockHandler.refresh, 300000);
        }
    },
    
    cleanup: function() {
        jq(window).unbind('unload', plone.UnlockHandler.execute);
        clearInterval(plone.UnlockHandler._refresher);
    },
    
    execute: function() {
        // this.submitting is set from the form unload handler
        // (formUnload.js) and signifies that we are in the
        // form submit process. This means: no unlock needed,
        // and it also would be harmful (ConflictError)
        if (this.submitting) return;
        jq.get(plone.UnlockHandler._baseUrl() + '/@@plone_lock_operations/safe_unlock');
    },
    
    refresh: function() {
        if (this.submitting) return;
        jq.get(plone.UnlockHandler._baseUrl() + '/@@plone_lock_operations/refresh_lock');
    },
    
    _baseUrl: function() {
        var baseUrl = jq('base').attr('href');
        if (!baseUrl) {
            var pieces = window.location.href.split('/');
            pieces.pop();
            baseUrl = pieces.join('/');
        }
        return baseUrl;
    }
};

jq(plone.UnlockHandler.init);
