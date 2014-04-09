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
from igep_qa.tests.qserial import TestSerial
from igep_qa.tests.qsysfs import TestSysfs

class TestBoardId(unittest.TestCase):
    def test_board_id(self):
        """ Test Board ID : Check for board identification pins.

        Type: Functional

        Description:
            Just read the board identification pins and check if they are
            correctly.

            GPIOS 135 134 133
            Value  1   0   0

        """
        self.failUnless(gpiolib.QGpio(135).get_value() == 1,
                        "failed: Invalid value for gpio 135 (should be 1)")
        self.failUnless(gpiolib.QGpio(134).get_value() == 0,
                        "failed: Invalid value for gpio 134 (should be 0)")
        self.failUnless(gpiolib.QGpio(133).get_value() == 0,
                        "failed: Invalid value for gpio 133 (should be 0)")


# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_SLNK0010():
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

    To configure the SLNK0010 board you should pass following kernel cmdline parameters:

    .. code-block:: ini

        board.ei485=no
        buddy=slnk0010
        omapdss.def_disp=lcd-hvga

    You can run the test at bootup adding:

    .. code-block:: ini

        autotest=SLNK0010 quiet

    What is tested?
        - Test Board ID : Check for board identification pins.
        - Test Serial (/dev/ttyO0): Loopback, each sent character should return
        - Test Serial (/dev/ttyO1): Loopback, each sent character should return
        - Test Serial (/dev/ttyO2): Loopback, each sent character should return
        - Test GPIOs : Loopback, between gpio 156 (in) and gpio 161 (out)
        - Test GPIOs : Loopback, between gpio 157 (in) and gpio 159 (out)
        - Test GPIOs : Loopback, between gpio 136 (in) and gpio 139 (out)
        - Test GPIOs : Loopback, between gpio 138 (in) and gpio 158 (out)
        - Test GPIOs : Loopback, between gpio 137 (in) and gpio 162 (out)
        - Test TSC2046: Check for TOUCH controller at spi1.0

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')

    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestBoardId("test_board_id"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO0"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO1"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO2"))
    suite.addTest(TestGpio('test_loopback', 156, 161,
            'Test GPIOs : Loopback, between gpio 156 (in) and gpio 161 (out)'))
    suite.addTest(TestGpio('test_loopback', 157, 159,
            'Test GPIOs : Loopback, between gpio 157 (in) and gpio 159 (out)'))
    suite.addTest(TestGpio('test_loopback', 136, 139,
            'Test GPIOs : Loopback, between gpio 136 (in) and gpio 139 (out)'))
    suite.addTest(TestGpio('test_loopback', 138, 158,
            'Test GPIOs : Loopback, between gpio 138 (in) and gpio 158 (out)'))
    suite.addTest(TestGpio('test_loopback', 137, 162,
            'Test GPIOs : Loopback, between gpio 137 (in) and gpio 162 (out)'))
    suite.addTest(TestSysfs('test_sysfs_entry',
            '/sys/bus/spi/devices/spi1.0/input',
            testdescription='Test TSC2046: Check for TOUCH controller at spi1.0'))

    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    # Setup test environment, these gpios should be inverted
    gpiolib.QGpio(139).set_active_low(1)

    # By default run using the dbmysql runner.
    suite = dbmysql.dbmysqlTestRunner(verbosity=2)

    # retval = unittest.TestResult()
    retval = suite.run(testsuite_SLNK0010())

    # retval = unittest.TextTestRunner(verbosity=2).run(testsuite_SLNK0010())
    # return 0 if all is ok, otherwise return the number of failures + errors
    sys.exit(len(retval.failures) + len(retval.errors))
