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

if (typeof(kukit) == "undefined") {
    var kukit = {};
}

/* Dummy scheduler for testing */

kukit.DummyScheduler = function(func) {
};

kukit.DummyScheduler.prototype.setNextWakeAtLeast = function(ts) {
};

kukit.RequestManagerTestCase = function() {
    this.name = 'kukit.RequestManagerTestCase';

    this.setUp = function() {
    };

    this.testSendQueue = function() {
        // Test the send queue
        var q;

        var expired = [];
        var cbe = function(item) {
            expired.push(item);
        };
        // Push items at different timepoints, with same timeout
        q = new kukit.rm.TestTimerQueue(cbe);
        var i1 = new kukit.rm.TestRequestItem(null, 1, null, 10000, 1000);
        q.push(i1);
        var i2 = new kukit.rm.TestRequestItem(null, 2, null, 10000, 2000);
        q.push(i2);
        var i3 = new kukit.rm.TestRequestItem(null, 3, null, 10000, 3000);
        q.push(i3);
        var i4 = new kukit.rm.TestRequestItem(null, 4, null, 10000, 4000);
        q.push(i4);
        this.assertEquals(q.count, 4);
        // pop 2, 4
        this.assertEquals(q.pop(i2), true);
        this.assertEquals(q.pop(i4), true);
        this.assertEquals(q.count, 2);
        this.assertEquals(expired.length, 0);
        // expire 1, 2
        q.handleExpiration(12010);
        this.assertEquals(q.count, 1);
        this.assertEquals(expired.length, 1);
        this.assertEquals(expired[0].url, 1);
        // pop 1, 3
        this.assertEquals(q.pop(i1), false);
        this.assertEquals(q.pop(i3), true);
        this.assertEquals(q.count, 0);
        this.assertEquals(expired.length, 1);
    };
    
    this.assertRmQueues = function(rm, out, wai) {
        this.assertEquals(rm.sentNr, out, 'OUT does not match');
        this.assertEquals(rm.waitingQueue.size(), wai, 'WAI does not match');
    };

    this.testNormalSend = function() {
        // Test a simple send situation
        var rm = new kukit.rm.RequestManager(null, 2, kukit.DummyScheduler);
        this.assertRmQueues(rm, 0, 0);
        // queues
        var sent = [];
        var cbs = function(item) {
            sent.push(item);
        };

        // send some elements
        rm.notifyServer(cbs, 1, null, 10000, 1000); 
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 1);
        this.assertEquals(sent[0].url, 1);
        rm.notifyServer(cbs, 2, null, 10000, 2000); 
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(sent[1].url, 2);
        rm.notifyServer(cbs, 3, null, 10000, 3000); 
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // receive the elements
        this.assertEquals(sent[0].receivedResult(4000), true);
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 3);
        this.assertEquals(sent[2].url, 3);
        this.assertEquals(sent[1].receivedResult(5000), true);
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 3);
        this.assertEquals(sent[2].receivedResult(6000), true);
        this.assertRmQueues(rm, 0, 0);
        this.assertEquals(sent.length, 3);

    };

    this.testSendWithTimeouts = function() {
        // Test a simple timeout situation
        var rm = new kukit.rm.RequestManager(null, 2, kukit.DummyScheduler);
        this.assertRmQueues(rm, 0, 0);
        // queues
        var sent = [];
        var cbs = function(item) {
            sent.push(item);
        };
        var timeout = [];
        var thook = function(item) {
            timeout.push(item);
        };

        // send some elements
        rm.notifyServer(cbs, 1, thook, 10000, 1000); 
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 1);
        this.assertEquals(sent[0].url, 1);
        this.assertEquals(timeout.length, 0);
        rm.notifyServer(cbs, 2, thook, 10000, 2000); 
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(sent[1].url, 2);
        this.assertEquals(timeout.length, 0);

        // time out 1
        rm.checkTimeout(11070);
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(timeout.length, 1);
        this.assertEquals(timeout[0].url, 1);

        // receive the elements
        this.assertEquals(sent[0].receivedResult(11060), false);
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(timeout.length, 1);
        this.assertEquals(sent[1].receivedResult(11070), true);
        this.assertRmQueues(rm, 0, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(timeout.length, 1);

    };
 
    this.testSendWithQueuedTimeout = function() {
        // Test timeout with queues not sent out
        var rm = new kukit.rm.RequestManager(null, 2, kukit.DummyScheduler);
        this.assertRmQueues(rm, 0, 0);
        // queues
        var sent = [];
        var cbs = function(item) {
            sent.push(item);
        };

        // send some elements
        rm.notifyServer(cbs, 1, null, 10000, 1000); 
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 1);
        this.assertEquals(sent[0].url, 1);
        rm.notifyServer(cbs, 2, null, 10000, 2000); 
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(sent[1].url, 2);
        rm.notifyServer(cbs, 3, null, 10000, 3000); 
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // time out 1
        rm.checkTimeout(11050);
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // receive the elements
        this.assertEquals(sent[0].receivedResult(11060), false);
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 3);
        this.assertEquals(sent[2].url, 3);
        this.assertEquals(sent[1].receivedResult(11070), true);
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 3);
        this.assertEquals(sent[2].receivedResult(11080), true);
        this.assertRmQueues(rm, 0, 0);
        this.assertEquals(sent.length, 3);

    };
 
    this.testSendWithQueuedSwallowed = function() {
        // If the queued element is timed out, it it not sent out
        var rm = new kukit.rm.RequestManager(null, 2, kukit.DummyScheduler);
        this.assertRmQueues(rm, 0, 0);
        // queues
        var sent = [];
        var cbs = function(item) {
            sent.push(item);
        };

        // send some elements
        rm.notifyServer(cbs, 1, null, 10000, 1000); 
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 1);
        this.assertEquals(sent[0].url, 1);
        rm.notifyServer(cbs, 2, null, 10000, 2000); 
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(sent[1].url, 2);
        rm.notifyServer(cbs, 3, null, 8500, 3000); 
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // time out 1
        rm.checkTimeout(11050);
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // time out 3
        rm.checkTimeout(11550);
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // receive the elements (will swallow the queued one)
        this.assertEquals(sent[0].receivedResult(11560), false);
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(sent[1].receivedResult(11570), true);
        this.assertRmQueues(rm, 0, 0);
        this.assertEquals(sent.length, 2);

    };

    this.testAllTimedOut = function() {
        // If all elements are timed out
        var rm = new kukit.rm.RequestManager(null, 2, kukit.DummyScheduler);
        this.assertRmQueues(rm, 0, 0);
        // queues
        var sent = [];
        var cbs = function(item) {
            sent.push(item);
        };

        // send some elements
        rm.notifyServer(cbs, 1, null, 10000, 1000); 
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 1);
        this.assertEquals(sent[0].url, 1);
        rm.notifyServer(cbs, 2, null, 10000, 2000); 
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(sent[1].url, 2);
        rm.notifyServer(cbs, 3, null, 10000, 3000); 
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // time out 1, 2, 3
        rm.checkTimeout(20000);
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // receive the elements (will swallow the queued one)
        this.assertEquals(sent[0].receivedResult(20010), false);
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(sent[1].receivedResult(20020), false);
        this.assertRmQueues(rm, 0, 0);
        this.assertEquals(sent.length, 2);

    };

    this.testTimeoutHooks = function() {
        // Test if timeout hook(s) are called
        var rm = new kukit.rm.RequestManager(null, 2, kukit.DummyScheduler);
        this.assertRmQueues(rm, 0, 0);
        // queues
        var sent = [];
        var cbs = function(item) {
            sent.push(item);
        };
        var timeout1 = [];
        var thook1 = function(item) {
            timeout1.push(item);
        };
        var timeout2 = [];
        var thook2 = function(item) {
            timeout2.push(item);
        };
        var timeout3 = [];
        var thook3 = function(item) {
            timeout3.push(item);
        };

        // send some elements
        rm.notifyServer(cbs, 1, thook1, 10000, 1000); 
        this.assertRmQueues(rm, 1, 0);
        this.assertEquals(sent.length, 1);
        this.assertEquals(sent[0].url, 1);
        rm.notifyServer(cbs, 2, thook2, 10000, 2000); 
        this.assertRmQueues(rm, 2, 0);
        this.assertEquals(sent.length, 2);
        this.assertEquals(sent[1].url, 2);
        rm.notifyServer(cbs, 3, thook3, 10000, 3000); 
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // time out 1, 2, 3
        rm.checkTimeout(20000);
        this.assertRmQueues(rm, 2, 1);
        this.assertEquals(sent.length, 2);

        // Check the timeout queues
        this.assertEquals(timeout1.length, 1);
        this.assertEquals(timeout1[0].url, 1);
        this.assertEquals(timeout2.length, 1);
        this.assertEquals(timeout2[0].url, 2);
        this.assertEquals(timeout3.length, 1);
        this.assertEquals(timeout3[0].url, 3);

    };
 
};
    
kukit.RequestManagerTestCase.prototype = new kukit.UtilsTestCaseBase;

if (typeof(testcase_registry) != 'undefined') {
    testcase_registry.registerTestCase(kukit.RequestManagerTestCase, 'kukit.RequestManagerTestCase');
}
