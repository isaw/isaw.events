

// bind toc code


kukit.actionsGlobalRegistry.register("createTableOfContents", function (oper) {
        createTableOfContents();
    });
kukit.commandsGlobalRegistry.registerFromAction('createTableOfContents', kukit.cr.makeGlobalCommand);

kukit.log('Plone [createTableOfContents] action registered.');

