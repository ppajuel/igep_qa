#!/usr/bin/env python

"""
HWMON Test Cases modules for unittest

"""

import unittest

class TestHwmon(unittest.TestCase):
    """ Generic Tests for HWMON interface.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - sysfspath : The sysfs device naming scheme. For example for an USB block.
        - tmin : Minium value in temperature range.
        - tmax : Maxium value in temperature range.
        - testdescription: Optional test description to overwrite the default.

    """

    def __init__(self, testname, sysfspath, tmin, tmax, testdescription = ''):
        super(TestHwmon, self).__init__(testname)
        self.sysfspath = sysfspath
        self.tmin = tmin
        self.tmax = tmax
        # Overwrite test description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_temperature_range(self):
        """ Test HWMON : Check temperature is in range

        Type: Functional

        Description:
            Reads the temperature value from the sensor and makes sure that the
            value is between tmin and tmax.

        """
        try:
            fd = open('%s' % self.sysfspath, "r")
            temp = fd.read()
            fd.close()
            self.assertLessEqual(int(temp), self.tmax, 'failed: '
                'temperature (%s) greater than tmax (%s)' % (temp, self.tmax))
            self.assertGreaterEqual(int(temp), self.tmin, 'failed: '
                'temperature (%s) less than tmin (%s)' % (temp, self.tmin))
        except IOError:
            self.fail('failed: failed opening sysfs path (%s)' % self.sysfspath)

if __name__ == '__main__':
    unittest.main(verbosity=2)
