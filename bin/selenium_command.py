#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals
import app

from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators
import os, sys, time, json, unittest
from website_monitoring import TestSuite, TestGenerator

@Configuration(distributed=False)
class seleniumCommand(GeneratingCommand):
    test = Option(require=True)

    def generate(self):
        test = json.loads(self.test)
        test_case = TestGenerator(test, True)
        setattr(TestSuite, "test_site", test_case)

        class TextTestResultWithSuccesses(unittest.TextTestResult):
            def addSuccess(self, test):
                super(TextTestResultWithSuccesses, self).addSuccess(test)
                self.results = test.test.results

        with open(os.devnull, 'w') as null_stream:
            suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
            testrunner = unittest.TextTestRunner(stream=null_stream, verbosity=0, resultclass=TextTestResultWithSuccesses).run(suite)
            testrunner.results['_raw'] = json.dumps(testrunner.results,sort_keys=True)
            yield testrunner.results

dispatch(seleniumCommand, sys.argv, sys.stdin, sys.stdout, __name__)