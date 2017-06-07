#!/usr/bin/env python

"""
Flash Test Cases modules for unittest

"""

import commands
import unittest
import os

class TestFlash(unittest.TestCase):
    """ Generic tests for flash devices.

    Keyword arguments:
        - testname:  The name of the test to be executed.
        - dev_partition: Partition path, e.g. /dev/mtd1 or /run/media/mmcblk2p2
        - file1: Optional, path from file1 stored into internal memory
        - file2: Optional, path from file2 stored into internal memory
        - file3: Optional, path from file3 stored into internal memory
        - testdescription: Optional test description to overwrite the default
    """
    def __init__(self, testname, dev_partition, file1='', file2='', file3='', testdescription=''):
        super(TestFlash, self).__init__(testname)
        self.dev_partition = dev_partition
        self.file1 = file1
        self.file2 = file2
        self.file3 = file3

        # Overwrite test description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_nandtest(self):
        """ Test nandtest : Write and read back random values

        Type: Functional

        .. warning::

            Althought by default should keep information in flash this test can be
            destructive.

        Description:
            The test writes random values to the flash partition and checks if the
            readed value is the same.

        """
        retval = commands.getstatusoutput("nandtest " + self.dev_partition + " -k -l 0xE0000")
        self.failUnless(retval[0] == 0, "error: Failed writting nand")

    def test_ubifsfirmware(self):
        """ Test ubifsfirmware : Read some files from UBIFS partition to ensure firmware flashed

        Type: Functional

        Description:
            The main goal of this test is detect if firmware has been flashed into an UBIFS partition.
            To achieve it, test ubifsfirmware mounts an UBIF partition and reads some files recorded.

        """
        #  Mount UBIFS partition to mountdirectory
        mountdirectory = '/tmp/UBIFS'
        retval = commands.getstatusoutput("ubiattach -p %s" % self.dev_partition)
        self.failUnless(retval[0] == 0, "error: Failed to attach UBIFS partition")
        retval = commands.getstatusoutput("mkdir %s" % mountdirectory)
        retval = commands.getstatusoutput("mount -t ubifs ubi0:filesystem %s" % mountdirectory)
        self.failUnless(retval[0] == 0, "error: Failed to mount UBIFS partition")
        #  Test the readability of file1
        retval = os.access((mountdirectory + self.file1), os.R_OK)
        self.failUnless(retval == 1, "failed: Seems that file '%s' doesn't exists" % (mountdirectory + self.file1))
        #  Test the readability of file2
        retval = os.access((mountdirectory + self.file2), os.R_OK)
        self.failUnless(retval == 1, "failed: Seems that file '%s' doesn't exists" % (mountdirectory + self.file2))
        #  Test the readability of file3
        retval = os.access((mountdirectory + self.file3), os.R_OK)
        self.failUnless(retval == 1, "failed: Seems that file '%s' doesn't exists" % (mountdirectory + self.file3))

    def test_firmware(self):
        """ Test firmware : Read some files from mounted partition to ensure firmware flashed

        Type: Functional

        Prerequisite recipes:
            - udev-extraconf

        Description:
            The main goal of this test is detect if firmware has been flashed into onboard memory.
            To achieve it, test firmware reads some files recorded.

        """
        #  Test the readability of file1
        retval = os.access((self.dev_partition + self.file1), os.R_OK)
        self.failUnless(retval == 1, "failed: Seems that file '%s' doesn't exists" % (self.dev_partition + self.file1))
        #  Test the readability of file2
        retval = os.access((self.dev_partition + self.file2), os.R_OK)
        self.failUnless(retval == 1, "failed: Seems that file '%s' doesn't exists" % (self.dev_partition + self.file2))
        #  Test the readability of file3
        retval = os.access((self.dev_partition + self.file3), os.R_OK)
        self.failUnless(retval == 1, "failed: Seems that file '%s' doesn't exists" % (self.dev_partition + self.file3))

if __name__ == '__main__':
    unittest.main(verbosity=2)
