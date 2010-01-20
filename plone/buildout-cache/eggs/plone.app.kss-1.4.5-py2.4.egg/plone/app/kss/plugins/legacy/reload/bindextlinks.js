
// bind external links marking on load

kukit.plonelegacy = {};

if (typeof(scanforlinks) == 'undefined') {
    kukit.plonelegacy.bindExternalLinks = function() {}
    }
else {
    kukit.plonelegacy.bindExternalLinks = function() {
        scanforlinks();
        }
    }

kukit.actionsGlobalRegistry.register("bindExternalLinks", function (oper) {
        kukit.plonelegacy.bindExternalLinks();
        kukit.logDebug('Plone external links bound.');
    });

kukit.log('Plone legacy [bindExternalLinks] action registered.');



