#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals
import app

from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators
import os, sys, time, json, unittest
from website_monitoring import TestSuite, TestGenerator

class Stream2Logger(object):

    def __init__(self, stream, logger, level):
        self._stream = stream
        self._logger = logger
        self._level = level
        self._buffer = []

    def write(self, message):
        self._buffer.append(message)
        if "\n" in message:
            self.flush()

    def flush(self):
        if self._buffer:
            message = "".join(self._buffer)
            if "\n" in message:
                self._logger.log(self._level, message.rstrip())
                self._buffer = []
            else:
                self._buffer = [message]

@Configuration(distributed=False)
class seleniumCommand(GeneratingCommand):
    test = Option(require=True)

    def generate(self):
        test = json.loads(self.test)
        self.logger.setLevel("DEBUG")
        test_case = TestGenerator(test, True)
        setattr(TestSuite, "test_site", test_case)

        class TextTestResultWithSuccesses(unittest.TextTestResult):
            def addSuccess(self, test):
                super(TextTestResultWithSuccesses, self).addSuccess(test)
                self.results = test.test.results

        suite = unittest.TestLoader().loadTestsFromTestCase(TestSuite)
        stream = Stream2Logger(sys.stderr, self.logger, self.logger.level)
        testrunner = unittest.TextTestRunner(stream=stream, verbosity=0, resultclass=TextTestResultWithSuccesses).run(suite)
        testrunner.results['_raw'] = json.dumps(testrunner.results,sort_keys=True)
        yield testrunner.results

dispatch(seleniumCommand, sys.argv, sys.stdin, sys.stdout, __name__)