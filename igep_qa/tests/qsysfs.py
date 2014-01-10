#!/usr/bin/env python

"""
SYSFS Test Cases modules for unittest

"""

import unittest

class TestSysfs(unittest.TestCase):
    """ Generic Tests for SYSFS interface.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - sysfspath : The sysfs path.
        - devname : The device name.
        - testdescription: Optional test description to overwrite the default.

    """

    def __init__(self, testname, sysfspath, devname, testdescription = ''):
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
