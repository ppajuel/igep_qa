#!/usr/bin/env python

"""
This provides various i.MX6/IGEP related helper functions.

"""

from igep_qa.helpers.common import QMmap, QCpuinfo
import commands

def imx6_get_unique_id():
    """ Single die identifier for i.MX6 processors

    Returns the unique 64b serial number in hexadecimal format.
    This number is stored at OCOTP_CFG0 and OCOTP_CFG1 registers

    See i.MX 6 Applications Processor Reference Manual

    """
    registers = [0x021BC420, 0x021BC410]
    mm = QMmap()
    return "".join(mm.read(addr) for addr in registers)

def cpu_is_imx6():
    """ Returns True if machine is i.MX6, otherwise returns False

    """
    cpu = QCpuinfo()
    if cpu["Hardware"] == "Freescale i.MX6 Quad/DualLite (Device Tree)":
        return True
    # otherwise
    return False

def igep0046_set_headset_amixer_settings(headset):
    """ Set amixer settings to playback/capture via headset,

    Make sure that the following amixer settings are done for the corresponding
    card (check the card no. by running the command cat /proc/asound/cards).

    """
    commands.getoutput("amixer -c %s sset 'PCM' 127" % headset)
