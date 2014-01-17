#!/usr/bin/env python

"""
SYSFS Test Cases modules for unittest

"""

import os
import unittest

class TestSysfs(unittest.TestCase):
    """ Generic Tests for SYSFS interface.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - sysfspath : The sysfs path.
        - devname : The device name.
        - testdescription: Optional test description to overwrite the default.

    """

    def __init__(self, testname, sysfspath, devname='', testdescription=''):
        super(TestSysfs, self).__init__(testname)
        self.sysfspath = sysfspath
        self.devname = devname
        # Overwrite test description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_device_name(self):
        """ Test SYSFS : Check if device name is available

        Type: Functional

        Description:
            Reads the <syspath>/name to check that devname is detected.

        """
        try:
            fd = open('%s/name' % self.sysfspath, "r")
            devname = fd.read().replace("\n", '')
            fd.close()
            self.assertEqual(self.devname, devname, 'failed: '
                'driver name (%s) is not equal to %s' % (self.devname, devname))
        except IOError:
            self.fail('failed: opening sysfs path (%s/name)' % self.sysfspath)

    def test_sysfs_entry(self):
        """ Test SYSFS : Test if device entry exists.

        Type: Functional

        Description:
            Check if specified syspath entry exists. Normally when a device is
            added a sysfs files are properly created, check the presence of one
            of this files can be useful to check that a device is probed. Note,
            but, some drivers create these files without probing or checking
            the communication with the device, in that case this test does not
            work and produces a false positive.

            To avoid this always make sure that the sys entry is created only
            when the device is probed, with some kind of communication between
            the driver and the device, and is not created when the probe fails.

        """
        self.failUnless(os.path.exists(self.sysfspath),
                        'failed: opening %s' % self.sysfspath)
