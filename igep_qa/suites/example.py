#!/usr/bin/env python

"""
For every test suite we create an instance of TestSuite and add test case
instances. When all tests have been added, the suite can be passed to a test
runner, such as TextTestRunner. It will run the individual test cases in the
order in which they were added, aggregating the results.

An example class implementation of a test suite:

.. code-block:: python

    import unittest
    from tests import network

    def TestSuiteMyExample():
        suite = unittest.TestSuite()
        suite.addTest(network.TestNetwork("test_ping_host", "127.0.0.1", "127.0.0.1", "eth0"))
        return suite

The main program just runs the test suite, the output format depends on the
Test Runner. Here we'll launch the test suite twice. The first one, uses the
popular TextTestRunner from unittest module. The second one, uses a very simple
Test Runner that only prints a '.' if the test case has been successed, and an
'F' if the test case has been failed.

.. code-block:: python

    from runners import lightly

    if __name__ == '__main__':
        # Output Using TextTestRunner from unittest module"
        unittest.TextTestRunner(verbosity=2).run(TestSuiteMyExample())
        # Output using LightlyTestRunner from lightly module"
        suite =  lightly.LightlyTestRunner()
        suite.run(TestSuiteMyExample())

"""

import unittest
from igep_qa.tests import qnetwork

def TestSuiteMyExample():
    """ An example class implementation of a test suite.

    What is tested?
        - Network : Ping the IP address of a remote host.

    """
    suite = unittest.TestSuite()
    suite.addTest(qnetwork.TestNetwork("test_ping_host", "127.0.0.1", "127.0.0.1", "eth0"))
    return suite

from igep_qa.runners import lightly

if __name__ == '__main__':
    # Output Using TextTestRunner from unittest module"
    unittest.TextTestRunner(verbosity=2).run(TestSuiteMyExample())
    # Output using LightlyTestRunner from lightly module"
    suite =  lightly.LightlyTestRunner()
    suite.run(TestSuiteMyExample())
