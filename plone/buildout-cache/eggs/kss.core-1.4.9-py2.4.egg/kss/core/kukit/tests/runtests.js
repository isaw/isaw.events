/*****************************************************************************
 *
 * Copyright (c) 2003-2004 EcmaUnit Contributors. All rights reserved.
 *
 * This software is distributed under the terms of the EcmaUnit
 * License. See LICENSE.txt for license text. For a list of EcmaUnit
 * Contributors see CREDITS.txt.
 *
 *****************************************************************************/

// $Id: runtests.js 18718 2005-10-17 14:29:18Z duncan $

/*
  Test runner for command-line environments, such as spidermonkey
*/

function runTests() {
    var reporter = new StdoutReporter;
    var testsuite = new TestSuite(reporter);
    testsuite.registerTest(kukit.UtilsTestCase);
    testsuite.registerTest(kukit.BaseURLTestCase);
    testsuite.registerTest(kukit.RequestManagerTestCase);
    testsuite.registerTest(kukit.TokenizerTestCase);
    testsuite.registerTest(kukit.KssParserTestCase);
    testsuite.registerTest(kukit.KssParserSelectorsTestCase);
    testsuite.registerTest(kukit.KssParserValueProvidersCheckTestCase);
    testsuite.registerTest(kukit.KssParserSelectorTestCase);
    testsuite.runSuite();
};

runTests();
