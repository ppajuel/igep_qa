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
from igep_qa.tests.qflash import TestFlash

# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_IGEP0033():
    """ A number of TestCases for the IGEP0033 board.

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

    To run the autotest you should replace u-boot.img with and special
    version with boot delay set to 0, otherwise the boot process stops
    when you shortcut TX and RX from serial port. See patch below:

    .. code-block:: diff

        diff --git a/include/configs/igep0033.h b/include/configs/igep0033.h
        index de60f75..fa231ed 100644
        --- a/include/configs/igep0033.h
        +++ b/include/configs/igep0033.h
        @@ -66,7 +66,7 @@
        #define CONFIG_UBI_SILENCE_MSG
        #define CONFIG_UBIFS_SILENCE_MSG

       -#define CONFIG_BOOTDELAY               1       /* negative for no autoboot */
       +#define CONFIG_BOOTDELAY               0       /* negative for no autoboot */

        #define CONFIG_ENV_VARS_UBOOT_CONFIG
        #define CONFIG_ENV_VARS_UBOOT_RUNTIME_CONFIG
        #define CONFIG_EXTRA_ENV_SETTINGS

    You can run the test at bootup adding:

    .. code-block:: ini

        autotest=IGEP0033 quiet

    As example, for u-boot you can create a uEnv.txt and set mmcargs like this:

    .. code-block:: ini

        mmcargs=setenv bootargs console=${console} autotest=IGEP0033 quiet root=${mmcroot} rootfstype=${mmcrootfstype}

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
    suite.addTest(TestFlash('test_nandtest', '/dev/mtd3'))
    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    #from igep_qa.runners import simple
    #suite =  simple.SimpleTestRunner()
    #suite.run(testsuite_IGEP0033())

    # By default run using the dbmysql runner.
    suite = dbmysql.dbmysqlTestRunner(verbosity=2)
    suite.run(testsuite_IGEP0033())
