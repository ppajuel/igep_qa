#!/usr/bin/env python

"""
Bluetooth Test Cases modules for unittest

"""

import commands
import unittest

class TestBluetooth(unittest.TestCase):
    """ Generic tests for bluetooth interfaces.

    Keyword arguments:
        - port: Serial device. E.g. /dev/ttyS0, /dev/ttyUSB0

    Prerequisite commands:
        - bccmd

    """
    def __init__(self, testname, port):
        super(TestBluetooth, self).__init__(testname)
        self.port = port

    def test_get_chip_revision(self):
        """ Test Bluetooth : Get chip revision

        Type: Functional

        Description:
            Ask for chip revision using the CSR BCCMD interface.

        """
        retval = commands.getstatusoutput("bccmd -t bcsp -d %s chiprev"
                                          "" % self.port)
        self.failUnless(retval[0]==0, "error: Failed to get chip revision")


if __name__ == '__main__':
    unittest.main(verbosity=2)
