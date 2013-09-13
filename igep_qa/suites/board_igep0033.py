#!/usr/bin/env python

import ConfigParser
import unittest
# Test Runners
from igep_qa.runners import dbmysql
# Test Cases
from igep_qa.tests.qaudio import TestAudio
from igep_qa.tests.qnetwork import TestNetwork
from igep_qa.tests.qserial import TestSerial
from igep_qa.tests.qusb import TestUSB

# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_IGEP0033():
    """ A number of TestCases for the IGEP0033 board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code:: ini

        [default]
        serverip = 192.168.13.1
        ipaddr = 192.168.13.11

        [mysqld]
        user = root
        host = 192.168.13.1
        database = dbtest

    Also, make sure getty is not running in any ttyO0 port, modify /etc/inittab
    file an comment following line:

    .. code:: ini

        S:2345:respawn:/sbin/getty 115200 ttyO0

    You can run the test at bootup adding:

    .. code:: ini

        autotest=IGEP0033 quiet

    What is tested?
        - Test audio : Play a wav file (user check)
        - Test Serial : ttyO0 Each sent character should return
        - Test USB HOST: Check for this_is_the_musb_hdrc_port file
        - Test Ethernet : Ping the IP address of a remote host
        - Test SD-card : Test is running from SD-card (implicit)
        - Test HDMI : Test shows the test result (implicit)

    What is NOT tested?
        - USB OTG

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestAudio('test_audio_playwav'))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO0"))
    suite.addTest(TestUSB('test_musb_hdrc'))
    suite.addTest(TestNetwork("test_ping_host",
                                config.get('default', 'ipaddr'),
                                config.get('default', 'serverip'),
                                'eth0'))
    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    #from igep_qa.runners import simple
    #suite =  simple.SimpleTestRunner()
    #suite.run(testsuite_IGEP0033())

    # By default run using the dbmysql runner.
    suite = dbmysql.dbmysqlTestRunner(verbosity=2)
    suite.run(testsuite_IGEP0033())
