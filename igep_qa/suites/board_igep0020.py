#!/usr/bin/env python

import ConfigParser
import commands
import sys
import unittest
# Test Runners
from igep_qa.runners.dbmysql import dbmysqlTestRunner
# Test Cases
from igep_qa.tests.qaudio import TestAudio
from igep_qa.tests.qbattery import TestBatteryBackup
from igep_qa.tests.qbluetooth import TestBluetooth
from igep_qa.tests.qnetwork import TestNetwork
from igep_qa.tests.qserial import TestSerial
from igep_qa.tests.qusb import TestUSB
from igep_qa.tests.qwifi import TestWiFi

# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_IGEP0020():
    """ A number of TestCases for the IGEP0020 board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code-block:: ini

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

    Before executing the Test Suite make sure that you have disabled any buddy
    option and configure UART1 to be used as a serial device.

    .. code-block:: bash

        board.ei485=no

    Also, make sure getty is not running in any ttyO2 port when the test runs.
    If it is necessary modify /etc/inittab file an comment following line:

    .. code-block:: ini

        S:2345:respawn:/sbin/getty 115200 ttyO2

    You can run the test at bootup adding:

    .. code-block:: ini

        autotest=IGEP0020 quiet

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

def testsuite_IGEP0020_RC80C01():
    """ A number of TestCases for the IGEP0020 RC80-C01 board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code-block:: ini

        [default]
        serverip = 192.168.13.1
        ipaddr = 192.168.13.11

        [remotex]
        ipaddr = 192.168.13.5

        [mysqld]
        user = root
        host = 192.168.13.1
        database = dbtest

    Make sure getty is not running in any ttyO2 port when the test runs.
    If it is necessary modify /etc/inittab file an comment following line:

    .. code-block:: ini

        S:2345:respawn:/sbin/getty 115200 ttyO2

    You can run the test at bootup adding:

    .. code-block:: ini

        autotest=IGEP0020_RC80C01 quiet

    What is tested?
        - Test Audio : Loopback, sound sent to audio-out should return in audio-in
        - Test Network (eth0): Ping the IP address of a remote host
        - Test Serial (/dev/ttyO2): Loopback, each sent character should return
        - Test USB OTG : Check for this_is_the_musb_omap_port file
        - Test USB HOST : Check for this_is_the_ehci_omap_port file
        - Test SD-card : Test is running from SD-card (implicit).

    As this board doesn't have DVI output, the results are sent to the server
    via ssh.

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    ipaddr = config.get("default", "ipaddr")
    serverip = config.get("default", "serverip")
    xserverip = config.get("remotex", "ipaddr")

    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestAudio("test_audio_loopback"))
    suite.addTest(TestBatteryBackup("test_battery_backup"))
    suite.addTest(TestNetwork("test_ping_host", ipaddr, serverip, "eth0"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO2"))
    suite.addTest(TestUSB("test_ehci_omap"))
    suite.addTest(TestUSB("test_musb_omap"))

    # log the Test Suite output
    log_file = "/tmp/log_test.txt"
    f = open(log_file, "w")
    # write the IP address in the head of the log file
    f.write("%s\n" % ipaddr)

    # run test
    runner = dbmysqlTestRunner(stream=f, verbosity=2)
    retval = runner.run(suite)
    # close the log
    f.close()

    # send result to the server
    commands.getstatusoutput("ifconfig eth0 %s" % ipaddr)
    commands.getstatusoutput("scp %s root@%s:/tmp" % (log_file, xserverip))
    commands.getstatusoutput("ssh -y root@%s xterm -display :0 "
                            "-fg white -bg black "
                            "-e /usr/share/igep_qa/contrib/show-results.sh "
                            % xserverip)
    return retval

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    args = sys.argv[1:]

    if args[0] == "RC80C01" :
        retval = testsuite_IGEP0020_RC80C01()
    else :
        # By default run using the dbmysql runner.
        suite = dbmysqlTestRunner(verbosity=2)
        retval = suite.run(testsuite_IGEP0020())
    # return 0 if all is ok, otherwise return the number of failures + errors
    sys.exit(len(retval.failures) + len(retval.errors))

