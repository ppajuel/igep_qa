#!/usr/bin/env python

import ConfigParser
import errno
import sys
import unittest
# Test Runners
from igep_qa.runners import dbmysql
# Test Helpers
from igep_qa.helpers import am33xx
# Test Cases
from igep_qa.tests.qbutton import TestButton
from igep_qa.tests.qpower import TestPower
from igep_qa.tests.qi2c import TestI2C
from igep_qa.tests.qserial import TestSerial
from igep_qa.tests.qstorage import TestBlockStorage
from igep_qa.tests.qaudio import TestAudio
from igep_qa.tests.qnetwork import TestNetwork
from igep_qa.tests.qwifi import TestWiFi
from igep_qa.tests.qflash import TestFlash
from igep_qa.tests.qbluetooth import TestBluetooth

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

        [wireless]
        serverip = 192.168.1.1
        ipaddr = 192.168.1.60
        essid = 'your_essid'
        password = 'your_password'

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
        - Test Button Fbtest : Read User button action and display fb-test pattern
        - Test Power : Check the maximum acceptable limit of current
        - Test TPS65910: Check for PMIC in bus 1 at address 0x2d
        - Test EEPROM: Check for EEPROM in bus 1 at address 0x50
        - Test Audio : Loopback, sound sent to audio-out should return in audio-in
        - Test Serial : ttyO0 Each sent character should return
        - Test Serial : ttyO3 Each sent character should return
        - Test Serial : ttyO5 Each sent character should return
        - Test USB HOST 2-1.1 : Check for this_is_an_storage_device file
        - Test USB HOST 2-1.2 : Check for this_is_an_storage_device file
        - Test USB HOST 2-1.3 : Check for this_is_an_storage_device file
        - Test USB OTG 1-1:1.0: Check for this_is_an_storage_device file
        - Test Network (eth0) : Ping the IP address of a remote host
        - Test WiFi : Ping the IP address of a remote host (adhoc+wep)
        - Test Bluetooth : Get Link Manager Protocol (LMP) revision
        - Test ubifsfirmware : Read some files from UBIFS partition to ensure firmware flashed
        - Test SD-card : Test is running from SD-card (implicit)
        - Test HDMI : Test shows the test result (implicit)

    What is NOT tested?
        - Gigabit Ethernet
        - CAN bus
        - Test ADC: get  AIN0-AIN6 values
        - Test TPS65910 RTC: Check for PMIC RTC is active (RTC_STATUS_REG:RUN bit)

    .. warning::

        IGEP0034-RA&BASE0040-RB needs an external 12 MHz 1V8
        oscillator attached to J1003:22 to test audio correctly
    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestButton("test_button_fbtest", 104))
    suite.addTest(TestNetwork("test_ping_host",
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            'eth0'))
    suite.addTest(TestPower('test_max_current',
                            0.75,
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            9999,
                            'eth0'))
    suite.addTest(TestI2C('test_i2cdetect', 1, '0x2d', '',
        'Test TPS65910: Check for PMIC in bus 1 at address 0x2d'))
    suite.addTest(TestI2C('test_i2cdetect', 1, '0x50', '',
        'Test EEPROM: Check for EEPROM in bus 1 at address 0x50'))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO0"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO3"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO5"))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb2/2-1/2-1.1',
        'Test USB HOST 2-1.1: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb2/2-1/2-1.2',
        'Test USB HOST 2-1.2: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb2/2-1/2-1.3',
        'Test USB HOST 2-1.3: Check for this_is_an_storage_device file'))
    suite.addTest(TestAudio('test_audio_loopback'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-1/1-1:1.0',
        'Test USB OTG 1-1:1.0: Check for this_is_an_storage_device file'))
    suite.addTest(TestWiFi("test_ap_with_wep_encryption",
                            config.get('wireless', 'serverip'),
                            config.get('wireless', 'essid'),
                            config.get('wireless', 'ipaddr'),
                            config.get('wireless', 'password')))
    suite.addTest(TestBluetooth('test_get_lmp_revision','','','0xac7c'))
    suite.addTest(TestFlash('test_ubifsfirmware', '/dev/mtd3',
        '/boot/zImage',
        '/boot/MLO',
        '/boot/u-boot.img'))

    return suite

def testsuite_IGEP0034_LITE():
    """ A number of TestCases for the IGEP0034 Lite board.

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

    To run the autotest you should replace am335x-igep-base0040-lite.dtb
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

    As example, for u-boot you can create a uEnv.txt and set mmcargs with the kernel parameters explained above:

    .. code-block:: ini

        mmcargs=setenv bootargs console=${console} consoleblank=0 autotest=IGEP0034 quiet ${optargs} root=${mmcroot} rootfstype=${mmcrootfstype} bootenv=uEnv.txt

    If you want to pass test during bootup, you need to add a symbolic link to igep-qa.sh

    .. code-block:: ini

        ln -sf /usr/bin/igep-qa.sh /etc/rc5.d/S99igep-qa.sh

    What is tested?
        - Test Button : Read User button action
        - Test Power : Check the maximum acceptable limit of current
        - Test TPS65910: Check for PMIC in bus 1 at address 0x2d
        - Test EEPROM: Check for EEPROM in bus 1 at address 0x50
        - Test Audio : Loopback, sound sent to audio-out should return in audio-in
        - Test Serial : ttyO3 Each sent character should return
        - Test Serial : ttyO5 Each sent character should return
        - Test USB HOST 2-1.1 : Check for this_is_an_storage_device file
        - Test USB HOST 2-1.2 : Check for this_is_an_storage_device file
        - Test USB HOST 2-1.3 : Check for this_is_an_storage_device file
        - Test USB OTG 1-1:1.0: Check for this_is_an_storage_device file
        - Test Network (eth0) : Ping the IP address of a remote host
        - Test WiFi : Ping the IP address of a remote host (adhoc+wep)
        - Test Bluetooth : Get Link Manager Protocol (LMP) revision
        - Test ubifsfirmware : Read some files from UBIFS partition to ensure firmware flashed
        - Test SD-card : Test is running from SD-card (implicit)
        - Test Serial : Test shows the test result (implicit)

    What is NOT tested?
        - Gigabit Ethernet
        - CAN bus
        - Test ADC: get  AIN0-AIN6 values
        - Test TPS65910 RTC: Check for PMIC RTC is active (RTC_STATUS_REG:RUN bit)

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestButton("test_button", 104))
    suite.addTest(TestNetwork("test_ping_host",
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            'eth0'))
    suite.addTest(TestPower('test_max_current',
                            0.58,
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            9999,
                            'eth0'))
    suite.addTest(TestI2C('test_i2cdetect', 1, '0x2d', '',
        'Test TPS65910: Check for PMIC in bus 1 at address 0x2d'))
    suite.addTest(TestI2C('test_i2cdetect', 1, '0x50', '',
        'Test EEPROM: Check for EEPROM in bus 1 at address 0x50'))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO3"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO5"))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb2/2-1/2-1.1',
        'Test USB HOST 2-1.1: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb2/2-1/2-1.2',
        'Test USB HOST 2-1.2: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb2/2-1/2-1.3',
        'Test USB HOST 2-1.3: Check for this_is_an_storage_device file'))
    suite.addTest(TestAudio('test_audio_loopback'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-1/1-1:1.0',
        'Test USB OTG 1-1:1.0: Check for this_is_an_storage_device file'))
    suite.addTest(TestWiFi("test_ap_with_wep_encryption",
                            config.get('wireless', 'serverip'),
                            config.get('wireless', 'essid'),
                            config.get('wireless', 'ipaddr'),
                            config.get('wireless', 'password')))
    suite.addTest(TestBluetooth('test_get_lmp_revision','','','0xac7c'))
    suite.addTest(TestFlash('test_ubifsfirmware', '/dev/mtd3',
        '/boot/zImage',
        '/boot/MLO',
        '/boot/u-boot.img'))

    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    args = sys.argv[1:]
    # Do some things to prepare the test environment.
    am33xx.igep0034_set_headset_amixer_settings(0)
    if len(args) == 0:
        # IGEP0034-RA20 (FULL)
        # By default run using the dbmysql runner.
        suite = dbmysql.dbmysqlTestRunner(verbosity=2)
        retval = unittest.TestResult()
        retval = suite.run(testsuite_IGEP0034())
    elif args[0] == "LITE" :
        # IGEP0034-RA10 (LITE)
        # By default run using the dbmysql runner.
        suite = dbmysql.dbmysqlTestRunner(verbosity=2)
        retval = unittest.TestResult()
        retval = suite.run(testsuite_IGEP0034_LITE())

    # return 0 if all is ok, otherwise return the number of failures + errors
    sys.exit(len(retval.failures) + len(retval.errors))