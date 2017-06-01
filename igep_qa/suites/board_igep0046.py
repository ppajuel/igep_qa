#!/usr/bin/env python

import ConfigParser
import errno
import sys
import unittest
# Test Runners
from igep_qa.runners import dbmysql
# Test Helpers
from igep_qa.helpers import imx6
# Test Cases
from igep_qa.tests.qnetwork import TestNetwork
from igep_qa.tests.qpower import TestPower
from igep_qa.tests.qserial import TestSerial
from igep_qa.tests.qaudio import TestAudio
from igep_qa.tests.qi2c import TestI2C

# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_IGEP0046_QuadC2():
    """ A number of TestCases for the IGEP0046RC02(and RD) board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code-block:: ini

        [default]
        serverip = 192.168.13.1
        ipaddr = 192.168.13.11

        [mysqld]
        user = root
        host = 192.168.13.1
        database = dbtest

        [wireless]
        serverip = 192.168.1.1
        ipaddr = 192.168.1.60
        essid = 'your_essid'
        password = 'your_password'

    You can run the test at bootup adding into kernel parameters:

    .. code-block:: ini

        autotest=IGEP0046 quiet

    And you can disable the console blank (screen saver) timeout adding into kernel parameters:

    .. code-block:: ini

        consoleblank=0

    As example, for u-boot you can create a uEnv.txt and set mmcargs with the kernel parameters explained above:

    .. code-block:: ini

        mmcargs=setenv bootargs console=${console},${baudrate} consoleblank=0 autotest=IGEP0046 quiet root=${mmcroot} ${video_args}

    If you want to pass test during bootup, you need to add a symbolic link to igep-qa.sh

    .. code-block:: ini

        ln -sf /usr/bin/igep-qa.sh /etc/rc5.d/S99igep-qa.sh

    What is tested?
        - Test Power : Check the maximum acceptable limit of current
        - Test Network (eth0) : Ping the IP address of a remote host
        - Test Audio : Loopback, sound sent to audio-out should return in audio-in
        - Test Serial : ttymxc1 Each sent character should return
        - Test Serial : ttymxc3 Each sent character should return
        - Test MMPF0100F0A: Check for PMIC in bus 1 at address 0x08 and register 0x00
        - Test TLV320AIC3106: Check for Expansion audio codec in bus 2 at address 0x1b
        - Test EEPROM: Check for EEPROM in bus 2 at address 0x50
        - Test SD-card : Test is running from SD-card (implicit)
        - Test HDMI : Test shows the test result (implicit)

    What is NOT tested?
        - CAN bus

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestNetwork("test_ping_host",
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            'eth0'))
    suite.addTest(TestPower('test_max_current',
                            0.55,
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            9999,
                            'eth0'))
    suite.addTest(TestAudio('test_audio_loopback'))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttymxc1"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttymxc3"))
    suite.addTest(TestI2C('test_i2cget', 1, '0x08', '0x00',
        'Test MMPF0100F0A: Check for PMIC in bus 1 at address 0x08 and register 0x00'))
    suite.addTest(TestI2C('test_i2cdetect', 2, '0x1b',
        'Test TLV320AIC3106: Check for Expansion audio codec in bus 2 at address 0x1b'))
    suite.addTest(TestI2C('test_i2cdetect', 2, '0x50',
        'Test EEPROM: Check for EEPROM in bus 2 at address 0x50'))

    return suite

def testsuite_IGEP0034_DualLiteD102():
    """ A number of TestCases for the IGEP0046-RD10 board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code-block:: ini

        [default]
        serverip = 192.168.13.1
        ipaddr = 192.168.13.11

        [mysqld]
        user = root
        host = 192.168.13.1
        database = dbtest

    You can run the test at bootup adding into kernel parameters:

    .. code-block:: ini

        autotest=IGEP0046 quiet

    And you can disable the console blank (screen saver) timeout adding into kernel parameters:

    .. code-block:: ini

        consoleblank=0

    As example, for u-boot you can create a uEnv.txt and set mmcargs with the kernel parameters explained above:

    .. code-block:: ini

        mmcargs=setenv bootargs console=${console},${baudrate} consoleblank=0 autotest=IGEP0046 quiet root=${mmcroot} ${video_args}

    If you want to pass test during bootup, you need to add a symbolic link to igep-qa.sh

    .. code-block:: ini

        ln -sf /usr/bin/igep-qa.sh /etc/rc5.d/S99igep-qa.sh

    What is tested?
        - Test Power : Check the maximum acceptable limit of current
        - Test Network (eth0) : Ping the IP address of a remote host
        - Test Audio : Loopback, sound sent to audio-out should return in audio-in
        - Test Serial : ttymxc0 Each sent character should return
        - Test Serial : ttymxc1 Each sent character should return
        - Test Serial : ttymxc3 Each sent character should return
        - Test SD-card : Test is running from SD-card (implicit)
        - Test HDMI : Test shows the test result (implicit)

    What is NOT tested?
        - CAN bus

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestNetwork("test_ping_host",
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            'eth0'))
    suite.addTest(TestPower('test_max_current',
                            0.55,
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            9999,
                            'eth0'))
    suite.addTest(TestAudio('test_audio_loopback'))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttymxc0"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttymxc1"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttymxc3"))

    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    # TODO : Set amixer configuration
    args = sys.argv[1:]
    # Do some things to prepare the test environment.
    imx6.igep0046_set_headset_amixer_settings(0)
    if len(args) == 0:
        # IGEP0046 always must be pass an argument
        raise Exception("IGEP0046 testsuite: an argument is requited")
    elif args[0] == "QuadC2" :
        # By default run using the dbmysql runner.
        suite = dbmysql.dbmysqlTestRunner(verbosity=2)
        retval = unittest.TestResult()
        retval = suite.run(testsuite_IGEP0046_QuadC2())
    elif args[0] == "DualLiteD102" :
        # By default run using the dbmysql runner.
        suite = dbmysql.dbmysqlTestRunner(verbosity=2)
        retval = unittest.TestResult()
        retval = suite.run(testsuite_IGEP0034_DualLiteD102())
    # return 0 if all is ok, otherwise return the number of failures + errors
    sys.exit(len(retval.failures) + len(retval.errors))