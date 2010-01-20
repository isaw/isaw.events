
// bind action menus on load


kukit.actionsGlobalRegistry.register("bindActionMenus", function (oper) {
        initializeMenus();
        kukit.logDebug('Plone menus initialized');
    });

kukit.log('Plone legacy [initializeMenus] action registered.');

