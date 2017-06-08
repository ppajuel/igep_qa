#!/usr/bin/env python

"""
I2C Test Cases modules for unittest

"""

import commands
import unittest

class TestI2C(unittest.TestCase):
    """ Generic Tests for I2C interface.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - i2cbus : The I2C bus number.
        - address : The device I2C address (in hexadecimal)
        - register : The device I2C register (in hexadecimal)
        - testdescription: Optional test description to overwrite the default.

    Prerequisite commands:
        - i2c-tools

    """

    def __init__(self, testname, i2cbus, address, register='', testdescription=''):
        super(TestI2C, self).__init__(testname)
        self.i2cbus = i2cbus
        self.address = address
        self.register = register
        # Overwrite test description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_i2cdetect(self):
        """ Test I2C : Check if device is at I2C bus at address.

        Type: Functional

        Description:
            Reads the <syspath>/name to check that devname is detected.

        """
        retval = commands.getstatusoutput('i2cget -f -y %s %s'
                                          % (self.i2cbus, self.address))
        self.failUnless(retval[0] == 0,
                        'failed: No device detected at I2C bus %s address %s'
                         % (self.i2cbus, self.address))

    def test_i2cget(self):
        """ Test I2C : Get I2C register from I2C bus at address.

        Type: Functional

        Description:
            Reads a register to check I2C device.

        """
        retval = commands.getstatusoutput('i2cget -f -y %s %s %s'
                                          % (self.i2cbus, self.address, self.register))
        self.failUnless(retval[0] == 0,
                        'failed: Cannot read at I2C bus %s address and %s register %s'
                         % (self.i2cbus, self.address, self.register))