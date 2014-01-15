""" 
This provides various OMAP/IGEP related helper functions. 

"""

from igep_qa.helpers.common import QMmap, QCpuinfo, QDeviceTree
import commands

def cpu_is_omap5():
    """ Returns True if machine is OMAP5, otherwise returns False

    """
    return QDeviceTree().compatible("ti,omap5")

def omap3_get_dieid():
    """ Single die identifier for OMAP processors

    Returns the die number in hexadecimal format

    See AM/DM37x Multimedia Device Silicon Revision 1.x TRM

    """
    registers = [0x4830A224, 0x4830A220, 0x4830A21C, 0x4830A218]
    mm = QMmap()
    return "".join(mm.read(addr) for addr in registers)

def omap5_get_dieid():
    """ Single die identifier for OMAP5 processors

    Returns the die number in hexadecimal format

    See OMAP543x Multimedia Device TRM Revision X

    """
    registers = [0x4A002210, 0x4A00220C, 0x4A002208, 0x4A002200]
    mm = QMmap()
    return "".join(mm.read(addr) for addr in registers)

def machine_is_igep0020():
    """ Returns True if machine is igep0020, otherwise returns False

    """
    cpu = QCpuinfo()
    if cpu["Hardware"] == "IGEP0020 board":
        return True
    # otherwise
    return False

def machine_is_igep0030():
    """ Returns True if machine is igep0030, otherwise returns False.

    """
    cpu = QCpuinfo()
    if cpu["Hardware"] == "IGEP0030 COM":
        return True
    # otherwise
    return False

def machine_is_igep0032():
    """ Returns True if machine is igep0032, otherwise returns False

    """
    cpu = QCpuinfo()
    if cpu["Hardware"] == "IGEP0032 COM":
        return True
    # otherwise
    return False

def buddy_is_igep0022():
    """ Returns True if buddy is igep0022, otherwise returns False.

    """
    fd = open("/proc/cmdline", "r")
    for opts in fd.readline().split(" "):
        if "buddy=igep0022" in opts:
            fd.close()
            return True
    # otherwise
    fd.close()
    return False

def buddy_is_base0010():
    """ Returns True if buddy is base0010, otherwise returns False

    """
    fd = open("/proc/cmdline", "r")
    for opts in fd.readline().split(" "):
        if "buddy=base0010" in opts:
            fd.close()
            return True
    # otherwise
    fd.close()
    return False

def buddy_is_ilms0015():
    """ Returns True if buddy is ilms0015, otherwise returns False.

    """
    fd = open("/proc/cmdline", "r")
    for opts in fd.readline().split(" "):
        if "buddy=ilms0015" in opts:
            fd.close()
            return True
    # otherwise
    fd.close()
    return False

def igep0050_set_headset_amixer_settings(headset):
    """ Set amixer settings to playback/capture via headset,

    Make sure that the following amixer settings are done for the corresponding
    card (check the card no. by running the command cat /proc/asound/cards).

    """
    commands.getoutput("amixer cset -c %s name='Headset Left Playback' 1" % headset)
    commands.getoutput("amixer cset -c %s name='Headset Right Playback' 1" % headset)
    commands.getoutput("amixer cset -c %s name='Headset Playback Volume' 12" % headset)
    commands.getoutput("amixer cset -c %s name='DL1 PDM Switch' 1" % headset)
    commands.getoutput("amixer cset -c %s name='Sidetone Mixer Playback' 1" % headset)
    commands.getoutput("amixer cset -c %s name='SDT DL Volume' 120" % headset)
    commands.getoutput("amixer cset -c %s name='DL1 Mixer Multimedia' 1" % headset)
    commands.getoutput("amixer cset -c %s name='DL1 Media Playback Volume' 110" % headset)
    commands.getoutput("amixer cset -c %s name='Sidetone Mixer Capture' 1" % headset)
    commands.getoutput("amixer sset -c %s 'Analog Left',0 'Headset Mic'" % headset)
    commands.getoutput("amixer sset -c %s 'Analog Right',0 'Headset Mic'" % headset)
    commands.getoutput("amixer sset -c %s 'AUDUL Media',0 149" % headset)
    commands.getoutput("amixer sset -c %s 'Capture',0 4" % headset)
    commands.getoutput("amixer sset -c %s MUX_UL00,0 AMic0" % headset)
    commands.getoutput("amixer sset -c %s MUX_UL01,0 AMic1" % headset)
    commands.getoutput("amixer sset -c %s 'AMIC UL',0 120" % headset)
