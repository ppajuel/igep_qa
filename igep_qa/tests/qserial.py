#!/usr/bin/env python

"""
Serial Test Cases modules for unittest

"""

import time
import serial
import unittest

class TestSerial(unittest.TestCase):
    """ Generic Tests for serial interface.

    Keyword arguments:
        - port: Serial device. E.g. /dev/ttyS0, /dev/ttyUSB0

    """
    def __init__(self, testname, port):
        super(TestSerial, self).__init__(testname)
        self.port = serial.Serial(port, timeout=1)
        self.port.flushInput()
        self.port.flushOutput()

    def __del__(self):
        self.port.close()

    def shortDescription(self):
        doc = self._testMethodDoc
        doc = doc.replace("Test Serial", "Test Serial (%s)" % self.port.portstr)
        return doc and doc.split("\n")[0].strip() or None

    def test_serial_loopback(self):
        """ Test Serial : Loopback, each sent character should return

        Type: Functional

        Requirements:
            A simple loopback hardware is required, shortcut these pin pairs:
                TX  <-> RX (on a 9 pole DSUB are the pins 2-3)

        Description:
            - Connect the loopback hardware.
            - A range of numbers are sent for TX and should return to RX.

        """
        for c in map(chr, range(32)):
            self.port.write(c)
            time.sleep(0.05)    # there might be a small delay
            self.failUnless(self.port.inWaiting() == 1, "failed: Expected one "
                            "character for inWainting()")
            self.failUnless(self.port.read(1) == c, "failed: Expected a '%s' "
                            "which was written before" % c)

if __name__ == '__main__':
    unittest.main(verbosity=2)
