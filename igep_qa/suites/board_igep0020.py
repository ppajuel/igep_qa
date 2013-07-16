#!/usr/bin/env python

import ConfigParser
import unittest
# Test Runners
from igep_qa.runners.dbmysql import dbmysqlTestRunner
# Test Cases
from igep_qa.tests.audio import TestAudio
from igep_qa.tests.bluetooth import TestBluetooth
from igep_qa.tests.network import TestNetwork
from igep_qa.tests.serial import TestSerial
from igep_qa.tests.usb import TestUSB
from igep_qa.tests.wifi import TestWiFi
 
# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_IGEP0020():
    """ A number of TestCases for the IGEP0020 board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code:: ini

        [default]
        serverip = 192.168.13.1
        ipaddr = 192.168.13.11
        
        [wireless]
        serverip = 192.168.6.1
        essid = 'IGEP_TEST'
        
        [mysqld]
        user = root
        host = 192.168.13.1
        database = dbtest

    What is tested?
        - Test audio : IN/OUT loopback.
        - Test Serial : ttyO2 Each sent character should return.
        - Test Serial : ttyO0 Each sent character should return.
        - Test USB HOST: Check for this_is_the_ehci_omap_port file.
        - Test USB OTG: Check for this_is_the_musb_omap_port file.
        - Test Ethernet : Ping the IP address of a remote host.
        - test WiFi: Ping the IP address of a remote host.
        - Test SD-card : Test is running from SD-card (implicit).
        - Test DVI : Test shows the test result. (implicit).

    What is NOT tested?
        - RS-485

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite 
    suite = unittest.TestSuite()
    suite.addTest(TestAudio('test_audio_loopback'))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO2"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO0"))
    suite.addTest(TestUSB('test_ehci_omap'))
    suite.addTest(TestUSB('test_musb_omap'))
    suite.addTest(TestNetwork("test_ping_host",
                                config.get('default', 'ipaddr'),
                                config.get('default', 'serverip'),
                                'eth0'))
    suite.addTest(TestBluetooth('test_get_chip_revision', '/dev/ttyO1'))
    suite.addTest(TestWiFi("test_ping_host",
                           config.get('wireless', 'essid'),
                           config.get('wireless', 'serverip')))
    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    # By default run using the dbmysql runner.
    suite = dbmysqlTestRunner(verbosity=2)
    suite.run(testsuite_IGEP0020())
