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
        - options: Use this parameter to pass other supported options to the
                   hciattach command. To see what options are available just
                   type hciattach without arguments in a terminal.

    Prerequisite commands:
        - bccmd

    """
    def __init__(self, testname, port, options=''):
        super(TestBluetooth, self).__init__(testname)
        self.port = port
        self.options = options

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

if __name__ == '__main__':
    unittest.main(verbosity=2)
