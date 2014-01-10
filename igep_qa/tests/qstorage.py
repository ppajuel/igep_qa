#!/usr/bin/env python

"""
Block Storage Test Cases modules for unittest

"""

import commands
import os
import unittest

class TestBlockStorage(unittest.TestCase):
    """ Generic Tests for Block Storage interfaces.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - sysfsname : The sysfs device naming scheme. For example for an USB block
                      device should follow the scheme:
                         root_hub_name/root_hub-hub_port/root_hub-hub_port.device
                      As example:
                         usb1/1-2/1-2.1
                      To check the sysfs device naming use the following command:
                         udevadm info -q path -n /dev/<block device>
        - testdescription: Optional test description to overwrite the default.

    """
    def __init__(self, testname, sysfsname, testdescription = ''):
        super(TestBlockStorage, self).__init__(testname)
        self.sysfsname = sysfsname
        self.file = 'this_is_an_storage_device'
        # Overwrite test short description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_storage_device(self):
        """ Test Storage: Check for this_is_an_storage_device file

        Type: Functional

        Prerequisite commands:
            - udevadm

        Requirements:
            Use a Storage device with one FAT32 partition and create inside a
            file called this_is_an_storage_device exists.

        Limitations:
            This function only is able to detect 5 storage ports (from /dev/sda
            to /dev/sde)

        Description:
            - Connect the storage to the port.
            - Read if the file this_is_an_storage_device exists.

        """
        exists = False
        for dev in [ '/dev/sda', '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde' ]:
            retval = commands.getstatusoutput('udevadm info -q path -n %s' % dev)
            if self.sysfsname in retval[1]:
                # find mountpoint
                for mp in open('/proc/mounts', 'r'):
                    # if device node is in mount point line
                    if dev in mp:
                        mntpoint = mp.split(' ')[1]
                        # find file resides on mount point
                        if os.path.isfile('%s/this_is_an_storage_device'
                                               % mntpoint):
                            exists = True
                            break
        self.assertTrue(exists, 'failed: file this_is_an_storage_device on '
                        'port %s not found' % self.sysfsname)

if __name__ == '__main__':
    unittest.main(verbosity=2)
