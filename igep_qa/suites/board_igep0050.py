#!/usr/bin/env python

import ConfigParser
import sys
import unittest
# Test Helpers
from igep_qa.helpers import omap
# Test Runners
from igep_qa.runners import dbmysql
# Test Cases
from igep_qa.tests.qaudio import TestAudio
from igep_qa.tests.qbluetooth import TestBluetooth
from igep_qa.tests.qhwmon import TestHwmon
from igep_qa.tests.qi2c import TestI2C
from igep_qa.tests.qnetwork import TestNetwork
from igep_qa.tests.qserial import TestSerial
from igep_qa.tests.qsysfs import TestSysfs
from igep_qa.tests.qstorage import TestBlockStorage
from igep_qa.tests.qwifi import TestWiFi

# For every test suite we create an instance of TestSuite and add test case
# instances. When all tests have been added, the suite can be passed to a test
# runner, such as TextTestRunner. It will run the individual test cases in the
# order in which they were added, aggregating the results.

def testsuite_IGEP0050():
    """ A number of TestCases for the IGEP0050 board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code-block:: ini

        [default]
        serverip = 192.168.13.1
        ipaddr = 192.168.13.11
        
        [wireless]
        serverip = 192.168.6.1
        essid = IGEP_TEST

        [mysqld]
        user = root
        host = 192.168.13.1
        database = dbtest

    To run the autotest you should replace u-boot.img with and special
    version with boot delay set to 0, otherwise the boot process stops
    when you shortcut TX and RX from serial port. See patch below:

    .. code-block:: diff

       -#define CONFIG_BOOTDELAY               1       /* negative for no autoboot */
       +#define CONFIG_BOOTDELAY               0       /* negative for no autoboot */

    You can run the test at bootup adding:

    .. code-block:: ini

        autotest=IGEP0050 quiet

    As example, for u-boot you can create a uEnv.txt and set mmcargs like this:

    .. code-block:: ini

        mmcargs=setenv bootargs console=${console} autotest=IGEP0050 quiet root=${mmcroot} rootfstype=${mmcrootfstype}

    What is tested?
        - Test SATA: Check for this_is_an_storage_device file
        - Test USB HOST 1-2.1: Check for this_is_an_storage_device file
        - Test USB HOST 1-2.2: Check for this_is_an_storage_device file
        - Test USB HOST 1-3.1: Check for this_is_an_storage_device file
        - Test USB HOST 1-3.2: Check for this_is_an_storage_device file
        - Test Audio HDMI: Play a wav file
        - Test Audio JACK: Loopback, sound sent to audio-out should return in audio-in
        - Test CPU TEMP: Check temperature is in range 40-70 degree
        - Test PALMAS: Check for PMIC in bus 0 at address 0x48
        - Test TWL6040: Check for audio codec in bus 0 at address 0x4b
        - Test EEPROM: Check for EEPROM in bus 0 at address 0x50
        - Test TMP102: Check for temperature sensor in bus 1 at address 0x48
        - Test TCA6416: Check for IO expander in bus 3 at address 0x21
        - Test SEM08G: Check for eMMC (8G) block device
        - Test Serial : Loopback, each sent character should return
        - Test WiFi : Scan for ESSID network
        - Test Bluetooth : Attach serial devices via UART HCI to BlueZ stack
        - Test Network : Ping the IP address of a remote host

    What is NOT tested?
        - USER BUTTON
        - USER LEDS
        - USB 3.0 CONNECTOR
        - RTC BATTERY

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # Do some things to prepare the test environment.
    omap.igep0050_power_up_bluetooth()
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestBlockStorage('test_storage_device', 'ata1/host0',
        'Test SATA: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-2/1-2.1',
        'Test USB HOST 1-2.1: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-2/1-2.2',
        'Test USB HOST 1-2.2: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-3/1-3.1',
        'Test USB HOST 1-3.1: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-3/1-3.2',
        'Test USB HOST 1-3.2: Check for this_is_an_storage_device file'))
    suite.addTest(TestAudio('test_audio_playwav',
        testdescription='Test Audio HDMI: Play a wav file'))
    suite.addTest(TestAudio('test_audio_loopback', 'plughw:1,0',
        'Test Audio JACK: Loopback, sound sent to audio-out should return in audio-in'))
    suite.addTest(TestHwmon('test_temperature_range', 
        '/sys/class/hwmon/hwmon0/temp1_input', 25000, 70000,
        'Test CPU TEMP: Check temperature is in range 40-70 degree'))
    suite.addTest(TestI2C('test_i2cdetect', 0, '0x48',
        'Test PALMAS: Check for PMIC in bus 0 at address 0x48'))
    suite.addTest(TestI2C('test_i2cdetect', 0, '0x4b',
        'Test TWL6040: Check for audio codec in bus 0 at address 0x4b'))
    suite.addTest(TestI2C('test_i2cdetect', 0, '0x50',
        'Test EEPROM: Check for EEPROM in bus 0 at address 0x50'))
    suite.addTest(TestI2C('test_i2cdetect', 1, '0x48',
        'Test TMP102: Check for temperature sensor in bus 1 at address 0x48'))
    suite.addTest(TestI2C('test_i2cdetect', 3, '0x21',
        'Test TCA6416: Check for IO expander in bus 3 at address 0x21'))
    suite.addTest(TestSysfs('test_device_name',
        '/sys/block/mmcblk1/device', 'SEM08G',
        'Test SEM08G: Check for eMMC (8G) block device'))
    suite.addTest(TestWiFi("test_scan_for_essid",
                           config.get('wireless', 'essid'),
                           config.get('wireless', 'serverip')))
    suite.addTest(TestBluetooth("test_attach_uart_hci", "/dev/ttyO4",
                           "-s 115200 texas 3000000"))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO2"))
    suite.addTest(TestNetwork("test_ping_host",
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            'eth0'))
    return suite

def testsuite_IGEP0050_RB20():
    """ A number of TestCases for the IGEP0050-RB20 board.

    The test Suite requires a configuration file /etc/testsuite.conf that consists of
    different sections in RFC 822. E.g.

    .. code-block:: ini

        [default]
        serverip = 192.168.13.1
        ipaddr = 192.168.13.11
        
        [wireless]
        serverip = 192.168.6.1
        essid = IGEP_TEST

        [mysqld]
        user = root
        host = 192.168.13.1
        database = dbtest

    To run the autotest you should replace u-boot.img with and special
    version with boot delay set to 0, otherwise the boot process stops
    when you shortcut TX and RX from serial port. See patch below:

    .. code-block:: diff

       -#define CONFIG_BOOTDELAY               1       /* negative for no autoboot */
       +#define CONFIG_BOOTDELAY               0       /* negative for no autoboot */

    You can run the test at bootup adding:

    .. code-block:: ini

        autotest=IGEP0050_RB20 quiet

    As example, for u-boot you can create a uEnv.txt and set mmcargs like this:

    .. code-block:: ini

        mmcargs=setenv bootargs console=${console} autotest=IGEP0050_RB20 quiet root=${mmcroot} rootfstype=${mmcrootfstype}

    What is tested?
        - Test SATA: Check for this_is_an_storage_device file
        - Test USB HOST 1-2.1: Check for this_is_an_storage_device file
        - Test USB HOST 1-2.2: Check for this_is_an_storage_device file
        - Test USB HOST 1-3.1: Check for this_is_an_storage_device file
        - Test USB HOST 1-3.2: Check for this_is_an_storage_device file
        - Test Audio HDMI: Play a wav file
        - Test Audio JACK: Loopback, sound sent to audio-out should return in audio-in
        - Test CPU TEMP: Check temperature is in range 40-70 degree
        - Test PALMAS: Check for PMIC in bus 0 at address 0x48
        - Test TWL6040: Check for audio codec in bus 0 at address 0x4b
        - Test EEPROM: Check for EEPROM in bus 0 at address 0x50
        - Test TMP102: Check for temperature sensor in bus 1 at address 0x48
        - Test TCA6416: Check for IO expander in bus 3 at address 0x21
        - Test Serial : Loopback, each sent character should return
        - Test Network : Ping the IP address of a remote host

    What is NOT tested?
        - USER BUTTON
        - USER LEDS
        - USB 3.0 CONNECTOR
        - RTC BATTERY

    """
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    config.read('/etc/testsuite.conf')
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestBlockStorage('test_storage_device', 'ata1/host0',
        'Test SATA: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-2/1-2.1',
        'Test USB HOST 1-2.1: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-2/1-2.2',
        'Test USB HOST 1-2.2: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-3/1-3.1',
        'Test USB HOST 1-3.1: Check for this_is_an_storage_device file'))
    suite.addTest(TestBlockStorage('test_storage_device', 'usb1/1-3/1-3.2',
        'Test USB HOST 1-3.2: Check for this_is_an_storage_device file'))
    suite.addTest(TestAudio('test_audio_playwav',
        testdescription='Test Audio HDMI: Play a wav file'))
    suite.addTest(TestAudio('test_audio_loopback', 'plughw:1,0',
        'Test Audio JACK: Loopback, sound sent to audio-out should return in audio-in'))
    suite.addTest(TestHwmon('test_temperature_range', 
        '/sys/class/hwmon/hwmon0/temp1_input', 25000, 50000,
        'Test CPU TEMP: Check temperature is in range 30-60 degree'))
    suite.addTest(TestI2C('test_i2cdetect', 0, '0x48',
        'Test PALMAS: Check for PMIC in bus 0 at address 0x48'))
    suite.addTest(TestI2C('test_i2cdetect', 0, '0x4b',
        'Test TWL6040: Check for audio codec in bus 0 at address 0x4b'))
    suite.addTest(TestI2C('test_i2cdetect', 0, '0x50',
        'Test EEPROM: Check for EEPROM in bus 0 at address 0x50'))
    suite.addTest(TestI2C('test_i2cdetect', 1, '0x48',
        'Test TMP102: Check for temperature sensor in bus 1 at address 0x48'))
    suite.addTest(TestI2C('test_i2cdetect', 3, '0x21',
        'Test TCA6416: Check for IO expander in bus 3 at address 0x21'))
    suite.addTest(TestSerial("test_serial_loopback", "/dev/ttyO2"))
    suite.addTest(TestNetwork("test_ping_host",
                            config.get('default', 'ipaddr'),
                            config.get('default', 'serverip'),
                            'eth0'))
    return suite

# The main program just runs the test suite in verbose mode
if __name__ == '__main__':
    args = sys.argv[1:]
    # By default run using the dbmysql runner.
    suite = dbmysql.dbmysqlTestRunner(verbosity=2)
    retval = unittest.TestResult()

    # Do some things to prepare the test environment.
    omap.igep0050_set_headset_amixer_settings(1)

    if len(args) == 0:
        # IGEP0050-RB10
        retval = suite.run(testsuite_IGEP0050())        
    elif args[0] == "RB20" :
        # IGEP0050-RB20
        retval = suite.run(testsuite_IGEP0050_RB20())

    # return 0 if all is ok, otherwise return the number of failures + errors
    sys.exit(len(retval.failures) + len(retval.errors))
