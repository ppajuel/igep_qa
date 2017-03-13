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
        - mtd_partition: The mtd device, e.g. /dev/mtd1
    """
    def __init__(self, testname, mtd_partition, file1="", file2="", file3=""):
        super(TestFlash, self).__init__(testname)
        self.mtd_partition = mtd_partition
        self.file1 = file1
        self.file2 = file2
        self.file3 = file3

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
        retval = commands.getstatusoutput("nandtest " + self.mtd_partition + " -k -l 0xE0000")
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
        retval = commands.getstatusoutput("ubiattach -p %s" % self.mtd_partition)
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

if __name__ == '__main__':
    unittest.main(verbosity=2)

