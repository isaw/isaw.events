/* XXX This is totally out-of-date now, but
   we may want to do something like this later. */

function RuleParseTestCase() {
    this.name = 'RuleParseTestCase';
}

RuleParseTestCase.prototype = new TestCase;
Class = RuleParseTestCase.prototype;

Class.setUp = function() {
    this.preprocessor = new kukit.RuleProcessor(); 
    this.doc = new DOMParser();
};

Class.tearDown = function() {
};


Class.testOneRule = function() {
    input = '<?xml version="1.0"?><rules><rule selector="button.button"><event name="click">getDivContent</event></rule></rules>';
    var dom = this.doc.parseFromString(input, 'text/xml')
    this.preprocessor.parseRuleDom(dom);
    rules = this.preprocessor.rules;
    this.assertEquals(rules.length, 1);
    rule = rules[0];
    this.assertEquals(rule.selector, 'button.button');
    this.assertEquals(rule.property_type, 'event');
    this.assertEquals(rule.name, 'click');
    this.assertEquals(rule.action, 'getDivContent');
}

Class.testOneWrongSelector = function() {
    input = '<?xml version="1.0"?><rules><rule selector=""><event name="click">getDivContent</event></rule></rules>';
    var dom = this.doc.parseFromString(input, 'text/xml')
    this.preprocessor.parseRuleDom(dom);
    rules = this.preprocessor.rules;
    this.assertEquals(rules.length, 0);
}

Class.testOneWrongEvent = function() {
    input = '<?xml version="1.0"?><rules><rule selector="button"><event name="">getDivContent</event></rule></rules>';
    var dom = this.doc.parseFromString(input, 'text/xml')
    this.preprocessor.parseRuleDom(dom);
    rules = this.preprocessor.rules;
    this.assertEquals(rules.length, 0);
}

Class.testOneWrongAction = function() {
    input = '<?xml version="1.0"?><rules><rule selector="button"><event name="click"></event></rule></rules>';
    var dom = this.doc.parseFromString(input, 'text/xml')
    this.preprocessor.parseRuleDom(dom);
    rules = this.preprocessor.rules;
    this.assertEquals(rules.length, 0);
}

Class.testCorrectRules = function() {
    input = '<?xml version="1.0"?><rules><rule selector="button.button"><event name="click">getDivContent</event></rule><rule selector="button.second"><event name="click">Second</event></rule></rules>';
    var dom = this.doc.parseFromString(input, 'text/xml')
    this.preprocessor.parseRuleDom(dom);
    rules = this.preprocessor.rules;
    this.assertEquals(rules.length, 2);
    rule = rules[0];
    this.assertEquals(rule.selector, 'button.button');
    this.assertEquals(rule.property_type, 'event');
    this.assertEquals(rule.name, 'click');
    this.assertEquals(rule.action, 'getDivContent');
    rule = rules[1];
    this.assertEquals(rule.selector, 'button.second');
    this.assertEquals(rule.property_type, 'event');
    this.assertEquals(rule.name, 'click');
    this.assertEquals(rule.action, 'Second');
}

Class.xxx_testCorrectRulesPlusOneWrong = function() {
    // this should throw an error, diabled till this is implemented
    input = '<?xml version="1.0"?>' +
        '<rules>' +
            '<rule selector="button.button">' +
                '<event name="click">getDivContent</event>' +
            '</rule>' +
            '<rule selector="button.second">' +
                '<event name="click">Second</event>' +
            '</rule>' +
            '<rule selector="button">' +
                '<event name="click">getDivContent</event>' +
                '<event name="click">getDivContent</event>' +
            '</rule>' +
        '</rules>';
    var dom = this.doc.parseFromString(input, 'text/xml')
    this.preprocessor.parseRuleDom(dom);
    rules = this.preprocessor.rules;
    this.assertEquals(rules.length, 2);
    rule = rules[0];
    this.assertEquals(rule.selector, 'button.button');
    this.assertEquals(rule.event, 'click');
    this.assertEquals(rule.action, 'getDivContent');
    rule = rules[1];
    this.assertEquals(rule.selector, 'button.second');
    this.assertEquals(rule.event, 'click');
    this.assertEquals(rule.action, 'Second');
}

testcase_registry.registerTestCase(RuleParseTestCase, 'ruleparse');

function CommandsParseTestCase() {
    this.name = 'CommandsParseTestCase';
}

CommandsParseTestCase.prototype = new TestCase;
Class = CommandsParseTestCase.prototype;

Class.setUp = function() {
    this.preprocessor = new kukit.RuleProcessor(); 
    this.doc = new DOMParser();
};

Class.tearDown = function() {
};


Class.testOneCommand = function() {
    /*input = '<?xml version="1.0"?><rules><rule><selector>button.button</selector><event>click</event><action>getDivContent</action></rule></rules>';
    var dom = this.doc.parseFromString(input, 'text/xml')
    this.preprocessor.parseRuleDom(dom);
    rules = this.preprocessor.rules;
    this.assertEquals(rules.length, 1);
    rule = rules[0];
    this.assertEquals(rule.selector, 'button.button');
    this.assertEquals(rule.event, 'click');
    this.assertEquals(rule.action, 'getDivContent');*/
}

testcase_registry.registerTestCase(CommandsParseTestCase, 'commandparse');
