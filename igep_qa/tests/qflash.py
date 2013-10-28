#!/usr/bin/env python

"""
Flash Test Cases modules for unittest

"""

import commands
import unittest

class TestFlash(unittest.TestCase):
    """ Generic tests for flash devices.

    Keyword arguments:
        - testname:  The name of the test to be executed.
        - mtd_partition: The mtd device, e.g. /dev/mtd1
    """
    def __init__(self, testname, mtd_partition):
        super(TestFlash, self).__init__(testname)
        self.mtd_partition = mtd_partition

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
        self.failUnless(retval[0]==0, "error: Failed writting nand")

if __name__ == '__main__':
    unittest.main(verbosity=2)

