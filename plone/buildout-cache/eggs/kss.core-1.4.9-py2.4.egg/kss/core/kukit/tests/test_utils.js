/*
* Copyright (c) 2005-2008
* Authors: KSS Project Contributors (see doc/CREDITS.txt)
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

kukit.UtilsTestCaseBase = function() {
   
    this.assertDictEquals = function(a, b, reason) {
        if (typeof(reason) == 'undefined') {
            reason = '';
        } else {
            reason += ', ';
        }
        for (var key in a) {
            this.assertNotEquals(typeof(b[key]), 'undefined', reason + 'key ' + key + ' missing from dict 2');
            this.assertEquals(a[key], b[key], reason + 'mismatch at key ' + key);
        }
        for (var key in b) {
            this.assertNotEquals(typeof(a[key]), 'undefined', reason + 'key ' + key + ' missing from dict 1');
            this.assertEquals(a[key], b[key], reason + 'mismatch at key ' + key);
        }
    };

    this.assertListEquals = function(a, b, reason) {
        if (typeof(reason) == 'undefined') {
            reason = '';
        } else {
            reason += ', ';
        }
        this.assertEquals(a.length, b.length, reason + 'lists of different length');
        for (var i=0; i<a.length; i++) {
            this.assertEquals('"' + a[i] + '"', '"' + b[i] + '"', reason + 'list values differ in position ' + i);
        }
    };
    
};

kukit.UtilsTestCaseBase.prototype = new TestCase;

kukit.UtilsTestCase = function() {
    this.name = 'kukit.UtilsTestCase';

    this.setUp = function() {
    };

    this.testFifoQueue = function() {
        // Test the fifo queue
        var q;

        q = new kukit.ut.FifoQueue();
        this.assertEquals(q.empty(), true);
        this.assertEquals(q.size(), 0);
        q.push(1);
        q.push(3);
        q.push(2);
        q.push(4);
        this.assertEquals(q.empty(), false);
        this.assertEquals(q.size(), 4);
        this.assertEquals(q.front(), 1);
        this.assertListEquals(q.elements, [1, 3, 2, 4]);
        this.assertEquals(q.pop(), 1);
        this.assertEquals(q.pop(), 3);
        this.assertEquals(q.pop(), 2);
        this.assertEquals(q.pop(), 4);
        this.assertEquals(q.empty(), true);
        this.assertEquals(q.size(), 0);
    };

    this.testSortedQueue = function() {
        // Test the sorted queue
        var q;

        q = new kukit.ut.SortedQueue();
        this.assertEquals(q.empty(), true);
        this.assertEquals(q.size(), 0);
        q.push(1);
        q.push(3);
        q.push(2);
        q.push(4);
        this.assertEquals(q.empty(), false);
        this.assertEquals(q.size(), 4);
        this.assertEquals(q.front(), 1);
        this.assertListEquals(q.elements, [1, 2, 3, 4]);
        this.assertEquals(q.pop(), 1);
        this.assertEquals(q.pop(), 2);
        this.assertEquals(q.pop(), 3);
        this.assertEquals(q.pop(), 4);
        this.assertEquals(q.empty(), true);
        this.assertEquals(q.size(), 0);

        // reverse order
        var comparefunc = function(a, b) {
            if (a < b) return +1;
            else if (a > b) return -1;
            else return 0;
        };
        q = new kukit.ut.SortedQueue(comparefunc);
        this.assertEquals(q.empty(), true);
        this.assertEquals(q.size(), 0);
        q.push(1);
        q.push(3);
        q.push(2);
        q.push(4);
        this.assertEquals(q.empty(), false);
        this.assertEquals(q.size(), 4);
        this.assertEquals(q.front(), 4);
        this.assertListEquals(q.elements, [4, 3, 2, 1]);
        this.assertEquals(q.pop(), 4);
        this.assertEquals(q.pop(), 3);
        this.assertEquals(q.pop(), 2);
        this.assertEquals(q.pop(), 1);
        this.assertEquals(q.empty(), true);
        this.assertEquals(q.size(), 0);

    };

    this.testEvalList = function() {
        var value = kukit.ut.evalList('');
        this.assertListEquals(value, []);
        var value = kukit.ut.evalList('    ');
        this.assertListEquals(value, []);
        value = kukit.ut.evalList('1');
        this.assertListEquals(value, ['1']);
        value = kukit.ut.evalList('1,2');
        this.assertListEquals(value, ['1', '2']);
        value = kukit.ut.evalList('1, 2');
        this.assertListEquals(value, ['1', '2']);
        value = kukit.ut.evalList('1, 2 ');
        this.assertListEquals(value, ['1', '2']);
        value = kukit.ut.evalList(' 1, 2');
        this.assertListEquals(value, ['1', '2']);
        value = kukit.ut.evalList('  1  ,  2  ');
        this.assertListEquals(value, ['1', '2']);
    }

};
    
kukit.UtilsTestCase.prototype = new kukit.UtilsTestCaseBase;

kukit.BaseURLTestCase = function() {
    this.name = 'kukit.BaseURLTestCase';

    this.setUp = function() {
        this.dom = new global.dommer.DOM();
        this.doc = this.dom.createDocument();
        this.html = this.doc.createElement('html');
        this.doc.appendChild(this.html);
        this.baseTag = this.doc.createElement('base');
        this.kssBaseTag = this.doc.createElement('link');
        this.kssBaseTag.rel = 'kss-base-url';
        this.pageLocation = "http://kssproject.org/tests";
        this.baseLocation = "http://kssproject.org/base";
        this.kssBaseLocation = "http://kssproject.org/kssbase";
        this.pageRoot = "http://kssproject.org";
    };

    this.testLocation = function() {
        var base = kukit.ut.calculateBase(this.doc, this.pageLocation);
        this.assertEquals(base, this.pageRoot + '/');
    };
    
    this.testLocationWithTrailingSlash = function() {
        var base = kukit.ut.calculateBase(this.doc, this.pageLocation + '/');
        this.assertEquals(base, this.pageLocation + '/');
    };
    
    this.testBaseTagWithTrailingSlash = function() {
        this.baseTag.href = this.baseLocation + '/';
        this.html.appendChild(this.baseTag);
        var base = kukit.ut.calculateBase(this.doc, this.pageLocation);
        this.assertEquals(base, this.baseLocation + '/');
    };
    
    this.testBaseTag = function() {
        this.baseTag.href = this.baseLocation;
        this.html.appendChild(this.baseTag);
        var base = kukit.ut.calculateBase(this.doc, this.pageLocation);
        this.assertEquals(base, this.pageRoot + '/');
    };
    
    this.testKssBaseTagWithTrailingSlash = function() {
        this.kssBaseTag.href = this.kssBaseLocation + '/';
        this.html.appendChild(this.kssBaseTag);
        var base = kukit.ut.calculateBase(this.doc, this.pageLocation);
        this.assertEquals(base, this.kssBaseLocation + '/');
    };
    
    // XXX This test is currently wrong, because Plone does _not_
    // XXX put the trailing slash to the end, so kss-base-url without
    // XXX the trailing slash is currently interpreted as if it were there.
    this.testKssBaseTag = function() {
        this.kssBaseTag.href = this.kssBaseLocation;
        this.html.appendChild(this.kssBaseTag);
        var base = kukit.ut.calculateBase(this.doc, this.pageLocation);
        // XXX this.assertEquals(base, this.pageRoot + '/');
        this.assertEquals(base, this.kssBaseLocation + '/');
    };
    
    this.testBothKssAndBaseTagWithTrailingSlash = function() {
        this.kssBaseTag.href = this.kssBaseLocation + '/';
        this.html.appendChild(this.kssBaseTag);
        this.baseTag.href = this.baseLocation;
        this.html.appendChild(this.baseTag);
        var base = kukit.ut.calculateBase(this.doc, this.pageLocation);
        this.assertEquals(base, this.kssBaseLocation + '/');
    };
    
    // XXX This test is currently wrong, because Plone does _not_
    // XXX put the trailing slash to the end, so kss-base-url without
    // XXX the trailing slash is currently interpreted as if it were there.
    this.testBothKssAndBaseTag = function() {
        this.kssBaseTag.href = this.kssBaseLocation;
        this.html.appendChild(this.kssBaseTag);
        this.baseTag.href = this.baseLocation;
        this.html.appendChild(this.baseTag);
        var base = kukit.ut.calculateBase(this.doc, this.pageLocation);
        // XXX this.assertEquals(base, this.pageRoot + '/');
        this.assertEquals(base, this.kssBaseLocation + '/');
    };
};

kukit.BaseURLTestCase.prototype = new kukit.UtilsTestCaseBase;

if (typeof(testcase_registry) != 'undefined') {
    testcase_registry.registerTestCase(kukit.UtilsTestCase, 'kukit.UtilsTestCase');
    testcase_registry.registerTestCase(kukit.BaseURLTestCase, 'kukit.BaseURLTestCase');
}
