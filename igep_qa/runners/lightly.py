#!/usr/bin/env python

"""
Lightly Test Runner for unittest module

"""

import sys
import unittest

class LightlyTestRunner:
    """ A Test Runner that show results in a string of characters.

    By default the results are:
        - '.' for success
        - 'F' for failure
        - 'E' for error.

    As example, a common output is:
        ....F....E...

    """
    def __init__(self, stream=sys.stderr, verbosity=0):
        self.stream = stream
        self.verbosity = verbosity

    def writeUpdate(self, message):
        self.stream.write(message)

    def run(self, test, success = '.', failure = 'F', error = 'E'):
        """ Run the given test case or Test Suite.

        Keyword arguments:
            - success: Character to be printed when successfully.
            - failure: Character to be printed when failure.
            - error: Character to be printed on error.

        """
        result = LightlyTestResult(self)
        result.updateResult(success, failure, error)
        test(result)
        result.testsRun
        return result

class LightlyTestResult(unittest.TestResult):
    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner

    def updateResult(self, success, failure, error):
        self.resultPass = success
        self.resultFail = failure
        self.resultError = error

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.runner.writeUpdate(self.resultPass)

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.runner.writeUpdate(self.resultError)

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.runner.writeUpdate(self.resultFail)
