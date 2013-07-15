""" 
This provides various OMAP/IGEP related helper functions. 

"""

from igep_qa.helpers.common import QMmap, QCpuinfo

def get_dieid():
    """ Single die identifier for OMAP processors

    Returns the die number in hexadecimal format

    See AM/DM37x Multimedia Device Silicon Revision 1.x TRM

    """
    registers = [0x4830A224, 0x4830A220, 0x4830A21C, 0x4830A218]
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
