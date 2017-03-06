#!/usr/bin/env python

import ConfigParser
import errno
import sys
import unittest
# Test Runners
from igep_qa.runners import dbmysql
# Test Cases
from igep_qa.tests.qi2c import TestI2C
from igep_qa.tests.qserial import TestSerial

# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_IGEP0034():
    """ A number of TestCases for the IGEP0034 (FULL) board.

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

    To run the autotest you should replace am335x-igep-base0040.dtb
    with and special version with usb0 dr_mode parameter set to "host",
    otherwise the autotest USB OTG will always fail. See patch below:

    .. code-block:: diff

        diff --git a/arch/arm/boot/dts/am335x-igep-igep0034-lite.dtsi b/arch/arm/boot/dts/am335x-igep-igep0034-lite.dtsi
        index d67ce0b..29cb702 100644
        --- a/arch/arm/boot/dts/am335x-igep-igep0034-lite.dtsi
        +++ b/arch/arm/boot/dts/am335x-igep-igep0034-lite.dtsi
        @@ -536,7 +536,7 @@
 
         &usb0 {
                status = "okay";
        -       dr_mode = "otg";
        +       dr_mode = "host";
         };
 
         &usb1 {

    You can run the test at bootup adding into kernel parameters:

    .. code-block:: ini

        autotest=IGEP0034 quiet

    And you can disable the console blank (screen saver) timeout adding into kernel parameters:

    .. code-block:: ini

        consoleblank=0

    As example, for u-boot you can create a uEnv.txt and set mmcargs with the kernel parameters explained above:

    .. code-block:: ini

        mmcargs=setenv bootargs console=${console} consoleblank=0 autotest=IGEP0034 quiet ${optargs} root=${mmcroot} rootfstype=${mmcrootfstype} bootenv=uEnv.txt 

    If you want to pass test during bootup, you need to add a symbolic link to igep-qa.sh

    .. code-block:: ini

        ln -sf /usr/bin/igep-qa.sh /etc/rc5.d/S99igep-qa.sh

    What is tested?
        - Test Power : Check the maximum acceptable limit of current
        - Test TPS65910: Check for PMIC in bus 1 at address 0x2d
        - Test TPS65910 RTC: Check for PMIC RTC is active (RTC_STATUS_REG:RUN bit)
        - Test EEPROM: Check for PMIC in bus 1 at address 0x50
        - Test Audio : IN/OUT loopback using headphone and line-in signals
        - Test Serial : ttyO0 Each sent character should return
        - Test Serial : ttyO3 Each sent character should return
        - Test Serial : ttyO5 Each sent character should return
        - Test USB HOST 1-J600A : Check for this_is_an_storage_device file
        - Test USB HOST 2-J600B : Check for this_is_an_storage_device file
        - Test USB HOST 3-J601 : Check for this_is_an_storage_device file
        - Test USB OTG J602: Check for this_is_an_storage_device file
        - Test Fast Ethernet : Ping the IP address of a remote host
        - Test WiFi: Ping the IP address of a remote AP
        - Test Bluetooth: Check Bluetooth at ttyO2
        - Test Flash: detect firmware flashed
        - Test ADC: get  AIN0-AIN6 values
        - Test SD-card : Test is running from SD-card (implicit)
        - Test HDMI : Test shows the test result (implicit)

    What is NOT tested?
        - Gigabit Ethernet
        - CAN bus

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestI2C('test_i2cdetect', 1, '0x2d',
        'Test TPS65910: Check for PMIC in bus 1 at address 0x2d'))
    suite.addTest(TestI2C('test_i2cdetect', 1, '0x50',
        'Test EEPROM: Check for PMIC in bus 1 at address 0x50'))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO0"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO3"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO5"))
    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    # TODO : Set amixer configuration
    args = sys.argv[1:]
    if len(args) == 0:
        # IGEP0034-RA20 (FULL)
        # By default run using the dbmysql runner.
        suite = dbmysql.dbmysqlTestRunner(verbosity=2)
        retval = unittest.TestResult()
        retval = suite.run(testsuite_IGEP0034())
    elif args[0] == "LITE" :
        # IGEP0034-RA10 (LITE)
        # TODO : Set a runner without display
        retval = suite.run(testsuite_IGEP0034_LITE())

    # return 0 if all is ok, otherwise return the number of failures + errors
    sys.exit(len(retval.failures) + len(retval.errors))