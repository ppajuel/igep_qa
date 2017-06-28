#!/usr/bin/env python

"""
Watchdog Test Cases modules for unittest

"""

import commands
import unittest
import time

class TestWatchdog(unittest.TestCase):
    """ Generic Tests for Watchdog reboot.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - device: Optional Watchdog device path.
        - i2cbus : Optional I2C bus number.
        - address : Optional device I2C address (in hexadecimal)
        - register : Optional device I2C register (in hexadecimal)
        - testdescription: Optional test description to overwrite the default.

    Prerequisite commands:
        - i2c-tools

    """

    def __init__(self, testname, device='', i2cbus='', address='', register='', testdescription=''):
        super(TestWatchdog, self).__init__(testname)
        self.device = device
        self.i2cbus = i2cbus
        self.address = address
        self.register = register

        # Overwrite test description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_igep0046_watchdog(self):
        """ Test IGEP0046 Watchdog : Check if device has been rebooted before

        Type: Functional

        Description:
            Trigger watchdog counter and set a volatile magic number to
            PMIC volatile memory. Finally, parse reboot procedure.

        .. warning::

            Test is not valid if a Coin cell battery is used.
            Test is only valid for IGEP0046.
            To reduce test procedure time. Add this test at the beginning
            of testsuite.
        """

        # Parse if IGEP0046 has rebooted before
        retval = commands.getstatusoutput('i2cget -f -y %s %s %s'
                                  % (self.i2cbus, self.address, self.register))
        self.failUnless(retval[0] == 0, "failed: Can't execute 'i2cget'")

        if not retval[1] == '0x89':
            # Board need to be rebooted
            retval = commands.getstatusoutput("reset > /dev/tty0")
            self.failUnless(retval[0] == 0, "failed: Can't execute 'reset > /dev/tty0'")
            retval = commands.getstatusoutput("echo '\033[37mTest IGEP0046 Watchdog : Board need to reboot to PASS test. Reboot on. WAIT. \033' > /dev/tty0")
            self.failUnless(retval[0] == 0, "failed: Can't execute 'echo'")
            # Set magic number
            retval = commands.getstatusoutput('i2cset -f -y %s %s %s 0x89'
                                      % (self.i2cbus, self.address, self.register))
            self.failUnless(retval[0] == 0,
                        'failed: Cannot read at I2C bus %s address and %s register %s'
                         % (self.i2cbus, self.address, self.register))
            # Reboot (enable watchdog)
            retval = commands.getstatusoutput('reboot')
            self.failUnless(retval[0] == 0,
                        'failed: Cannot reboot board')
            # Reboot timeout
            time.sleep(20)
            retval = commands.getstatusoutput("echo '\033[37mTest IGEP0046 Watchdog : Reboot FAILED. Test cannot be executed \033' > /dev/tty0")
            self.failUnless(retval[0] == 0, "failed: Can't execute 'echo'")
            self.fail("Error, reboot failed")