#!/usr/bin/env python

"""
This provides a wrapper of GPIO access conventions on Linux. 

See: Documentation/gpio.txt from kernel sources

"""

import os

class QGpio:
    """ GPIOLIB interface to access the GPIO pins from the User Space.

    """
    def __init__(self, gpio):
        """ Export a GPIO to userspace through sysfs
        
        Keyword arguments:
            - gpio: GPIO number to make available, already requested

        """
        self.debug = False
        self.already_exported = True
        self.gpio = str(gpio)
        self.sysfs = '/sys/class/gpio/gpio%s' % gpio
        if os.path.exists(self.sysfs):
            if self.debug == True:
                print "GPIO %s already exists, skipping exporting" % self.gpio
            self.already_exported = True
        else:
            fd = open('/sys/class/gpio/export', 'w')
            fd.write(self.gpio)
            fd.close()

    def __del__(self):
        """ Reverse gpio_export from User Space.

        """
        if not self.already_exported:
            fd = open('/sys/class/gpio/unexport', 'w')
            fd.write(self.gpio)
            fd.close()

    def get_direction(self):
        """ Get GPIO direction.

        Returns "in" for input and "out" for output.

        """
        try:
            fd = open("%s/direction" % self.sysfs, "r")
            retval = fd.read()
            fd.close()
            return retval
        except IOError:
            if self.debug == True:
                print "gpio%s/direction not found, check direction capabilites" % self.gpio
            return ""

    def set_direction(self, direction):
        """Set GPIO direction.

        Keyword arguments:
            - direction: "in" for input and "out" for output.

        """
        if not os.path.exists("%s/direction" % self.sysfs):
            if self.debug == True:
                print "direction for GPIO %s not found, skipping" % self.gpio
            pass
        else:
            fd = open('%s/direction' % self.sysfs, 'w')
            fd.write(direction)
            fd.close()

    def get_value(self):
        """ Get GPIO value.

        Returns "0" for low level and "1" for high level.

        """
        fd = open('%s/value' % self.sysfs, 'r')
        retval = fd.read()
        fd.close()
        return int(retval)

    def set_value(self, value):
        """ Set GPIO value.
        
        Keyword arguments:
            - value: Set zero for low level and nonzero for high level.

        """
        self.set_direction("out")
        fd = open('%s/value' % self.sysfs, 'w')
        fd.write(str(value))
        fd.close()

    def get_active_low(self):
        """ Get active_low value.

        Returns "0" for low level and "1" for high level.

        """
        fd = open('%s/value' % self.sysfs, 'r')
        retval = fd.read()
        fd.close()
        return int(retval)

    def set_active_low(self, value):
        """ Set active_low value.

        Keyword arguments:
            - value: Write any nonzero value to invert the value attribute both
                     for reading and writing.

        """
        fd = open('%s/active_low' % self.sysfs, 'w')
        fd.write(str(value))
        fd.close()

    def get_edge(self):
        """ Get GPIO edge.

        Returns: "none", "rising", "falling" or "both"

        """
        try:
            fd = open("%s/edge" % self.sysfs, "r")
            retval = fd.read()
            fd.close()
            return retval
        except IOError:
            if self.debug == True:
                print "gpio%s/edge not found, check edge capabilites" % self.gpio
            return ""

    def set_edge(self, edge):
        """Set GPIO edge.

        Keyword arguments:
            - edge: must be "none", "rising", "falling" or "both".

        """
        if not os.path.exists("%s/edge" % self.sysfs):
            if self.debug == True:
                print "edge for GPIO %s not found, skipping" % self.gpio
            pass
        else:
            fd = open('%s/edge' % self.sysfs, 'w')
            fd.write(edge)
            fd.close()

# -----------------------------------------------------------------------------
# Test Cases for class TGPIO
# -----------------------------------------------------------------------------
import unittest

class TestClassQGpio(unittest.TestCase):
    """ Unittest for class QGpio

    """
    def setUp(self):
        self.gpio = QGpio(21)

    def test_set_value_to_high(self):
        self.gpio.set_value(1)
        retval = self.gpio.get_value()
        self.failUnless(retval == 1,
            "Error: Expected value '1' and readed '%s'" % retval)

    def test_set_value_to_low(self):
        self.gpio.set_value(0)
        retval = self.gpio.get_value()
        self.failUnless(retval == 0,
            "Error: Expected value '0' and readed '%s'" % retval)

    def test_set_direction_to_output(self):
        self.gpio.set_direction("out")
        retval = self.gpio.get_direction()
        self.failUnless(retval == 'out\n',
            "Error: Expected value 'out' and readed %s" % retval)

    def test_set_direction_to_input(self):
        self.gpio.set_direction("in")
        retval = self.gpio.get_direction()
        self.failUnless(retval == 'in\n',
            "Error: Expected value 'in' and readed %s" % retval)

    def test_set_edge_to_none(self):
        self.gpio.set_edge("none")
        retval = self.gpio.get_edge()
        self.failUnless(retval == 'none\n',
            "Error: Expected value 'none' and readed %s" % retval)

    def test_set_edge_to_rising(self):
        self.gpio.set_edge("rising")
        retval = self.gpio.get_edge()
        self.failUnless(retval == 'rising\n',
            "Error: Expected value 'rising' and readed %s" % retval)

    def test_set_edge_to_falling(self):
        self.gpio.set_edge("falling")
        retval = self.gpio.get_edge()
        self.failUnless(retval == 'falling\n',
            "Error: Expected value 'falling' and readed %s" % retval)

    def test_set_edge_to_both(self):
        self.gpio.set_edge("both")
        retval = self.gpio.get_edge()
        self.failUnless(retval == 'both\n',
            "Error: Expected value 'both' and readed %s" % retval)

if __name__ == '__main__':
    unittest.main()
