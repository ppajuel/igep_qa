#!/usr/bin/env python

"""
User button Test Cases modules for unittest

"""

import unittest
import os
import select
import commands
import time
from igep_qa.helpers.gpiolib import QGpio
from igep_qa.helpers.imx6 import cpu_is_imx6

class TestButton(unittest.TestCase):
    """ Generic test for user button.

    Keyword arguments:
        - gpio_in: GPIO input mapped to user button.
    """
    def __init__(self, testname, gpio_in):
        super(TestButton, self).__init__(testname)
        self.gpio_in = QGpio(gpio_in)
        if testname == "test_button_fbtest":
            if cpu_is_imx6():
                self._testMethodDoc = "\033[33mTest Button Fbtest : PLEASE, CAPTURE QR CODE AND PRESS USER BUTTON (S1200) TO TEST IT OR WAIT 30 SECONDS.\033\n[0m"
            else:
                self._testMethodDoc = "\033[33mPLEASE, PRESS USER BUTTON (S1200) TO TEST IT. THEN, IF THE FOLLOWING IMAGE PATTERN IS CORRECT PRESS USER BUTTON AGAIN OR WAIT 30 SECONDS.\033\n[0m"
        if testname == "test_button":
            self._testMethodDoc = "\033[33mTest Button : PLEASE, CAPTURE QR CODE AND PRESS USER BUTTON (S1200) TO TEST IT OR WAIT 30 SECONDS.\033\n[0m"

    def test_button_fbtest(self):
        """ Test Button Fbtest : Read User button action and display fb-test pattern

        Type: Functional

        Description:
            - This test needs the interaction with the user. First of all, is
              necessary to pulse the user button to display fb-test pattern. Once user
              has validated that fb-test pattern is correct, press again user button to
              finish and save test results.

        .. warning::

            For i.MX6, this test should be the last one. For the rest of boards,
            it should be placed at the beginning of testsuite
        """

        def exit_commands():
            if cpu_is_imx6():
                retval = commands.getstatusoutput("echo ' ' > /dev/tty0")
                self.failUnless(retval[0] == 0, "failed: Can't execute 'echo'")
                retval = commands.getstatusoutput("echo '\033[37mTest Button Fbtest : Test finished, result is \033' > /dev/tty0")
                self.failUnless(retval[0] == 0, "failed: Can't execute 'echo'")
            else:
                retval = commands.getstatusoutput("clear > /dev/tty0")
                self.failUnless(retval[0] == 0, "failed: Can't execute 'clear > /dev/tty0'")
                retval = commands.getstatusoutput("echo '\033[37mTest Button Fbtest : Read User button action and display fb-test pattern: \033' > /dev/tty0")
                self.failUnless(retval[0] == 0, "failed: Can't execute 'echo'")

            f.close();

            self._testMethodDoc = "Test Button Fbtest : Read User button action and display fb-test pattern"

        self.gpio_in.set_direction("in")
        retval = self.gpio_in.get_direction()
        self.failUnless(retval == 'in\n',
            "Error: Expected value 'in' and readed %s" % retval)

        self.gpio_in.set_edge("falling")
        retval = self.gpio_in.get_edge()
        self.failUnless(retval == 'falling\n',
            "Error: Expected value 'falling' and readed %s" % retval)

        f = open(os.path.join(self.gpio_in.sysfs, 'value'), 'r')

        po = select.poll()
        po.register(f, select.POLLPRI)

        f.seek(0)
        state_last = f.read()
        events = po.poll(30000)
        if not events:
            exit_commands()
            self.fail("Error timeout, unable to get first button press")

        if cpu_is_imx6():
            retval = commands.getstatusoutput("echo ' ' > /dev/tty0")
            self.failUnless(retval[0] == 0, "failed: Can't execute 'echo'")
            retval = commands.getstatusoutput("echo '\033[33mTest Button Fbtest : PLEASE, PRESS USER BUTTON (S1200) TO ACCEPT DISPLAY PATTERN OR WAIT 30 SECONDS. \033' > /dev/tty0")
            self.failUnless(retval[0] == 0, "failed: Can't execute 'echo'")
        else:
            retval = commands.getstatusoutput("/usr/bin/fb-test")
            self.failUnless(retval[0] == 0, "failed: Can't execute /usr/bin/fb-test")

        if cpu_is_imx6():
            time.sleep(1)
        else:
            time.sleep(2)

        f.seek(0)
        state_last = f.read()
        events = po.poll(30000)
        if not events:
            exit_commands()
            self.fail("Error timeout, unable to get second button press")

        exit_commands()

    def test_button(self):
        """ Test Button : Read User button action

        Type: Functional

        Description:
            - This test needs the interaction with the user. It is
              necessary to pulse the user button to PASS TEST.

        """

        def exit_commands():
            self._testMethodDoc = "Test Button : Read User button action"

            retval = commands.getstatusoutput("echo '\033[37mTest Button : Read User button action:  \033' > /dev/ttyO0")
            self.failUnless(retval[0] == 0, "failed: Can't execute 'echo'")

            f.close();

        self.gpio_in.set_direction("in")
        retval = self.gpio_in.get_direction()
        self.failUnless(retval == 'in\n',
            "Error: Expected value 'in' and readed %s" % retval)

        self.gpio_in.set_edge("falling")
        retval = self.gpio_in.get_edge()
        self.failUnless(retval == 'falling\n',
            "Error: Expected value 'falling' and readed %s" % retval)

        f = open(os.path.join(self.gpio_in.sysfs, 'value'), 'r')

        po = select.poll()
        po.register(f, select.POLLPRI)

        f.seek(0)
        state_last = f.read()
        events = po.poll(30000)
        if not events:
            exit_commands()
            self.fail("Error timeout, unable to get button press")

        exit_commands()

if __name__ == '__main__':
    unittest.main(verbosity=2)
