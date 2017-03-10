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
        - ipaddr : The local IP address (some tests acquire the ip via dhcp).
        - password : Remote WiFi password (some tests don't need them).

    Prerequisite commands:
        - iwconfig
        - ifconfig
        - udhcpc
        - ping

    """
    def __init__(self, testname, serverip, essid, ipaddr="", password=""):
        super(TestWiFi, self).__init__(testname)
        self.serverip = serverip
        self.essid = essid
        self.ipaddr = ipaddr
        self.password = password

    def test_ping_host(self):
        """  Test WiFi : Ping the IP address of a remote host

        Type: Functional

        Description:
            The test configures the 'interface' in ad-hoc mode, then tries
            get an ip address via dhcp and then to send a echo request ("ping")
            that is expected to be received back in an echo reply. You must
            configure a remote dhcp server.

        """
        retval = commands.getstatusoutput("ip link set wlan0 down")
        self.failUnless(retval[0] == 0, "failed: Can't down interface wlan0")
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
        retval = commands.getstatusoutput("ip link set wlan0 down")
        self.failUnless(retval[0] == 0, "failed: Can't down interface wlan0")
        retval = commands.getstatusoutput("ip link set wlan0 up")
        self.failUnless(retval[0] == 0, "failed: No wlan0 interface found.")
        retval = commands.getstatusoutput("iw dev wlan0 scan")
        self.failUnless(retval[0] == 0, "failed: Is not possible to scan.")
        self.failUnless(self.essid in retval[1], "failed: ESSID %s not found." % self.essid)
        retval = commands.getstatusoutput("ip link set wlan0 down")
        self.failUnless(retval[0] == 0, "failed: Can't down the interface.")

    def test_adhoc_with_wep_encryption(self):
        """  Test WiFi : Ping the IP address of a remote host (adhoc+wep)

        Type: Functional

        Description:
            The test connects to server in ad-hoc mode with WEP encryption,
            then tries to send a echo request ("ping") that is expected to
            be received back in an echo reply. You must configure a remote dhcp server.

        .. warning::

            AT THE MOMENT THIS TEST ONLY WORKS THE FIRST TIME THAT RUNS.
            There is a bug in kernel (2.6.37-8) that causes the wlan connection
            doesn't work setting down and up the interface if the interface was
            already up before, as a workaround to do this test don't set down
            the interface. Please make sure the interface was never set up,
            otherwise the test may fail.

        """
        # retval = commands.getstatusoutput("ip link set wlan0 down")
        # self.failUnless(retval[0] == 0, "failed: Can't down interface wlan0")
        retval = commands.getstatusoutput("ip link set wlan0 up")
        self.failUnless(retval[0] == 0, "failed: No wlan0 interface found.")
        retval = commands.getstatusoutput("iw wlan0 set type ibss")
        self.failUnless(retval[0] == 0, "failed: %s" % retval[1])
        commands.getstatusoutput("ifconfig wlan0 %s" % self.ipaddr)
        # For now there are some fixed parameters like channel and key
        retval = commands.getstatusoutput("iw wlan0 ibss join %s 2422 key d:0:a2PheIrWs23-f" % self.essid)
        self.failUnless(retval[0] == 0, "failed: %s" % retval[1])
        retval = commands.getstatusoutput("ping -I wlan0 -c 5 -s 8096 %s" % self.serverip)
        self.failUnless(retval[0] == 0, "failed: Pinging to %s" % self.serverip)
        # retval = commands.getstatusoutput("ip link set wlan0 down")
        # self.failUnless(retval[0] == 0, "failed: Can't down interface wlan0")

    def test_ap_with_wep_encryption(self):
        """  Test WiFi : Ping the IP address of a remote host (ap+wep)

        Type: Functional

        Description:
            The test connects to hotspot in AP mode with WEP encryption,
            then tries to send a echo request ("ping") that is expected to
            be received back in an echo reply.
        """
        retval = commands.getstatusoutput("ifconfig wlan0 up")
        self.failUnless(retval[0] == 0, "failed: No wlan0 interface found.")
        retval = commands.getstatusoutput("ifconfig wlan0 %s" % self.ipaddr)
        self.failUnless(retval[0] == 0, "failed: wlan0 interface cannot set ipaddr.")
        retval = commands.getstatusoutput("iw wlan0 connect %s key 0:%s" % (self.essid, self.password))
        self.failUnless(retval[0] == 0, "failed: wlan0 cannot connect to hotspot: %s." % self.essid)
        retval = commands.getstatusoutput("ping -I wlan0 -c 5 -s 8096 %s" % self.serverip)
        self.failUnless(retval[0] == 0, "failed: Pinging to %s" % self.serverip)
        retval = commands.getstatusoutput("ifconfig wlan0 down")
        self.failUnless(retval[0] == 0, "failed: Can't down interface wlan0.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
