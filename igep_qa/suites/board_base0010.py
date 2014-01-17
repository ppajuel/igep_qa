#!/usr/bin/env python

import ConfigParser
import commands
import sys
import unittest
# Test Runners
from igep_qa.runners import dbmysql
# Test Cases
from igep_qa.tests.qaudio import TestAudio
from igep_qa.tests.qbattery import TestBatteryBackup
from igep_qa.tests.qgpio import TestGpio
from igep_qa.tests.qi2c import TestI2C
from igep_qa.tests.qmodem import TestModem
from igep_qa.tests.qnetwork import TestNetwork
from igep_qa.tests.qserial import TestSerial
from igep_qa.tests.qsysfs import TestSysfs
from igep_qa.tests.qstorage import TestBlockStorage

# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_BASE0010():
    """ A number of TestCases for the BASE0010 board.

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

    You can run the test at bootup adding:

    .. code-block:: ini

        autotest=BASE0010 quiet

    What is tested?
        - Test USB OTG : Check for this_is_an_storage_device file
        - Test USB HOST 1-2.2 : Check for this_is_an_storage_device file
        - Test USB HOST 1-2.3 : Check for this_is_an_storage_device file
        - Test USB HOST 1-2.4 : Check for this_is_an_storage_device file
        - Test Audio : Loopback, sound sent to audio-out should return in audio-in
        - Test EEPROM : Check for EEPROM in bus i2c.3 at address 0x50
        - Test TVP5151 : Check Video decoder in bus i2c.3 at address 0x5d
        - Test MCP251x : Check for CAN controller at spi1.0
        - Test Modem : Send and request pin number (5555)
        - Test Battery Backup : Read battery voltage level
        - Test Serial : Loopback, each sent character should return
        - Test Network (eth0) : Ping the IP address of a remote host
        - Test Network (eth1) : Ping the IP address of a remote host
        - Test Network (eth2) : Ping the IP address of a remote host
        - Test GPIOs : Check loopback between gpio 18 (in) and gpio 14 (out)

    What is NOT tested?
        - BUZZER
        - DINPUT4, ADCIN2, ADCIN3, OUTPUT2, OUTPUT3
        - USB HOST 1-2.1, because conflicts (physically) with the OTG connector.

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestBlockStorage('test_storage_device', 'usb2/2-1/2-1',
            'Test USB OTG: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-2/1-2.2',
            'Test USB HOST 1-2.2: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-2/1-2.3',
            'Test USB HOST 1-2.3: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-2/1-2.4',
            'Test USB HOST 1-2.4: Check for this_is_an_storage_device file'))
    suite.addTest(TestAudio('test_audio_loopback'))
    suite.addTest(TestI2C('test_i2cdetect', 3, '0x50',
            'Test EEPROM: Check for EEPROM in bus i2c.3 at address 0x50'))
    suite.addTest(TestI2C('test_i2cdetect', 3, '0x5d',
            'Test TVP5151: Check Video decoder in bus i2c.3 at address 0x5d'))
    suite.addTest(TestSysfs('test_sysfs_entry',
            '/sys/bus/spi/devices/spi1.0/net/can0',
            testdescription='Test MCP251x: Check for CAN controller at spi1.0'))
    suite.addTest(TestSysfs('test_sysfs_entry',
            '/sys/bus/spi/devices/spi1.1/input',
            testdescription='Test TSC2046: Check for TOUCH controller at spi1.1'))
    suite.addTest(TestModem('test_command_at_cpin',
            163, 145, 170, '/dev/ttyO1'))
    suite.addTest(TestBatteryBackup("test_battery_backup"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO2"))
    suite.addTest(TestNetwork("test_ping_host",
            config.get('default', 'ipaddr'),
            config.get('default', 'serverip'),
            'eth0'))
    suite.addTest(TestNetwork("test_ping_host",
            config.get('default', 'ipaddr'),
            config.get('default', 'serverip'),
            'eth1'))
    suite.addTest(TestNetwork("test_ping_host",
            config.get('default', 'ipaddr'),
            config.get('default', 'serverip'),
            'eth2'))
    suite.addTest(TestGpio('test_loopback', 18, 14,
            'Test GPIOs: Check loopback between gpio 18 (in) and gpio 14 (out)'))
    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    # By default run using the dbmysql runner.
    suite = dbmysql.dbmysqlTestRunner(verbosity=2)
    retval = unittest.TestResult()

    # Workarounds for kernel 2.6.37:
    #   Force loading tvp5151 video decoder driver
    commands.getoutput('modprobe omap3-isp')

    retval = suite.run(testsuite_BASE0010())
    # unittest.TextTestRunner(verbosity=2).run(testsuite_BASE0010())

    # return 0 if all is ok, otherwise return the number of failures + errors
    sys.exit(len(retval.failures) + len(retval.errors))
