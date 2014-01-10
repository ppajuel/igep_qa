#!/usr/bin/env python

"""
Wifi Test Cases modules for unittest

"""

import commands
import unittest

class TestWiFi(unittest.TestCase):
    """ Generic tests for wifi interfaces.

    .. warning::

        The test uses wlan0 interface. The interface is set up when the test
        start and set down when finishes.

    Keyword arguments:
        - testname:  The name of the test to be executed.
        - essid: The EESID to be connected.
        - serverip : The remote IP address.

    Prerequisite commands:
        - iwconfig
        - ifconfig
        - udhcpc
        - ping

    """
    def __init__(self, testname, essid, serverip):
        super(TestWiFi, self).__init__(testname)
        self.serverip = serverip
        self.essid = essid

    def setUp(self):
        # Ensure that interface is down
        commands.getstatusoutput("ifconfig wlan0 down")

    def test_ping_host(self):
        """  Test WiFi : Ping the IP address of a remote host

        Type: Functional

        Description:
            The test configures the 'interface' in ad-hoc mode, then tries
            get an ip address via dhcp and then to send a echo request ("ping")
            that is expected to be received back in an echo reply. You must
            configure a remote dhcp server.

        """
        retval = commands.getstatusoutput("iwconfig wlan0 essid %s channel 1"
                                          "" % self.essid)
        self.failUnless(retval[0] == 0, "failed: No wlan0 interface found.")
        retval = commands.getstatusoutput("udhcpc -n -i wlan0")
        self.failUnless(retval[0] == 0, "failed: Can't get ip address from "
                        "server")
        retval = commands.getstatusoutput("ping -c 3 %s" % self.serverip)
        self.failUnless(retval[0] == 0, "failed: Pinging to %s" % self.serverip)
        retval = commands.getstatusoutput("ifconfig wlan0 down")
        self.failUnless(retval[0] == 0, "failed: Can't down interface wlan0")

    def test_scan_for_essid(self):
        """ Test WiFi : Scan for ESSID network

        Type: Functional

        Description:
            The test sets up the 'interface' and then scans for the presence of
            a WiFi ESSID, after that set down the 'interface'.

        """
        retval = commands.getstatusoutput("ip link set wlan0 up")
        self.failUnless(retval[0] == 0, "failed: No wlan0 interface found.")
        retval = commands.getstatusoutput("iw dev wlan0 scan")
        self.failUnless(retval[0] == 0, "failed: Is not possible to scan.")
        self.failUnless(self.essid in retval[1], "failed: ESSID %s not found." % self.essid)
        retval = commands.getstatusoutput("ip link set wlan0 down")
        self.failUnless(retval[0] == 0, "failed: Can't down the interface.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
