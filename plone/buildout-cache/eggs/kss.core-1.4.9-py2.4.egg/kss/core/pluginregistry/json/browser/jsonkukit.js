
/*
* Copyright (c) 2005-2006
* Authors:
*   Balázs Reé <ree@greenfinity.hu>
*
* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
* 02111-1307, USA.
*/

/*
* Supplemental script for json
*
* This gets included when json plugins are registered.
*
* This transparently replaces the normal transport with JSON.
* To do this, we overwrite notifyServer and at one point we 
* return to the normal execution chain (after results are received).
* (We need to do this because even an old style event plugin may
* invoke new style command plugins as a response.)
*
* To manually call the server from an event plugin, the
* makeJSONKukitMethod function should be used to create a
* proxy method.
*/

kukit.makeJSONKukitMethod = function(url, methodName, supplement) {
	// url and methodName can be used, 
	// or methodName can be set to null and url will be used as a full url.
	if (typeof(supplement) == 'undefined') {
    	// default timeout is 4 sec... a sane choice
		supplement = null;
	}
    // XXX RequestManager of json is not compatible with kukit's at the moment.
    return new JSONRPCMethod(url, methodName, kukit.jsonCallback, kukit.jsonError,
			null, supplement, null, null);
}

// OVERWRITE kukit.js
kukit.notifyServer = function(url, params, oper) {
    var f = function(queueItem) {
        // store the queue reception on the oper
        oper.queueItem = queueItem;
        // sending form, with standard form parameters.
        var method = kukit.makeJSONKukitMethod(url, null, oper);
	    method(params);
    };
   kukit.requestManager.notifyServer(f, url);
}

kukit.jsonCallback = function(result, oper) {
    // notify the queue that we are done
    var success = oper.queueItem.receivedResult()
    // We only process if the response has not been timed
    // out by the queue in the meantime.
    if (success) {
        try {
            var command_processor = new kukit.CommandProcessor();
            // Transport parm is same as result (although we don't use it)
            command_processor.parseCommands(result, result);
            command_processor.executeCommands(oper);
        } catch(e) {
            kukit.logError('Error during command execution: ' + e);
            throw e;
        }
    }
}

kukit.jsonError = function(result, oper) {
    // XXX at the moment timeouts don't arrive here...
    // notify the queue that we are done
    var success = oper.queueItem.receivedResult()
    kukit.logError('JSON call failed: ' + result); 
}

/* Command execution */

// OVERWRITE kukit.js
kukit.CommandProcessor.prototype.parseCommand = function(command, transport) {
    // Add the command.
    var command = new kukit.cr.makeCommand(command.selector, command.name, command.selectorType, command.params, transport);
    this.addCommand(command);
} 

