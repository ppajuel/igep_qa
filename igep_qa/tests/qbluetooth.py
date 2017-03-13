#!/usr/bin/env python

"""
Bluetooth Test Cases modules for unittest

"""

import commands
import unittest
# Test Helpers
from igep_qa.helpers import common

class TestBluetooth(unittest.TestCase):
    """ Generic tests for bluetooth interfaces.

    Keyword arguments:
        - port: Serial device. E.g. /dev/ttyS0, /dev/ttyUSB0
        - options: Use this parameter to pass other supported options to the
                   hciattach command. To see what options are available just
                   type hciattach without arguments in a terminal.
        - revision: Use this parameter to pass lmp revision.

    Prerequisite commands:
        - bccmd: for class test_get_chip_revision
        - hciconfig: for class test_attach_uart_hci
        - hciattach: for class test_get_lmp_revision

    """
    def __init__(self, testname, port='', options='', revision=''):
        super(TestBluetooth, self).__init__(testname)
        self.port = port
        self.options = options
        self.revision = revision

    def test_get_chip_revision(self):
        """ Test Bluetooth : Get chip revision

        Type: Functional

        Description:
            Ask for chip revision using the CSR BCCMD interface.

        """
        retval = commands.getstatusoutput("bccmd -t bcsp -d %s chiprev"
                                          "" % self.port)
        self.failUnless(retval[0] == 0, "error: Failed to get chip revision")

    def test_attach_uart_hci(self):
        """ Test Bluetooth : Attach serial devices via UART HCI to BlueZ stack

        Type: Functional

        Description:
            Attach to serial device connected to <port> using hciattach command.

        """
        retval = commands.getstatusoutput("hciattach %s %s" % (self.port, self.options))
        self.failUnless(retval[0] == 0, "error: Failed to attach to bluetooth ")

    def test_get_lmp_revision(self):
        """ Test Bluetooth : Get Link Manager Protocol (LMP) revision

        Type: Functional

        Description:
            Ask for Bluetooth LMP revision using the hciconfig program

        """
        common.set_WiLink_bluetooth()

        retval = commands.getstatusoutput("hciconfig hci0 version | grep %s" % self.revision)
        self.failUnless(retval[0] == 0, "error: Failed to get chip revision")

if __name__ == '__main__':
    unittest.main(verbosity=2)
