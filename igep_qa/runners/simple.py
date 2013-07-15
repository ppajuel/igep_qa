#!/usr/bin/env python

"""
Simple Test Runner for unittest module

"""

import sys
import unittest

class SimpleTestRunner:
    """ A Test Runner that shows results in a simple human-readable format.  

    As example, a common output is:
        This is a test short description : PASS
        This is another test short description : FAIL
        ---------------------------------------------

    """
    def __init__(self, stream=sys.stderr, verbosity=0):
        self.stream = stream
        self.verbosity = verbosity

    def writeUpdate(self, message):
        self.stream.write(message)

    def run(self, test):
        """ Run the given test case or Test Suite.

        """
        result = TextTestResult(self)
        test(result)
        result.testsRun
        self.writeUpdate("---------------------------------------------\n")
        return result

class TextTestResult(unittest.TestResult):
    # Print in terminal with colors
    PASS = '\033[92mPASS\033[0m\n'
    FAIL = '\033[91mFAIL\033[0m\n'
    ERROR = '\033[91mERROR\033[0m\n'

    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self.runner.writeUpdate("%s : " % test.shortDescription())

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.runner.writeUpdate(self.PASS)

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.runner.writeUpdate(self.ERROR)

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.runner.writeUpdate(self.FAIL)
