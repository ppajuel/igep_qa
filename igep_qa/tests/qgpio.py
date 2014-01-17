#!/usr/bin/env python

"""
GPIO Test Cases modules for unittest

"""

import time
import unittest

from igep_qa.helpers.gpiolib import QGpio

class TestGpio(unittest.TestCase):
    """ Generic Tests for GPIOs.

    Keyword arguments:
        - gpio_in: GPIO input number.
        - gpio_out: GPIO output number.
        - testdescription: Optional test description to overwrite the default.

    """
    def __init__(self, testname, gpio_in, gpio_out, testdescription=''):
        super(TestGpio, self).__init__(testname)
        self.gpio_in = QGpio(gpio_in)
        self.gpio_out = QGpio(gpio_out)

        # Overwrite test description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_loopback(self):
        """ Test GPIO: Test loopback

        Type: Functional

        Description:
            This test suposes that there is a loopback between the gpio_in and
            the gpio_out. With this condition the test consists to set the
            gpio_out to high value and check gpio_in to have the same value,
            after that, sets the gpio_out to low and checks again that gpio_in
            has the same value.

        """
        self.gpio_out.set_value(1)
        # a delay is required as the relay is slow
        time.sleep(2)
        retval = self.gpio_in.get_value()
        self.failUnless(retval == 1, "failed: Expected value '1' and read '%s'" % retval)
        self.gpio_out.set_value(0)
        # a delay is required as the relay is slow
        time.sleep(2)
        retval = self.gpio_in.get_value()
        self.failUnless(retval == 0, "failed: Expected value '0' and read '%s'" % retval)

if __name__ == '__main__':
    unittest.main(verbosity=2)
