#!/usr/bin/env python

"""
Network Test Cases modules for unittest

"""

import commands
import unittest

from igep_qa.helpers import common

class TestNetwork(unittest.TestCase):
    """Generic tests for network interfaces.

    .. warning::

        The interface is set up when the test start and set down when finishes.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - ipaddr : The local IP address.
        - serverip : The remote IP address.
        - interface : The interface to be used, e.g. eth0, wlan0.
        - min_throughput : The minimum throughput required (in MBits)

    Prerequisite commands:
        - ifconfig
        - iperf
        - ping

    """
    def __init__(self, testname, ipaddr, serverip, interface, min_throughput = 90):
        super(TestNetwork, self).__init__(testname)
        self.ipaddr = ipaddr
        self.serverip = serverip
        self.interface = interface
        self.min_throughput = min_throughput

    def setUp(self):
        # NOT deconfiguring network interfaces in follwing cases 
        # - If / is an NFS mount
        # - Pinging local address 127.0.0.1
        # Instead of, use an ethernet alias.
        if common.is_nfsroot() or self.serverip == "127.0.0.1" :
            self.interface = "%s:0" % self.interface
        commands.getstatusoutput("ifconfig %s down" % self.interface)
        commands.getstatusoutput("ifconfig %s %s"
                                "" % (self.interface, self.ipaddr))

    def tearDown(self):
        commands.getstatusoutput("ifconfig %s down" % self.interface)

    def shortDescription(self):
        doc = self._testMethodDoc
        doc = doc.replace("Test Network", "Test Network (%s)" % self.interface)
        return doc and doc.split("\n")[0].strip() or None

    def test_ping_host(self):
        """ Test Network : Ping the IP address of a remote host

        Type: Functional

        Description:
            The test configures the 'interface' and then tries to send a echo 
            request ("ping") that is expected to be received back in an echo
            reply. For that, you must configure a remote host with proper IP
            address. Finally the test downs the interface.

        """
        retval = commands.getstatusoutput("ping -c 3 %s" % self.serverip)
        self.failUnless(retval[0] == 0, "failed: Pinging to %s" % self.serverip)

    def test_measure_throughput(self):
        """ Network : Measure the throughput and the quality of a network link.

        Type: Performance

        Description:
            The test configures the interface and then uses 'iperf' to
            measure the bandwidth. For that, you should configure a remote host
            with proper address and start the iperf server ('iperf -s').
            Then checks if the throughput is better than the specified. Finally
            it downs the interface.

        """
        retval, output = commands.getstatusoutput("iperf -x CMSV -c %s" % self.serverip)
        self.failUnless(retval == 0, "Failed: iperf command returned non-zero value:\n%s" % output)
        # Find the Mbits
        start = output.find("MBytes")
        self.failUnless(start > 0, "Failed: can't found MBytes string:\n%s" % output)
        end = output.find("Mbits")
        self.failUnless(end > 0, "Failed can't found Mbits string:\n%s" % output)
        mbits = output[start + 8:end - 1]
        self.failIf(float(mbits) < self.min_throughput, "Failed: the throughput is less than %s Mbits" % mbits)
