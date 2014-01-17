#!/usr/bin/env python

"""
Modem Test Cases modules for unittest

"""

import unittest

from igep_qa.helpers.modem import QModemTelit

class TestModem(unittest.TestCase):
    """ Generic Tests for modem devices.

    Keyword arguments:
        - on: GPIO number to turn ON/OFF the modem.
        - reset: GPIO number to reset the modem.
        - pwrmon: GPIO number that should be monitored to check if the
                  device has powered on.
        - port: The serial port used for the modem.
        - testdescription: Optional test description to overwrite the default.

    """
    def __init__(self, testname, on, reset, pwrmon, port, testdescription=''):
        super(TestModem, self).__init__(testname)
        self.modem = QModemTelit(on, reset, pwrmon, '/dev/ttyO1')
        # Overwrite test description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_command_at_cpin(self):
        """ Test Modem : Send and request pin number (5555)

        The test covers the serial communication between the processor and the
        modem device, the on, reset and pwrmon gpios and the SIM holder
        connection.

        The PIN has to be introduced only once, to avoid false negative test
        results we do a reset before execute the CPIN command.

        """
        self.modem.restart()
        # Now turn on the modem and send the cpin command
        self.modem.turn_on()
        retval = self.modem.at_cpin(5555)
        self.failUnless(retval == 0, "failed: Expected 'at+cpin=5555\r\r\nOK"
                        "\r\n' and received '%s' " % retval)

if __name__ == '__main__':
    unittest.main(verbosity=2)
