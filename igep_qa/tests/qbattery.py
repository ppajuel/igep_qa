#!/usr/bin/env python

"""
Battery Backup Test Cases modules for unittest

"""

import unittest

from igep_qa.helpers.madc import QMadc

class TestBatteryBackup(unittest.TestCase):
    """ Generic test for battery backup.

    """
    def test_battery_backup(self):
        """ Test Battery Backup : Read battery voltage level

        Type: Functional

        Description:
            - Read the level of the battery backup. The value should be between
              1.5V and 3.3V.

        """
        batt = QMadc(9)
        value = batt.voltage()
        self.failIf((value < 1.5) | (value > 3.3), "failed: Battery Backup "
                    "failed (%s)." % value)

if __name__ == '__main__':
    unittest.main(verbosity=2)
