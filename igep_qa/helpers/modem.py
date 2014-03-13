#!/usr/bin/env python

"""
This provides helper functions for Modem chips.

"""

import serial
import time

from igep_qa.helpers.gpiolib import QGpio

class QModemTelit:
    """ ModemTelit (GE865)

    The GE865 uses a serial UART and the #ON, #RESET and #PWRMON gpio to drive
    the modem.

    See the Telit GE865-QUAD Hardware User Guide

    """
    def __init__(self, on, reset, pwrmon, port):
        """ Initialize Telit Modem

        Keyword arguments:
            - on: GPIO number to turn ON/OFF the modem
            - reset: GPIO number to reset the modem
            - pwrmon: GPIO number that should be monitored to check if the
              device has powered on
            - port: The serial port used for the modem

        """
        self.on = QGpio(on)
        self.reset = QGpio(reset)
        self.pwrmon = QGpio(pwrmon)
        self.port = serial.Serial(port, timeout=1)

    def __del__(self):
        self.port.close()

    def turn_on(self):
        """ Turning ON the GE865 by tying pulse pin ON#

        Return 1 if fail and the modem is OFF, 0 on success

        To turn on the GE865 the pad ON# must be tied low for at least 1 second
        and then released.

        """
        retval = 0
        if self.pwrmon.get_value() == 0:
            # modem is OFF, power ON impulse
            self.on.set_value(1)
            time.sleep(1)
            self.on.set_value(0)
            time.sleep(2)
            if self.pwrmon.get_value() == 0:
                # fail, the modem is OFF
                retval = 1
        time.sleep(1)
        # success, the modem is ON
        return retval

    def turn_off(self):
        """ Turning OFF the GE865 by tying pulse pin ON

        Returns 1 if fail and the modem is ON, 0 on success

        To turn OFF the GE865 the pad ON must be tied low for at least 2
        seconds and then released.

        """
        retval = 0
        if self.pwrmon.get_value() == 1:
            # modem is ON, power OFF impulse
            self.on.set_value(1)
            time.sleep(2)
            self.on.set_value(0)
            time.sleep(15)
            if self.pwrmon.get_value() == 1:
                # fail, the modem is ON
                retval = 1
        time.sleep(1.5)
        # success, the modem is OFF
        return retval

    def restart(self):
        """ Resetting/restarting the GE865

        To unconditionally reboot the GE865, the pad RESET must be tied low for
        at least 200 milliseconds and then released.

        .. warning::

            The hardware unconditional Restart must not be used during
            normal operation of the device since it does not detach the device
            from the network. It shall be kept as an emergency exit procedure
            to be done in the rare case that the device gets stacked waiting
            for some network or SIM responses.

        """
        retval = 0
        self.reset.set_value(1)
        time.sleep(0.2)
        self.reset.set_value(0)
        if self.pwrmon.get_value() == 0:
            # fail, the modem is OFF
            retval = 1
        time.sleep(2)
        return retval

    def command(self, command):
        """ Send AT command to the GE865

        Returns the command response

        Keyword arguments:

            - command: AT command to be send.

        """
        # Before send any command make sure that the input buffer is empty,
        # otherwise we can return a dirty string.
        if self.port.inWaiting():
            # Flush input buffer, discarding all it’s contents.
            self.port.flushInput()
        self.port.write(command)
        return self.port.read(255)

    def at(self):
        """ Send AT command

        Returns 0 on success, otherwise returns the command output.

        """
        expected = "AT\r\r\nOK\r\n"
        retval = self.command("AT\r")
        if retval == expected:
            return 0
        else:
            return retval

    def at_cpin(self, cpin):
        """ Send AT+CPIN = <cpin> command

        Returns 1 if fail, 0 on success

        Keyword arguments:
            - cpin: SIM card pin number.

        """
        expected = "at+cpin=%s\r\r\nOK\r\n" % cpin
        retval = self.command("at+cpin=%s\r" % cpin)
        if retval == expected:
            return 0
        else:
            return retval

# Test Cases for class TModemTelit
import unittest

class TestClassQModemTelit(unittest.TestCase):
    """ Unittest for class ModemTelit

    """
    def setUp(self):
        self.modem = QModemTelit(141, 140, 156, '/dev/ttyO1')

    def test_turning_on_modem(self):
        retval = self.modem.turn_on()
        self.failUnless(retval == 0,
            "Error: Turning ON the modem, expected value '0' "
            "and returned '%s'" % retval)

    def test_turning_off_modem(self):
        retval = self.modem.turn_off()
        self.failUnless(retval == 0,
            "Error: Turning OFF the modem, expected value '0' "
            "and returned '%s'" % retval)

    def test_restarting_the_modem(self):
        self.modem.turn_on()
        retval = self.modem.restart()
        self.failUnless(retval == 0,
            "Error: Turning restarting the modem, expected value '0' "
            "and returned '%s'" % retval)

    def test_command_at(self):
        self.modem.turn_on()
        # AT command: AT
        retval = self.modem.at()
        self.failUnless(retval == 0, "Error: Expected '%s' and received '%s' "
                        % (repr("AT\r\r\nOK\r\n"), repr(retval)))

    def test_command_at_cpin(self):
        self.modem.turn_on()
        # AT command: Enter pin
        retval = self.modem.at_cpin(5555)
        self.failUnless(retval == 0, "Error: Expected '%s' and received '%s' "
                        % (repr("at+cpin=5555\r\r\nOK\r\n"), repr(retval)))

if __name__ == '__main__':
    unittest.main()
