#!/usr/bin/env python

"""
Power Test Cases modules for unittest

"""

import commands
import socket
import time
import unittest

from igep_qa.helpers import common
from igep_qa.helpers import am33xx

class TestPower(unittest.TestCase):
    """Generic tests for power interfaces.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - current_max : The maximum value of amperes.
        - ipaddr : The local IP address.
        - serverip : The remote IP address.
        - port : The remote port to connect.
        - interface : The interface to be used, e.g. eth0, wlan0.

    Prerequisite commands:
        - ifconfig

    """
    def __init__(self, testname, max_current, ipaddr, serverip, port, interface):
        super(TestPower, self).__init__(testname)
        self.max_current = max_current
        self.ipaddr = ipaddr
        self.serverip = serverip
        self.port = port
        self.interface = interface

    def setUp(self):
        # Set up the interface
        commands.getstatusoutput("ifconfig %s %s"
                                "" % (self.interface, self.ipaddr))
        # Use a small delay to be sure the interface is up
        time.sleep(1)

    def tearDown(self):
        commands.getstatusoutput("ifconfig %s down" % self.interface)

    def test_max_current(self):
        """ Test Power : Check the maximum acceptable limit of current

        Type: Functional

        Description:
            The test configures the 'interface' and then tries to connect to
            server to request the current. Is expected that this value is
            lower than the max_current parameter. Finally the test downs the
            interface.

        """
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((self.serverip, self.port))
            sock.sendall("\n")

            # Receive data from the server and shut down
            retval = float(sock.recv(1024))
            self.failUnless(retval < self.max_current, "failed: "
                            "Current (%s A) exceeds the maximum (%s A)"
                            % (retval, self.max_current))
        finally:
            sock.close()
