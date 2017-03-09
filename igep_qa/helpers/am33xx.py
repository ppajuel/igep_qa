#!/usr/bin/env python

"""
This provides various AM33XX/IGEP related helper functions.

"""

from igep_qa.helpers.common import QMmap, QCpuinfo
import commands

def am335x_get_mac_id0():
    """ The AM335x has a pair of unique MAC IDs.

    These IDs are unique not only for every AM335x, but are universally unique
    out of the Ethernet MAC allocation pool.

    Returns the MAC ID0 number in hexadecimal format

    See AM335x ARM Cortex-A8 Microprocessors TRM and search for mac_id0.

    """
    registers = [0x44e10630, 0x44e10634]
    mm = QMmap()
    a = "".join(mm.read(addr) for addr in registers)
    # reverse bytes
    return "".join(reversed([a[i:i + 2] for i in range(0, len(a), 2)]))

def am335x_get_mac_id1():
    """ The AM335x has a pair of unique MAC IDs.

    These IDs are unique not only for every AM335x, but are universally unique
    out of the Ethernet MAC allocation pool.

    Returns the MAC ID1 number in hexadecimal format

    See AM335x ARM Cortex-A8 Microprocessors TRM and search for mac_id1.

    """
    registers = [0x44e10638, 0x44e1063C]
    mm = QMmap()
    a = "".join(mm.read(addr) for addr in registers)
    # reverse bytes
    return "".join(reversed([a[i:i + 2] for i in range(0, len(a), 2)]))

def cpu_is_am33xx():
    """ Returns True if machine is AM33xx, otherwise returns False

    """
    cpu = QCpuinfo()
    if cpu["Hardware"] == "Generic AM33XX (Flattened Device Tree)":
        return True
    # otherwise
    return False

def igep0034_set_headset_amixer_settings(headset):
    """ Set amixer settings to playback/capture via headset,

    Make sure that the following amixer settings are done for the corresponding
    card (check the card no. by running the command cat /proc/asound/cards).

    """
    commands.getoutput("amixer -c %s sset 'PCM' 127" % headset)
