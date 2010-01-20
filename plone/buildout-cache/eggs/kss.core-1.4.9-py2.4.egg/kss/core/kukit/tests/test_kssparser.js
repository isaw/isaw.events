/*
* Copyright (c) 2005-2007
* Authors: KSS Project Contributors (see docs/CREDITS.txt) 
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

if (typeof(kukit) == "undefined") {
    var kukit = {};
}

kukit.KssParserTestCaseBase = function() {

    this.setUp = function() {
        kukit.eventsGlobalRegistry.register('dnd', 'drag',
            kukit.pl.NativeEventBinder, '__bind__nodeordocument', null);
    };

    this.tearDown = function() {
        kukit.eventsGlobalRegistry.unregister('dnd', 'drag');
    };

    this.assertKssParmValueEquals = function(a, b, reason) {
        if (typeof(reason) == 'undefined') {
            reason = '';
        } else {
            reason += ', ';
        }
        this.assertEquals(a.isMethod, b.isMethod, reason + 'different types');
        if (! a.isMethod) {
            this.assertEquals(a.txt, b.txt, reason + 'text mismatch' );
        } else {
            this.assertEquals(a.methodName, b.methodName, reason + 'methodName mismatch');
            this.assertListEquals(a.args, b.args, reason + 'args mismatch');
        }
    };

    this.assertKssParmEquals = function(a, b, reason) {
        if (typeof(reason) == 'undefined') {
            reason = '';
        } else {
            reason += ', ';
        }
        for (var key in a) {
            this.assertNotEquals(typeof(b[key]), 'undefined', reason + 'key ' + key + ' missing from parms 2');
            this.assertKssParmValueEquals(a[key], b[key], 'mismatch at parm key ' + key);
        }
        for (var key in b) {
            this.assertNotEquals(typeof(a[key]), 'undefined', reason + 'key ' + key + ' missing from parms 1');
            this.assertKssParmValueEquals(a[key], b[key], reason + 'mismatch at parm key ' + key);
        }
    };
};

kukit.KssParserTestCaseBase.prototype = new kukit.TokenizerTestCaseBase;

kukit.KssParserTestCase = function() {
    this.name = 'kukit.KssParserTestCase';
 
    this.testPropValue = function() {
        // Parsing property values 

        var txt= "b";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.PropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.value.isMethod, false);
        this.assertEquals(parser.value.txt, 'b');

        // XXX multiword in PropValue was supported by the token
        // previously, but it really was never used.

        // multiword is not allowed.
        txt= "b   c";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.PropValue, cursor, null, true,
            'Wrong value : unallowed characters [c] after the argument.')

        // multiword is not allowed.
        txt= "  apples and   oranges   ;";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.PropValue, cursor, null, true,
            'Wrong value : unallowed characters [and] after the argument.')

        // multiword is not allowed.
        txt= " /* comments; */ apples and  /* more comments and*/ oranges   ;";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.PropValue, cursor, null, true,
            'Wrong value : unallowed characters [and] after the argument.')
 
        // params ok
        txt= "formVar(x, y) ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.PropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.value.isMethod, true);
        this.assertEquals(parser.value.methodName, 'formVar');
        this.assertListEquals(parser.value.args, ['x', 'y']);

        // params ok
        txt= "formVar(x, y)";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.PropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.value.isMethod, true);
        this.assertEquals(parser.value.methodName, 'formVar');
        this.assertListEquals(parser.value.args, ['x', 'y']);

        //ok
        txt= "   formVar   (x, y)";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.PropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.value.isMethod, true);
        this.assertEquals(parser.value.methodName, 'formVar');
        this.assertListEquals(parser.value.args, ['x', 'y']);

        txt= " a formVar(x, y)";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.PropValue, cursor, null, true,
            'Wrong value : unallowed characters [formVar] after the argument.')

        txt= " 'formVar'(x, y)";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.PropValue, cursor, null, true,
            'Wrong value : unallowed characters [(] after the argument.')

        txt= "formVar(x, y) xxx";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.PropValue, cursor, null, true,
            'Wrong value : unallowed characters [xxx] after the argument.')
    };

    this.testPropValueNoParam = function() {
        // no parameters ok in a provider.
        var txt= "formVar()";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.PropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.value.isMethod, true);
        this.assertEquals(parser.value.methodName, 'formVar');
        this.assertListEquals(parser.value.args, []);
    };

    this.testPropValueNoMethodName = function() {
        var txt= " (x, y)";
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.PropValue, cursor, null, true,
            'Wrong value : empty method name.');
    };
 
    this.testMultiPropValueSingleWord = function() {
        // Multi prop value with single word
        var txt= "b";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 1);
        this.assertEquals(parser.values[0].isMethod, false);
        this.assertEquals(parser.values[0].txt, 'b');
    };

    this.testMultiPropValueMultiWord = function() {
        // Multi prop value with multi word.
        var txt= "b   c";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 2);
        this.assertEquals(parser.values[0].isMethod, false);
        this.assertEquals(parser.values[0].txt, 'b');
        this.assertEquals(parser.values[1].isMethod, false);
        this.assertEquals(parser.values[1].txt, 'c');
    };

    this.testMultiPropValueMultiWord2 = function() {
        // Multi prop value with multi word.
        var txt= "  apples and   oranges   ;";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, false);
        this.assertEquals(parser.values[0].txt, 'apples');
        this.assertEquals(parser.values[1].isMethod, false);
        this.assertEquals(parser.values[1].txt, 'and');
        this.assertEquals(parser.values[2].isMethod, false);
        this.assertEquals(parser.values[2].txt, 'oranges');
    };

    this.testMultiPropValueMultiWord2 = function() {
        // Multi prop value with multi word and comments.
        var txt= " /* comments; */ apples and  /* more comments and*/ oranges   ;";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, false);
        this.assertEquals(parser.values[0].txt, 'apples');
        this.assertEquals(parser.values[1].isMethod, false);
        this.assertEquals(parser.values[1].txt, 'and');
        this.assertEquals(parser.values[2].isMethod, false);
        this.assertEquals(parser.values[2].txt, 'oranges');
    };


    this.testMultiPropValueStringAndWord = function() {
        // Multi prop value with string and word.
        var txt= "'apples' and oranges;";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, false);
        this.assertEquals(parser.values[0].txt, 'apples');
        this.assertEquals(parser.values[1].isMethod, false);
        this.assertEquals(parser.values[1].txt, 'and');
        this.assertEquals(parser.values[2].isMethod, false);
        this.assertEquals(parser.values[2].txt, 'oranges');
    };

    this.testMultiPropValueWordAndString = function() {
        // Multi prop value with string and word.
        var txt= "'apples' and oranges;";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, false);
        this.assertEquals(parser.values[0].txt, 'apples');
        this.assertEquals(parser.values[1].isMethod, false);
        this.assertEquals(parser.values[1].txt, 'and');
        this.assertEquals(parser.values[2].isMethod, false);
        this.assertEquals(parser.values[2].txt, 'oranges');
    };

    this.testMultiPropValueWordAndProvider = function() {
        // Multi prop value with word and provider and word.
        var txt= "apples formVar(x, y) oranges;";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, false);
        this.assertEquals(parser.values[0].txt, 'apples');
        this.assertEquals(parser.values[1].isMethod, true);
        this.assertEquals(parser.values[1].methodName, 'formVar');
        this.assertListEquals(parser.values[1].args, ['x', 'y']);
        this.assertEquals(parser.values[2].isMethod, false);
        this.assertEquals(parser.values[2].txt, 'oranges');
    };

    this.testMultiPropValueProviderAndWord = function() {
        // Multi prop value with provider and word.
        var txt= "formVar(x, y) and oranges;";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, true);
        this.assertEquals(parser.values[0].methodName, 'formVar');
        this.assertListEquals(parser.values[0].args, ['x', 'y']);
        this.assertEquals(parser.values[1].isMethod, false);
        this.assertEquals(parser.values[1].txt, 'and');
        this.assertEquals(parser.values[2].isMethod, false);
        this.assertEquals(parser.values[2].txt, 'oranges');
    };

    this.testMultiPropValueMethodArgsWithSpace = function() {
        // Multi prop value with space after the provider name.
        var txt= "formVar   (x, y) and oranges;";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, true);
        this.assertEquals(parser.values[0].methodName, 'formVar');
        this.assertListEquals(parser.values[0].args, ['x', 'y']);
        this.assertEquals(parser.values[1].isMethod, false);
        this.assertEquals(parser.values[1].txt, 'and');
        this.assertEquals(parser.values[2].isMethod, false);
        this.assertEquals(parser.values[2].txt, 'oranges');
    };

    this.testMultiPropValueManyProviders = function() {
        // Multi prop value with many providers
        var txt= "formVar(x, y) kssAttr(foo, true) formVar(a, b);";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, true);
        this.assertEquals(parser.values[0].methodName, 'formVar');
        this.assertListEquals(parser.values[0].args, ['x', 'y']);
        this.assertEquals(parser.values[1].isMethod, true);
        this.assertEquals(parser.values[1].methodName, 'kssAttr');
        this.assertListEquals(parser.values[1].args, ['foo', 'true']);
        this.assertEquals(parser.values[2].isMethod, true);
        this.assertEquals(parser.values[2].methodName, 'formVar');
        this.assertListEquals(parser.values[2].args, ['a', 'b']);
    };

    this.testMultiPropValueStringAndManyProviders = function() {
        // Multi prop value with a string and many providers
        var txt= "blah kssAttr(foo, true) formVar(a, b);";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MultiPropValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.values.length, 3);
        this.assertEquals(parser.values[0].isMethod, false);
        this.assertEquals(parser.values[0].txt, 'blah');
        this.assertEquals(parser.values[1].isMethod, true);
        this.assertEquals(parser.values[1].methodName, 'kssAttr');
        this.assertListEquals(parser.values[1].args, ['foo', 'true']);
        this.assertEquals(parser.values[2].isMethod, true);
        this.assertEquals(parser.values[2].methodName, 'formVar');
        this.assertListEquals(parser.values[2].args, ['a', 'b']);
    };

    this.testEventValueSimple = function() {
        // Parsing event value
        var txt= "b";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.EventValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.value.methodName, 'b');
    };

    this.testEventValueMultiword = function() {
        // multiword ok but does not finish
        var txt= "b   c";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.EventValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(cursor.pos, 1);
        this.assertEquals(parser.value.methodName, 'b');
    };

    this.testEventValueStartsWithSpace = function() {
        // space ok but does not finish
        var txt= " b";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.EventValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(cursor.pos, 0);
        this.assertEquals(parser.value.methodName, '');
    };

    this.testEventValueWithComment = function() {
        // ok, does not finish
        var txt= "apples/* more comments and*/";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.EventValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(cursor.pos, 6);
        this.assertEquals(parser.value.methodName, 'apples');
    };

    this.testEventValueWithBinderId = function() {
        // params ok
        var txt= "click(x)";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.EventValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.value.methodName, 'click');
        this.assertEquals(parser.value.arg.isMethod, false);
        this.assertEquals(parser.value.arg.txt, 'x');

        // more then 1 args not ok (but we check it only from kss selector)
        //txt= "drag(x, y)";
        //cursor = new kukit.tk.Cursor(txt);

        // not ok but we don't parse an error
        //txt= "'drag'(x)";
        //cursor = new kukit.tk.Cursor(txt);
        //this.assertParsingError(kukit.kssp.EventValue, cursor, null, true,
        //    'Excess characters after the property value', 16);
    };

    this.testEventValueWithValueProvider = function() {
        // methods ok
        var txt= "click(kssAttr(x))";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.EventValue(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.value.methodName, 'click');
        this.assertEquals(parser.value.arg.isMethod, true);
        this.assertEquals(parser.value.arg.methodName, 'kssAttr');
        this.assertListEquals(parser.value.arg.args, ['x']);
    };

    this.testEventValueWithValueProviderRejectsAccessValues = function() {
        // no more values in the method
        var txt= "click(kssAttr(x), aaa)";
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.EventValue, cursor, null, true,
            'Wrong event selector : [,] is not expected before the closing parenthesis. :<EVENTNAME>(<ID>) can have only one parameter.', 000);

        // XXX add more failing cases, maybe?
    };

    this.testMethodArgs = function() {
        // Parsing method args
        var txt= "(a, b)";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MethodArgs(cursor, kukit.kssp.openParent, true);
        this.assertEquals(parser.finished, true);
        this.assertListEquals(parser.args, ['a', 'b']);
    
        txt= "('a',  /* to annoy you */ \"b\")";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.MethodArgs(cursor, kukit.kssp.openParent, true);
        this.assertEquals(parser.finished, true);
        this.assertListEquals(parser.args, ['a', 'b']);

        txt= "(' a    multi', /* to annoy you */ \"b    multi \")";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.MethodArgs(cursor, kukit.kssp.openParent, true);
        this.assertEquals(parser.finished, true);
        this.assertListEquals(parser.args, [' a    multi','b    multi ']);

        txt= "('a', /*comment*/  /* to annoy you */ \"b\")";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.MethodArgs(cursor, kukit.kssp.openParent, true);
        this.assertEquals(parser.finished, true);
        this.assertListEquals(parser.args, ['a', 'b']);

        txt= "(a, b, )";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.MethodArgs(cursor, kukit.kssp.openParent, true);
        this.assertEquals(parser.finished, true);
        this.assertListEquals(parser.args, ['a', 'b']);

        txt= "(a, b c )";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.MethodArgs, cursor, kukit.kssp.openParent, true,
            'Wrong method argument [b c] : value cannot have spaces', 9);

        txt= "(a, b 'x' )";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.MethodArgs, cursor, kukit.kssp.openParent, true,
            'Unexpected token : [string] found, [comma] was expected.', 11);

    };

    this.testMethodArgsNoParam = function() {
        // Parsing method args with no parameters
        txt= "()";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.MethodArgs(cursor, kukit.kssp.openParent, true);
        this.assertEquals(parser.finished, true);
        this.assertListEquals(parser.args, []);
    };

    this.testMethodArgsRecursive = function() {
        var txt= "(a, b(c, d))";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.MethodArgs(cursor, kukit.kssp.openParent, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.args.length, 2);
        this.assertEquals(parser.args[0], 'a');
        this.assertEquals(parser.args[1].isMethod, true);
        this.assertEquals(parser.args[1].methodName, 'b');
        this.assertListEquals(parser.args[1].args, ['c', 'd']);
    };

    this.testEmptyDoc = function() {
        // unexpected eof handling 

        var txt= "";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.eventRules.length, 0);

        // In particular, this should not raise unexpected eof.
        var txt= "/*xxx*/";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.eventRules.length, 0);
    };

    this.testFull = function() {
        // Basic parsing test
        var txt= ""
            +"/* a long\n"
            +"** comment\n"
            +"*/\n"
            +"\n"
            +"#calendar-previous a:click {\n"
            +"   action-server : kukitresponse/kukitGetPreviousMonth;\n"
            +"}\n"
            +"div#update-area:timeout {\n"
            +"   evt-timeout-delay: 2000; \n"
            +"   action-server: getCurrentTime;\n"
            +"   getCurrentTime-effect: fade; \n"
            +"}\n"
            +"#calendar-previous a:click {\n"
            +"   action-server: 'kukitresponse/kukitGetPreviousMonth' /* place comment here*/;\n"
            +"}\n"
            +"#calendar-previous a:click {\n"
            +"   action-server : kukitGetPreviousMonth /* place comment here*/;\n"
            +"   kukitGetPreviousMonth-member: formVar(edit, 'f_member');\n"
            +"}\n"
            +"#calendar-previous a:dnd-drag(shelve) {\n"
            +"   action-server : whatever\n"
            +"}\n"
            +"#button-one:dnd-drag(annoy-me) {\n"
            +"   action-server:     clickedButton;\n"
            +"   clickedButton-id:  nodeAttr(id);\n"
            +"}\n"
            +"document:dnd-drag(annoyMe) {\n"
            +"   action-client:    alert;\n"
            +'   alert-message:    "You are an idiot! Ha ha ha. (But just keep on trying...)";\n'
            +"}\n"
            +"document:dnd-drag(annoyMe) {\n"
            +"   action-client:    alert;\n"
            +'   alert-message:       "You are an idiot! Ha ha ha. (But just keep on trying...)";\n'
            +"}\n"
            +"div#update-area:timeout {\n"
            +"   evt-timeout-delay: 2000; \n"
            +"   action-server: getCurrentTime;\n"
            +"   getCurrentTime-effect: fade; \n"
            +"   action-client:    log;\n"
            +'   log-message:    "Logging";\n'
            +"}\n"
            +"document:dnd-drag(annoyMe) {\n"
            +"   evt-dnd-drag-preventdefault:   true;\n"
            +"   action-client:    namespaced-alert;\n"
            +'   namespaced-alert-message:       "You are an idiot! Ha ha ha. (But just keep on trying...)";\n'
            +'}\n'
            +'#button_1:click {\n'
            +'action-client: setStyle;\n'
            +'setStyle-kssSelector: htmlid(button_2);\n'
            +'setStyle-name: backgroundColor;\n'
            +'setStyle-value: #FFa0a0;\n'
            +'}\n'
            +'#button_3:click {\n'
            +'action-client: setStyle;\n'
            +'setStyle-kssSelector: "#button_4";\n'
            +'setStyle-name: /* comment blabla */ backgroundColor;\n'
            +'setStyle-value: #FFa0a0;\n'
            +'}\n'
            +"#calendar-previous a:click {\n"
            +"   action-server : kukitGetPreviousMonth /* place comment here*/;\n"
            +"   kukitGetPreviousMonth-member: formVar(edit, kssAttr(foo));\n"
            +'}\n'
            +"#button-one:click(kssAttr(widannoy)) {\n"
            +"   action-client:     alert;\n"
            +"}\n";

        var cursor = new kukit.tk.Cursor(txt);

        // XXX TODO change comments
        
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.eventRules.length, 14);
        var rule;
        var action;

        // rule 0
            // #calendar-previous a:click {
            //   action-server : kukitresponse/kukitGetPreviousMonth;
            // }
        rule = parser.eventRules[0];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '#calendar-previous a');
        this.assertEquals(rule.kssSelector.name,  'click');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['kukitresponse/kukitGetPreviousMonth'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitresponse/kukitGetPreviousMonth');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {});

        // rule 1
            // div#update-area:timeout {
            //   evt-timeout-delay: 2000;
            //   effect: fade;
            //   action-server: getCurrentTime;
            // }
        rule = parser.eventRules[1];
        this.assertDictEquals(rule.parms, {'delay': '2000'});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  'div#update-area');
        this.assertEquals(rule.kssSelector.name,  'timeout');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['getCurrentTime'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'getCurrentTime');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
                'effect': new kukit.rd.KssTextValue('fade')
            });
        
        // rule 2
            // #calendar-previous a:click {
            //   action-server : 'kukitresponse/kukitGetPreviousMonth' /* place comment here*/;
            // }
        rule = parser.eventRules[2];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.css,  '#calendar-previous a');
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.name,  'click');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['kukitresponse/kukitGetPreviousMonth'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitresponse/kukitGetPreviousMonth');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {});

        // rule 3
            // #calendar-previous a:click {
            //   action-server : 'kukitresponse/kukitGetPreviousMonth' /* place comment here*/;
            //   member: formVar(edit, 'f_member');
            // }
        rule = parser.eventRules[3];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.css,  '#calendar-previous a');
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.name,  'click');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['kukitGetPreviousMonth'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitGetPreviousMonth');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
                'member': new kukit.rd.KssMethodValue('formVar', ['edit', 'f_member'])
            });
         
        // rule 4
            // #calendar-previous a:dnd-drag(shelve) {
            //   action-server : whatever
            // }
        rule = parser.eventRules[4];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.css,  '#calendar-previous a');
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.name,  'drag');
        this.assertEquals(rule.kssSelector.namespace,  'dnd');
        this.assertEquals(rule.kssSelector.id,  'shelve');
        action = rule.actions.content['whatever'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'whatever');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
            });
 
        // rule 5
            //#button-one:dnd-drag(annoyMe) {
            //   action-server:     clickedButton;
            //   id:             nodeAttr(id);
            //}
        rule = parser.eventRules[5];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.css,  '#button-one');
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.name,  'drag');
        this.assertEquals(rule.kssSelector.namespace,  'dnd');
        this.assertEquals(rule.kssSelector.id,  'annoy-me');
        action = rule.actions.content['clickedButton'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'clickedButton');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
                'id': new kukit.rd.KssMethodValue('nodeAttr', ['id'])
            });

        // rule 6
            // document:dnd-drag(annoyMe) {
            //   action-client:    alert;
            //   message:       "You are an idiot! Ha ha ha. (But just keep on trying...)";
            //}
        rule = parser.eventRules[6];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.css, 'document');
        this.assertEquals(rule.kssSelector.isMethodSelector, true);
        this.assertEquals(rule.kssSelector.name, 'drag');
        this.assertEquals(rule.kssSelector.namespace, 'dnd');
        this.assertEquals(rule.kssSelector.id, 'annoyMe');
        action = rule.actions.content['alert'];
        this.assertEquals(action.type, 'C');
        this.assertEquals(action.name, 'alert');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
                'message': new kukit.rd.KssTextValue( "You are an idiot! Ha ha ha. (But just keep on trying...)")
            });

        // rule 7
            // document:dnd-drag(annoyMe) {
            //   action-client:    alert;
            //   message:       "You are an idiot! Ha ha ha. (But just keep on trying...)";
            //}
        rule = parser.eventRules[7];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.css, 'document');
        this.assertEquals(rule.kssSelector.isMethodSelector, true);
        this.assertEquals(rule.kssSelector.name, 'drag');
        this.assertEquals(rule.kssSelector.namespace, 'dnd');
        this.assertEquals(rule.kssSelector.id, 'annoyMe');
        action = rule.actions.content['alert'];
        this.assertEquals(action.type, 'C');
        this.assertEquals(action.name, 'alert');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
                'message': new kukit.rd.KssTextValue( "You are an idiot! Ha ha ha. (But just keep on trying...)")
            });

        // rule 8
        rule = parser.eventRules[8];
        this.assertDictEquals(rule.parms, {'delay': '2000'});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  'div#update-area');
        this.assertEquals(rule.kssSelector.name,  'timeout');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['getCurrentTime'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'getCurrentTime');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
                'effect': new kukit.rd.KssTextValue('fade')
            });
        action = rule.actions.content['log'];
        this.assertEquals(action.type, 'C');
        this.assertEquals(action.name, 'log');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
                'message': new kukit.rd.KssTextValue('Logging')
            });

        // rule 9
            //document:dnd-drag(annoyMe) {\n"
            //   evt-dnd-drag-preventdefault:   true;\n"
            //   action-client:    namespaced-alert;\n"
            //   namespaced-alert-message:       "You are an idiot! Ha ha ha. (But just keep on trying...)";\n'
            //}
        rule = parser.eventRules[9];
        this.assertDictEquals(rule.parms, {'preventdefault': 'true'});
        this.assertEquals(rule.kssSelector.css, 'document');
        this.assertEquals(rule.kssSelector.isMethodSelector, true);
        this.assertEquals(rule.kssSelector.name, 'drag');
        this.assertEquals(rule.kssSelector.namespace, 'dnd');
        this.assertEquals(rule.kssSelector.id, 'annoyMe');
        action = rule.actions.content['namespaced-alert'];
        this.assertEquals(action.type, 'C');
        this.assertEquals(action.name, 'namespaced-alert');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
                'message': new kukit.rd.KssTextValue( "You are an idiot! Ha ha ha. (But just keep on trying...)")
            });

        // rule 10
            //#button_1:click {
            //    action-client: setStyle;
            //    setStyle-kssSelector: htmlid(button_2);
            //    setStyle-name: backgroundColor;
            //    setStyle-value: #FFa0a0;
            //}
        rule = parser.eventRules[10];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '#button_1');
        this.assertEquals(rule.kssSelector.name,  'click');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['setStyle'];
        this.assertEquals(action.type, 'C');
        this.assertEquals(action.name, 'setStyle');
        this.assertEquals(action.error, null);
        // At this point the parms are before separation yet
        this.assertKssParmEquals(action.parms, {
                'name': new kukit.rd.KssTextValue('backgroundColor'),
                'value': new kukit.rd.KssTextValue('#FFa0a0'),
                'kssSelector': new kukit.rd.KssMethodValue('htmlid', ['button_2'])
            });

        // rule 11
            //#button_3:click {
            //    action-client: setStyle;
            //    setStyle-kssSelector: "#button_4";
            //    setStyle-name: backgroundColor;
            //    setStyle-value: #FFa0a0;
            //}\n";
        rule = parser.eventRules[11];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '#button_3');
        this.assertEquals(rule.kssSelector.name,  'click');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['setStyle'];
        this.assertEquals(action.type, 'C');
        this.assertEquals(action.name, 'setStyle');
        this.assertEquals(action.error, null);
        // At this point the parms are before separation yet
        this.assertKssParmEquals(action.parms, {
                'name': new kukit.rd.KssTextValue('backgroundColor'),
                'value': new kukit.rd.KssTextValue('#FFa0a0'),
                'kssSelector': new kukit.rd.KssTextValue('#button_4')
            });

        // rule 12
            // #calendar-previous a:click {
            //   kss-action : 'kukitresponse/kukitGetPreviousMonth' /* place comment here*/;
            //   member: formVar(edit, kssAttr(foo));
            // }
        rule = parser.eventRules[12];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.css,  '#calendar-previous a');
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.name,  'click');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['kukitGetPreviousMonth'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitGetPreviousMonth');
        this.assertEquals(action.error, null);
        var formVar = action.parms.member;
        this.assertEquals(formVar.methodName, 'formVar');
        this.assertEquals(formVar.args[0], 'edit');
        var kssAttr = formVar.args[1];
        this.assertEquals(kssAttr.methodName, 'kssAttr');
        this.assertListEquals(kssAttr.args, ['foo']);

        // rule 13
            // #button-one:click(kssAttr(widannoy)) {\n"
            //   action-client:    alert;
            //}
        rule = parser.eventRules[13];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.css, '#button-one');
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.name, 'click');
        this.assertEquals(rule.kssSelector.namespace, null);
        this.assertEquals(rule.kssSelector.id, null);
        this.assertEquals(rule.kssSelector.ppid.methodName, 'kssAttr');
        this.assertListEquals(rule.kssSelector.ppid.args, ['widannoy']);
        action = rule.actions.content['alert'];
        this.assertEquals(action.type, 'C');
        this.assertEquals(action.name, 'alert');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {
            });

    };
    
    this.testActionErrorParameters = function() {

        var txt= ""
            +"/* a long\n"
            +"** comment\n"
            +"*/\n"
            +"\n"
            +".inlineEditable:blur{ \n"
            +"   action-server : kukitresponse;\n"
            +"   kukitresponse-error : errors;\n"
            +"}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.eventRules.length, 1);
        var rule;
        var action;

        rule = parser.eventRules[0];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '.inlineEditable');
        this.assertEquals(rule.kssSelector.name,  'blur');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['kukitresponse'];
        this.assertEquals((typeof(action) != 'undefined'), true);
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitresponse');
        this.assertEquals(action.error, 'errors');
        this.assertKssParmEquals(action.parms, {});
    };
    
    this.testDefaultActionErrorParameters = function() {

        return;

        // XXX
        // default actions can be tested from plugins only currently
        var txt= ""
            +"/* a long\n"
            +"** comment\n"
            +"*/\n"
            +"\n"
            +".inlineEditable:blur{ \n"
            +"   default-error : errors;\n"
            +"}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.eventRules.length, 1);
        var rule;
        var action;

        rule = parser.eventRules[0];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '.inlineEditable');
        this.assertEquals(rule.kssSelector.name,  'blur');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['default'];
        this.assertEquals((typeof(action) != 'undefined'), true);
        this.assertEquals(action.error, 'errors');
        this.assertKssParmEquals(action.parms, {});
    };
};

kukit.KssParserTestCase.prototype = new kukit.KssParserTestCaseBase;

kukit.KssParserValueProvidersCheckTestCase = function() {
    this.name = 'kukit.KssParserValueProvidersCheckTestCase';
    // Different tests to see if the syntax type check of
    // the value providers is working correctly.
    // At the moment we have the following return value types:
    //
    //   string:     almost all normal providers return string
    //   selection:  a selector provider returns a list of nodes
    //   formquery:   a form provider returns an ordered list
    //               of key-value pairs to be marshalled
    //   url:        the return type of the url() provider
    //
    // We do not check the actual evaluation here, as we
    // have no DOM at hand.
    //
    // We also check how these providers can be combined
    // on one line.
    //
    // This testcase can run in DEVELOPMENT MODE ONLY,
    // (because the checks are ignored in production mode)
    // and all tests will be skipped
    // and pass GREEN in production mode.
    
    this.testNormalProviderAcceptsString = function() {
        // normal providers does accept string
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "nodeAttr('id')";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.PropValue(cursor, null, true);
        var value = parser.value;
        value.check();
    };

    this.testNormalProviderRejectsSelectionAsParameter = function() {
        // normal providers does not accept selection
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "nodeAttr(htmlid('id'))";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.PropValue(cursor, null, true);
        var value = parser.value;
        this.assertThrows(function() {
            value.check();
            },
            Error);
    };
 
    this.testNormalProviderRejectsSelectionFullRule = function() {
        // normal providers do not accept selection
        // full rule
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client: log;\n"
               + "    log-message:   nodeAttr(htmlid('id'));\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Error in value for action parameter [message] : Error: Expected string value and got [selection] in argument #[1] of provider [nodeAttr].., at row 1, column 11');
    };

    this.testNormalProviderRejectsFormData = function() {
        // normal providers do not accept form query
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "nodeAttr(form('name'))";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.PropValue(cursor, null, true);
        var value = parser.value;
        this.assertThrows(function() {
            value.check();
            },
            Error);
    };
 
    this.testNormalProviderRejectsFormDataFullRule = function() {
        // normal providers do not accept form query
        // full rule
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client: log;\n"
               + "    log-message:   nodeAttr(form('name'));\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Error in value for action parameter [message] : Error: Expected string value and got [formquery] in argument #[1] of provider [nodeAttr].., at row 1, column 11');
    };

    this.testNormalParameterRejectsSelectorInItself = function() {
        // normal parameters do not accept selector (in itself)
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client: log;\n"
               + "    log-message:   htmlid('id');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [selection] not allowed in the action parameter [message]., at row 1, column 11');
    };

    this.testNormalParameterRejectsFormData = function() {
        // normal parameters do not accept form query
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client: log;\n"
               + "    log-message:   form('name');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [formquery] not allowed in the action parameter [message]., at row 1, column 1');
    };

    this.testKssSelectorAcceptsSelector = function() {
        // kssSelector accepts selector
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client:              setAttribute;\n"
               + "    setAttribute-kssSelector:   htmlid('id');\n"
               + "    setAttribute-name:          name;\n"
               + "    setAttribute-value:          value;\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testKssSelectorAcceptsString = function() {
        // kssSelector accepts string
        // (it will evaluate as css(xxx), but we can't check that without a dom)
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client:              setAttribute;\n"
               + "    setAttribute-kssSelector:   htmlid('id');\n"
               + "    setAttribute-name:          name;\n"
               + "    setAttribute-value:          value;\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testKssSelectorRejectsFormData = function() {
        // kssSelector rejects form query
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client:              setAttribute;\n"
               + "    setAttribute-kssSelector:   form('name');\n"
               + "    setAttribute-name:          name;\n"
               + "    setAttribute-value:          value;\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [formquery] not allowed in the kss action parameter [kssSelector]., at row 1, column 11');
    };

    this.testKssSubmitFormAcceptsFormData = function() {
        // kssSubmitForm accepts form query
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:              doIt;\n"
               + "    doIt-kssSubmitForm:         form('name');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testKssSubmitFormAcceptsString = function() {
        // kssSubmitForm accepts string
        // (it will evaluate as form(xxx), but we can't check that without a dom)
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:              doIt;\n"
               + "    doIt-kssSubmitForm:         'name';\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testKssSubmitFormRejectsSelection = function() {
        // kssSubmitForm rejects selection
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:              doIt;\n"
               + "    doIt-kssSubmitForm:         htmlid('id');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [selection] not allowed in the kss action parameter [kssSubmitForm]., at row 1, column 11');
    };

    this.testCombinedClientAction = function() {
        // Client action accepts a list of combined providers.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client:   htmlid(id) doIt;\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testCombinedClientActionRejectsFormData = function() {
        // Client action rejects form query.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client:   htmlid(id) doIt form();\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Error in value for action definition [action-client] : Error: form method needs 1 arguments (formname)., at row 1, column 11');
    };

    this.testCombinedServerAction = function() {
        // Server action accepts a list of combined providers.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   doIt currentForm();\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testCombinedServerActionRejectsSelector = function() {
        // Server action rejects a selection provider.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   doIt currentForm() htmlid(id);\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [selection] not allowed in the action definition [action-server]., at row 1, column 11');
    };

    this.testCombinedServerActionAcceptsStringAndUrl = function() {
        // Server action accepts a string and an url.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   doIt url('http://foo.bar');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testCombinedServerActionAcceptsUrlAndString = function() {
        // Server action accepts a string and an url.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   doIt url('http://foo.bar');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testCombinedServerActionAcceptsStringAndFormAndUrl = function() {
        // Server action accepts string, form, and url providers together.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   doIt currentForm() url('http://foo.bar');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testCombinedServerActionRejectsUrlInItself = function() {
        // Server action rejects url() in itself.
        // It should have a string in any case.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   url('http://foo.bar');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Missing [string] value in the action definition [action-server]., at row 1, column 11');
    };

    this.testCombinedServerActionRejectsTwoStrings = function() {
        // Server action rejects two strings.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   foo 'bar';\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Only one [string] value is allowed in the action definition [action-server]., at row 1, column 11');
    };


    this.testCombinedServerActionRejectsUrlWithoutParms = function() {
        // Server action rejects url() if url has no parameter.
        // It should have a string in any case.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   doIt url();\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Error in value for action definition [action-server] : Error: url() needs 1 argument., at row 1, column 11');
    };

    this.testServerActionRejectsValueProviderForString = function() {
        // Server action must have a string, no value provider is allowed here.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   kssAttr(blah);\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Wrong value for key [action-server] : value providers are not allowed for action-<QUALIFIER> keys., at row 1, column 11');
    };

    this.testNormalProviderRejectsValueAndSelector = function() {
        // normal parameters rejects value and selector
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client: log;\n"
               + "    log-message:   kssAttr(blah) htmlid('id');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [selection] not allowed in the action parameter [message]., at row 1, column 11'); 
    };


    this.testNormalProviderRejectsSelectorAndString = function() {
        // normal parameters accepts selector and string
        // although this does not make much sense... but it's allowed.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client: log;\n"
               + "    log-message:   htmlid('id') 'message';\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [selection] not allowed in the action parameter [message]., at row 1, column 11') 
    };

    this.testNormalProviderRejectsSelector = function() {
        // normal parameters accepts value and selector
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client: log;\n"
               + "    log-message:   htmlid('id');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [selection] not allowed in the action parameter [message]., at row 1, column 11') 
    };

    this.testAliasedClientAction = function() {
        // Client action can be aliased.
        //
        // This test can only run in development mode, pass otherwise.
        // Note that merging the rules is not really tested from here,
        // as we don't have DOM. So we can't really see if the alias
        // is working, only that it is parsed well.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client:   doIt alias(doAlias);\n"
               + "    doAlias-foo:     bar;\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
    };

    this.testServerActionRejectsAlias = function() {
        // Server action rejects alias().
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-server:   doIt alias(doAlias);\n"
               + "    doAlias-foo:     bar;\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [alias] not allowed in the action definition [action-server]., at row 1, column 11');
    };

    this.testNormalParameterRejectsAlias = function() {
        // normal parameters do not accept alias.
        //
        // This test can only run in development mode, pass otherwise.
        if (! kukit.isDevelMode) {return;}
        //
        var txt= "#id:click {\n"
               + "    action-client: log;\n"
               + "    log-message:   whatever alias('name');\n"
               + "}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
            // XXX This error message will be fixed in service-layer branch
            // XXX This will also fix running from IE, currently broken at error assert.
            'Provider result type [alias] not allowed in the action parameter [message]., at row 1, column 11');
    };

}; 

kukit.KssParserValueProvidersCheckTestCase.prototype = new kukit.KssParserTestCaseBase;


kukit.KssParserSelectorTestCase = function() {
    this.name = 'kukit.KssParserSelectorTestCase';

    this.testSelectorWithBinderId = function() {
        // Parsing event selector params
        var txt= "a:dnd-drag(hello)";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, 'a');
        this.assertEquals(parser.kssSelector.name, 'drag');
        this.assertEquals(parser.kssSelector.namespace, 'dnd');
        this.assertEquals(parser.kssSelector.id, 'hello');
    };
    
    this.testKssSelector = function() {
        var txt= "a:dnd-drag(hello)";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, 'a');
        this.assertEquals(parser.kssSelector.name, 'drag');
        this.assertEquals(parser.kssSelector.namespace, 'dnd');
        this.assertEquals(parser.kssSelector.id, 'hello');

        var txt= "a:dnd-drag-toomuch(hello)";
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector [dnd-drag-toomuch] : qualifier should be :<EVENTNAME> or :<NAMESPACE>' 
            , 25);

        // maybe in std css space is not allowed in the parents,
        // but we tolerate it
        txt= "  a div#id:dnd-drag( hello)";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, '  a div#id');
        this.assertEquals(parser.kssSelector.name, 'drag');
        this.assertEquals(parser.kssSelector.namespace, 'dnd');
        this.assertEquals(parser.kssSelector.id, 'hello');

        // We do not allow space here 
        txt= "  a div#id:dnd-drag   (hello)";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 25);

        // We do not allow space here
        txt= "  a div#id: dnd-drag(hello)";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 23);

        txt= "a div#id:click ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, 'a div#id');
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);

        txt= "a div.class:click ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, 'a div.class');
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);

        txt= "a:click ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, 'a');
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);

        // two params: not allowed
        txt= "a:click('hello', bello)";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : [,] is not expected before the closing parenthesis. :<EVENTNAME>(<ID>) can have only one parameter.', 22);

        // zero params: not std css but tolerated 
        txt= "a:click()";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 8);

        txt= "   (hello)";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 10);

        txt= "hello  ('bello')";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 16);

        txt= "a:lang(hu)  (hello)";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 19);

        txt= "a:lang(hu) b (hello)";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 20);

        // A valid attr selector in the css selector part.
        txt= "a[href=hello].class:lang(hu) div#id:click ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, "a[href=hello].class:lang(hu) div#id");
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);

        txt= "a[href=hello].class:lang(hu) div#id:click(hello) ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, "a[href=hello].class:lang(hu) div#id");
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);
        this.assertEquals(parser.kssSelector.id, 'hello');

        txt= "   a:lang(hu) click ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 20);

        // Spaces in the end
        // txt= "   a:lang(hu, uh) b:click    "; // XXX not supported
        txt= "   a:lang(hu-uh) b:click    ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, "   a:lang(hu-uh) b");
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);

        // Comment in the end
        txt= "   a:lang(hu-uh) b:click/*comment here*/";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, "   a:lang(hu-uh) b");
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);

        // Should be ok.
        txt= "a:lang(hu)/*comment here*/b:click ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, "a:lang(hu)/*comment here*/b");
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);
  
        // Should be ok.
        txt= "a:lang(hu) click/*comment here*/b:load ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, "a:lang(hu) click/*comment here*/b");
        this.assertEquals(parser.kssSelector.name, 'load');
        this.assertEquals(parser.kssSelector.namespace, null);

        txt= "a:click:clack ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 14);

        txt= "a:click    :clack ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : space before the colon.', 18);

        txt= "a:click/*comment */:clack ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 26);

        txt= "click/*comment here*/:clack ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 28);

        txt= "/*comment here*/div:click ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);

        txt= " no-document:click(hello)";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, " no-document");
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);
        this.assertEquals(parser.kssSelector.id, "hello");

            
        // Event method selectors

        txt= " document:click(hello)  ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isMethodSelector, true);
        this.assertEquals(parser.kssSelector.css, 'document');
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);
        this.assertEquals(parser.kssSelector.id, 'hello');

        txt= " document:dnd-drag(hello)  ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isMethodSelector, true);
        this.assertEquals(parser.kssSelector.css, 'document');
        this.assertEquals(parser.kssSelector.name, 'drag');
        this.assertEquals(parser.kssSelector.namespace, 'dnd');
        this.assertEquals(parser.kssSelector.id, 'hello');
 
        txt= "document";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : missing event qualifier :<EVENTNAME> or :<EVENTNAME>(<ID>).', 8);

        txt= "document: ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Wrong event selector : event name cannot have spaces.', 10);

        // also, "behaviour:" works
        txt= " behaviour:click(hello)  ";
        cursor = new kukit.tk.Cursor(txt);
        parser = new kukit.kssp.KssSelector(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isMethodSelector, true);
        this.assertEquals(parser.kssSelector.css, 'behaviour');
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);
        this.assertEquals(parser.kssSelector.id, 'hello');

    }
    
    this.testKssSelectorWithWrongEventWithoutNamespace = function() {
        txt= " document:clack ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Error : undefined global event [clack] (or maybe namespace is missing ?).');
        txt= " document:clack(hello) ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Error : undefined global event [clack] (or maybe namespace is missing ?).');
    }
    
    this.testKssSelectorWithRightEventAndMissingNamespace = function() {
        txt= " document:drag ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Error : undefined global event [drag] (or maybe namespace is missing ?).');
        txt= " document:drag(hello) ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Error : undefined global event [drag] (or maybe namespace is missing ?).');
    }
    
    this.testKssSelectorWithUndefinedNamespaceWhenNamespace = function() {
        txt= " document:dad-drag ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Error : undefined namespace or event in [dad-drag].');
        txt= " document:dad-drag(hello) ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Error : undefined namespace or event in [dad-drag].');
    }
    
    this.testKssSelectorWithUndefinedEventNameWhenNameSpace = function() {
        txt= " document:dnd-drog ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Error : undefined namespace or event in [dnd-drog].');
        txt= " document:dnd-drog(hello) ";
        cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, cursor, null, true,
            'Error : undefined namespace or event in [dnd-drog].');
    }

}; 

kukit.KssParserSelectorTestCase.prototype = new kukit.KssParserTestCaseBase;

kukit.KssParserSelectorsTestCase = function() {
    this.name = 'kukit.KssParserSelectorsTestCase';

    this.testSingleSelector = function() {
        var txt= "a:dnd-drag(hello)";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 1);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'a');
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
    };
    
    this.testMultipleSelectors = function() {
        var txt= "a:dnd-drag(hello), div a:click";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 2);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'a');
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
        var kssSelector = parser.selectors[1];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'div a');
        this.assertEquals(kssSelector.name, 'click');
        this.assertEquals(kssSelector.namespace, null);

    };

    this.testMultipleSelectorsWithComment = function() {
        var txt= "a:dnd-drag(hello), /* a comment */ div a:click";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 2);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'a');
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
        var kssSelector = parser.selectors[1];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'div a');
        this.assertEquals(kssSelector.name, 'click');
        this.assertEquals(kssSelector.namespace, null);
    };

    this.testSingleSelectorWithCommaInDoubleQuoteStringInSelector = function() {
        var txt = 'a[value="Hi, I am a comma"]:dnd-drag(hello)';
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 1);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'a[value="Hi, I am a comma"]');
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
    };

    this.testSingleSelectorWithCommaInSingleQuoteStringInSelector = function() {
        var txt = "a[value='Hi, I am a comma']:dnd-drag(hello)";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 1);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, "a[value='Hi, I am a comma']");
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
    };

    this.testMultipleSelectorsWithCommaInDoubleQuoteStringInSelector = function() {
        var txt = 'a[value="Hi, I am a comma"]:dnd-drag(hello), div a:click';
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 2);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'a[value="Hi, I am a comma"]');
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
        var kssSelector = parser.selectors[1];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'div a');
        this.assertEquals(kssSelector.name, 'click');
        this.assertEquals(kssSelector.namespace, null);
    };

    this.testMultipleSelectorsWithCommaInSingleQuoteStringInSelector = function() {
        var txt = "a[value='Hi, I am a comma']:dnd-drag(hello), div a:click";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 2);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, "a[value='Hi, I am a comma']");
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
        var kssSelector = parser.selectors[1];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'div a');
        this.assertEquals(kssSelector.name, 'click');
        this.assertEquals(kssSelector.namespace, null);
    };

    this.testMultipleSelectorsWithCommentAndNewline = function() {
        var txt= "a:dnd-drag(hello), /* a comment */ \n div a:click";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 2);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'a');
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
        var kssSelector = parser.selectors[1];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'div a');
        this.assertEquals(kssSelector.name, 'click');
        this.assertEquals(kssSelector.namespace, null);
    };

    this.testMultipleSelectorsWithNewline = function() {
        var txt= "a:dnd-drag(hello), \n div a:click";
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelectors(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.selectors.length, 2);
        var kssSelector = parser.selectors[0];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'a');
        this.assertEquals(kssSelector.name, 'drag');
        this.assertEquals(kssSelector.namespace, 'dnd');
        this.assertEquals(kssSelector.id, 'hello');
        var kssSelector = parser.selectors[1];
        this.assertEquals(kssSelector.isEventSelector, true);
        this.assertEquals(kssSelector.css, 'div a');
        this.assertEquals(kssSelector.name, 'click');
        this.assertEquals(kssSelector.namespace, null);
    };

    this.testSingleSelectorWithFirstComma = function() {
        var txt= ",a:dnd-drag(hello),";
        var cursor = new kukit.tk.Cursor(txt);
        var msg = 'Wrong event selector : missing event';
        this.assertParsingError(kukit.kssp.KssSelectors, cursor, null, true,
            msg, 1);
    }

    this.testSingleSelectorWithMiddleComma = function() {
        var txt= "a:dnd-drag(hello),,p:click";
        var cursor = new kukit.tk.Cursor(txt);
        var msg = 'Wrong event selector : missing event';
        this.assertParsingError(kukit.kssp.KssSelectors, cursor, null, true,
            msg, 1);
    }

    this.testSingleSelectorWithAdditionalComma = function() {
        var txt= "a:dnd-drag(hello),";
        var cursor = new kukit.tk.Cursor(txt);
        var msg = 'Wrong event selector : trailing comma';
        this.assertParsingError(kukit.kssp.KssSelectors, cursor, null, true,
            msg, 1);
    }

    this.testSingleSelectorWithAdditionalCommas = function() {
        var txt= "a:dnd-drag(hello),,";
        var cursor = new kukit.tk.Cursor(txt);
        var msg = 'Wrong event selector : missing event';
        this.assertParsingError(kukit.kssp.KssSelectors, cursor, null, true,
            msg, 1);
    }

    this.testEventRulesWithMultipleSelectors = function() {
        var txt= ""
            +"/* a long\n"
            +"** comment\n"
            +"*/\n"
            +"\n"
            +"#calendar-previous a:click,\n"
            +".inlineEditable:blur{ \n"
            +"   action-server : kukitresponse/kukitGetPreviousMonth;\n"
            +"}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.eventRules.length, 2);
        var rule;
        var action;

        rule = parser.eventRules[0];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '#calendar-previous a');
        this.assertEquals(rule.kssSelector.name,  'click');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['kukitresponse/kukitGetPreviousMonth'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitresponse/kukitGetPreviousMonth');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {});

        rule = parser.eventRules[1];
        this.assertDictEquals(rule.parms, {});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '.inlineEditable');
        this.assertEquals(rule.kssSelector.name,  'blur');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['kukitresponse/kukitGetPreviousMonth'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitresponse/kukitGetPreviousMonth');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {});
    }

    this.testEventParameters = function() {
        var txt= ""
            +"/* a long\n"
            +"** comment\n"
            +"*/\n"
            +"\n"
            +"#calendar-previous a:click,\n"
            +".inlineEditable:keydown{ \n"
            +"   evt-click-allowbubbling: true;\n"
            +"   evt-keydown-keycode: 1;\n"
            +"   action-server : kukitresponse/kukitGetPreviousMonth;\n"
            +"}\n"
        var cursor = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.Document(cursor, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.eventRules.length, 2);
        var rule;
        var action;

        rule = parser.eventRules[0];
        this.assertDictEquals(rule.parms, {'allowbubbling': 'true'});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '#calendar-previous a');
        this.assertEquals(rule.kssSelector.name,  'click');
        this.assertEquals(rule.kssSelector.namespace,  null);
        action = rule.actions.content['kukitresponse/kukitGetPreviousMonth'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitresponse/kukitGetPreviousMonth');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {});

        rule = parser.eventRules[1];
        this.assertDictEquals(rule.parms, {'keycode':'1'});
        this.assertEquals(rule.kssSelector.isEventSelector, true);
        this.assertEquals(rule.kssSelector.css,  '.inlineEditable');
        this.assertEquals(rule.kssSelector.name,  'keydown');
        this.assertEquals(rule.kssSelector.namespace,  null);

        action = rule.actions.content['kukitresponse/kukitGetPreviousMonth'];
        this.assertEquals(action.type, 'S');
        this.assertEquals(action.name, 'kukitresponse/kukitGetPreviousMonth');
        this.assertEquals(action.error, null);
        this.assertKssParmEquals(action.parms, {});
    }

    this.testEventParametersErrorWithoutNamespace = function() {
        var txt= ""
            +"/* a long\n"
            +"** comment\n"
            +"*/\n"
            +"\n"
            +"#calendar-previous a:click,\n"
            +".inlineEditable:keydown{ \n"
            +"   evt-click-allowbubbling: true;\n"
            +"   evt-blur-allowbubling: true;\n"
            +"   action-server : kukitresponse/kukitGetPreviousMonth;\n"
            +"}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
                                'Wrong value for evt-[<NAMESPACE>-]<EVENTNAME> [blur] : <NAMESPACE>-<EVENTNAME> should exist in the event of the selectors.', 6);
    }
    
    this.testEventParametersErrorWithNamespace = function() {
        var txt= ""
            +"/* a long\n"
            +"** comment\n"
            +"*/\n"
            +"\n"
            +"#calendar-previous a:click,\n"
            +".inlineEditable:keydown{ \n"
            +"   evt-click-allowbubbling: true;\n"
            +"   evt-dnd-drag-preventdefault:   true;\n"
            +"   action-server : kukitresponse/kukitGetPreviousMonth;\n"
            +"}\n"
        var cursor = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.Document, cursor, null, true,
                                'Wrong value for evt-[<NAMESPACE>-]<EVENTNAME> [dnd-drag] : <NAMESPACE>-<EVENTNAME> should exist in the event of the selectors.', 6);
    }

    this.testValueProvidersInEventIdentification = function() {
        // Param providers within the event identification

        var txt= "a:click(kssAttr(hello))";
        var src = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelector(src, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, 'a');
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);
        this.assertEquals(parser.kssSelector.id, null);
        this.assertEquals(parser.kssSelector.ppid.methodName, 'kssAttr');
        this.assertListEquals(parser.kssSelector.ppid.args, ['hello']);
    };

    this.testValueProvidersInEventIdentification2 = function() {
        var txt= "a:click(kssAttr(hello, true ))";
        var src = new kukit.tk.Cursor(txt);
        var parser = new kukit.kssp.KssSelector(src, null, true);
        this.assertEquals(parser.finished, true);
        this.assertEquals(parser.kssSelector.isEventSelector, true);
        this.assertEquals(parser.kssSelector.css, 'a');
        this.assertEquals(parser.kssSelector.name, 'click');
        this.assertEquals(parser.kssSelector.namespace, null);
        this.assertEquals(parser.kssSelector.id, null);
        this.assertEquals(parser.kssSelector.ppid.methodName, 'kssAttr');
        this.assertListEquals(parser.kssSelector.ppid.args, ['hello', 'true']);
    };

    this.testValueProvidersInEventIdentificationRejectsMoreParameters = function() {
        var txt= "a:drag(kssAttr(hello), xxx)";
        var src = new kukit.tk.Cursor(txt);
        this.assertParsingError(kukit.kssp.KssSelector, src, null, true,
            'Wrong event selector : [,] is not expected before the closing parenthesis. :<EVENTNAME>(<ID>) can have only one parameter.', 000);
    };

};

kukit.KssParserSelectorsTestCase.prototype = new kukit.KssParserTestCaseBase;

if (typeof(testcase_registry) != 'undefined') {
    testcase_registry.registerTestCase(kukit.KssParserTestCase,
                                       'kukit.KssParserTestCase');
    testcase_registry.registerTestCase(kukit.KssParserValueProvidersCheckTestCase,
                                       'kukit.KssParserValueProvidersCheckTestCase');
    testcase_registry.registerTestCase(kukit.KssParserSelectorTestCase,
                                       'kukit.KssParserSelectorTestCase');
    testcase_registry.registerTestCase(kukit.KssParserSelectorsTestCase,
                                       'kukit.KssParserSelectorsTestCase');
}
