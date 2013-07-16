#!/usr/bin/env python

"""
USB Test Cases modules for unittest

"""

import commands
import os
import unittest

class TestUSB(unittest.TestCase):
    """ Generic Tests for USB interface.

    """
    def __init__(self, testname):
        super(TestUSB, self).__init__(testname)

    def test_musb_omap(self):
        """ USB OTG : Check for this_is_the_musb_omap_port file.

        Type: Functional

        Requirements:
            Use a USB pendrive with one FAT32 partition and create inside a
            file called this_is_the_ehci_omap_port.

        Description:
            - Connect the USB pendrive to the MUSB port.
            - Read if the file this_is_the_musb_omap_port exists.

        """
        exists = False
        for dev in [ '/dev/sda1', '/dev/sdb1' ]:
            retval = commands.getstatusoutput("udevadm info -q path -n %s" % dev)
            if "musb-omap" in retval[1]:
                # find mountpoint
                for mp in open("/proc/mounts", "r"):
                    # if device node is in mount point line
                    if dev in mp:
                        mntpoint = mp.split(" ")[1]
                        # find file resides on mount point
                        if os.path.isfile("%s/this_is_the_musb_omap_port"
                                               % mntpoint):
                            exists = True
                            break
        self.assertTrue(exists, "failed: file this_is_the_musb_omap_port on "
                        "MUSB USB not found")

    def test_ehci_omap(self):
        """ USB HOST : Check for this_is_the_ehci_omap_port file.

        Type: Functional

        Prerequisite commands:
            - udevadm

        Requirements:
            Use a USB pendrive with one FAT32 partition and create inside a
            file called this_is_the_ehci_omap_port.

        Description:
            - Connect the USB pendrive to the ECHI port.
            - Read if the file this_is_the_ehci_port exists.

        """
        exists = False
        for dev in [ '/dev/sda1', '/dev/sdb1' ]:
            retval = commands.getstatusoutput("udevadm info -q path -n %s" % dev)
            if "ehci-omap" in retval[1]:
                # find mountpoint
                for mp in open("/proc/mounts", "r"):
                    # if device node is in mount point line
                    if dev in mp:
                        mntpoint = mp.split(" ")[1]
                        # find file resides on mount point
                        if os.path.isfile("%s/this_is_the_ehci_omap_port"
                                               % mntpoint):
                            exists = True
                            break
        self.assertTrue(exists, "failed: file this_is_the_ehci_omap_port on "
                        "EHCI USB not found")

if __name__ == '__main__':
    unittest.main(verbosity=2)
