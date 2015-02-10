#!/usr/bin/env python

import ConfigParser
import sys
import unittest
# Test Helpers
from igep_qa.helpers import gpiolib
# Test Runners
from igep_qa.runners import dbmysql
# Test Cases
from igep_qa.tests.qgpio import TestGpio
from igep_qa.tests.qmodem import TestModem
from igep_qa.tests.qserial import TestSerial
import time

class TestModemSlnk0011(TestModem):
    """ Specific Test for modem on SLNK0011 board.

    Keyword arguments:
        - on: GPIO number to turn ON/OFF the modem.
        - reset: GPIO number to reset the modem.
        - pwrmon: GPIO number that should be monitored to check if the
                  device has powered on.
        - port: The serial port used for the modem.
        - testdescription: Optional test description to overwrite the default.

    Description:
        In this board is required to enable the serial port via a gpio in order
        get working.

    """
    def __init__(self, testname, on, reset, pwrmon, port, testdescription=''):
        super(TestModemSlnk0011, self).__init__(testname, on, reset, pwrmon, port, testdescription)

    def setUp(self):
        self.port_enable = gpiolib.QGpio(137)
        self.port_enable.set_value(0)
        # a small delay to be sure port switched
        time.sleep(1)

class TestSerialSlnk0011(TestSerial):
    """ Generic Tests for serial interface.

    Keyword arguments:
        - port: Serial device. E.g. /dev/ttyS0, /dev/ttyUSB0

    """
    def __init__(self, testname, port):
        super(TestSerialSlnk0011, self).__init__(testname, port)

    def setUp(self):
        self.port_enable = gpiolib.QGpio(137)
        self.port_enable.set_value(1)
        time.sleep(1)
        self.port.flushInput()
        self.port.flushOutput()


# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_SLNK0011():
    """ A number of TestCases for the SLNK0010 board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code-block:: ini

        [default]
        serverip = 192.168.13.1
        ipaddr = 192.168.13.10

        [mysqld]
        user = root
        host = 192.168.13.1
        database = dbtest

    To configure the SLNK0011 board you should pass following kernel cmdline parameters:

    .. code-block:: ini

        board.ei485=no
        buddy=slnk0011

    You can run the test at bootup adding:

    .. code-block:: ini

        autotest=SLNK0011 quiet

    What is tested?
        - Test Serial (/dev/ttyO0): Loopback, each sent character should return
        - Test Serial (/dev/ttyO1): Loopback, each sent character should return
        - Test Serial (/dev/ttyO2): Loopback, each sent character should return
        - Test GPIOs : Loopback, between gpio 156 (in) and gpio 161 (out)
        - Test GPIOs : Loopback, between gpio 157 (in) and gpio 159 (out)
        - Test GPIOs : Loopback, between gpio 130 (in) and gpio 131 (out)
        - Test GPIOs : Loopback, between gpio 135 (in) and gpio 158 (out)
        - Test GPIOs : Loopback, between gpio 133 (in) and gpio 158 (out)
        - Test GPIOs : Loopback, between gpio 132 (in) and gpio 162 (out)
        - Test GPIOs : Loopback, between gpio 136 (in) and gpio 139 (out)
        - Test Modem : Send and request pin number (5555)

    What is NOT tested?

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')

    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO0"))
    suite.addTest(TestSerialSlnk0011("test_serial_loopback", "/dev/ttyO1"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO2"))
    suite.addTest(TestGpio('test_loopback', 156, 161,
            'Test GPIOs : Loopback, between gpio 156 (in) and gpio 161 (out)'))
    suite.addTest(TestGpio('test_loopback', 157, 159,
            'Test GPIOs : Loopback, between gpio 157 (in) and gpio 159 (out)'))
    suite.addTest(TestGpio('test_loopback', 130, 131,
            'Test GPIOs : Loopback, between gpio 130 (in) and gpio 131 (out)'))
    suite.addTest(TestGpio('test_loopback', 135, 158,
            'Test GPIOs : Loopback, between gpio 135 (in) and gpio 158 (out)'))
    suite.addTest(TestGpio('test_loopback', 133, 158,
            'Test GPIOs : Loopback, between gpio 133 (in) and gpio 158 (out)'))
    suite.addTest(TestGpio('test_loopback', 132, 162,
            'Test GPIOs : Loopback, between gpio 132 (in) and gpio 162 (out)'))
    suite.addTest(TestGpio('test_loopback', 136, 139,
            'Test GPIOs : Loopback, between gpio 136 (in) and gpio 139 (out)'))
    suite.addTest(TestModemSlnk0011('test_command_at_cpin',
            140, 141, 138, '/dev/ttyO1'))
    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    # By default run using the dbmysql runner.
    suite = dbmysql.dbmysqlTestRunner(verbosity=2)

    # retval = unittest.TestResult()
    retval = suite.run(testsuite_SLNK0011())

    # retval = unittest.TextTestRunner(verbosity=2).run(testsuite_SLNK0011())
    # return 0 if all is ok, otherwise return the number of failures + errors
    sys.exit(len(retval.failures) + len(retval.errors))
