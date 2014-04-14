#!/usr/bin/env python

"""
Board Specific Test Cases modules for unittest

"""

import serial
import time
import unittest

from igep_qa.helpers import gpiolib

class TestSerialMuxer(unittest.TestCase):
    """ Serial Muxer tests for ILMS0010 board.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - testdescription: Optional test description to overwrite the default.

    """
    def __init__(self, testname, testdescription=''):
        super(TestSerialMuxer, self).__init__(testname)
        self.timeout = 1
        self.gpio19 = gpiolib.QGpio(19)
        self.gpio22 = gpiolib.QGpio(22)
        # Overwrite test description
        if testdescription:
            self._testMethodDoc = testdescription

    def setUp(self):
        self.s = serial.Serial('/dev/ttyO1', 115200, timeout=self.timeout)

    def tearDown(self):
        self.s.close()

    def fight(self, r):
        if r == 0:
            self.gpio19.set_value(0)
            self.gpio22.set_value(0)
        elif r == 1:
            self.gpio19.set_value(1)
            self.gpio22.set_value(0)
        elif r == 2:
            self.gpio19.set_value(0)
            self.gpio22.set_value(1)
        elif r == 3:
            self.gpio19.set_value(1)
            self.gpio22.set_value(1)

    def test_serial_muxer(self):
        """ Test Serial Muxer : Request-response with other computer (Ryu VS Ken)

        Type: Functional

        Requirements:
             - A simple cross wired hardware, shortcut these pin pairs:
                 TX-a  <-> RX-b (on a 9 pole DSUB are the pins 2-3)
                 TX-b  <-> RX-a (on a 9 pole DSUB are the pins 2-3)

        Description:
            Connect cross cables between port 1 to 4 of equipment under test
            to ports 1 to 4 of serial server equipment.
            The test selects the first port setting gpio19 and gpio22 and sends
            the message 'Are You Ken?' to the server if the server answers
            'Come closer!' the test repeats this sequence for the other 3 ports.
            (in memory of Street Fighter)

        """
        for port in range(4):
            self.fight(port)
            time.sleep(0.05)  # there might be a small delay
            self.s.write('Are You Ken?')
            retval = (self.s.read(12) == 'Come Closer!')
            self.failUnless(retval, 'error: Failed talking with port %s.' % (port + 1))

if __name__ == '__main__':
    unittest.main(verbosity=2)
