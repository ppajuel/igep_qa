#!/usr/bin/env python

"""
This provides various generic helper functions and classes 

"""

import fcntl
import mmap
import os
import struct
import socket

def is_in_path(name):
    """ Return True if name refers to an existing file in path, otherwise 
    returns False.
    
    Keyword arguments:
        - name: The path name.

    """
    for p in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(p, name)):
            return True
    # File not found in path
    return False

def is_nfsroot():
    """ Return True if rootfs is mounted via nfs, otherwise returns False

    """
    fd = open("/proc/mounts", "r")
    content = fd.read()
    if content.find("/ nfs") == -1 :
        return False
    return True

def get_hwaddr(ifname):
    """ Return the MAC address for a specific local interface.

    Keyword arguments:
         - ifname : The interface name, e.g. eth0, wlan0.

    """ 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
    # exception
    except:
        return ""

class TCpuinfo:
    """ Helper class to parse the /proc/cpuinfo
    
    On Linux systems various information about the CPU ( or CPUs ) in the
    computer can be gleaned from /proc/cpuinfo.
    
    Known issues:
        1. This class doesn't work as expected with more than one core

    """
    def __init__(self):
        """ Parse /proc/cpuinfo file and store into map.

        """
        fd = open("/proc/cpuinfo", "r")
        self.data = { "processor" : "0" }
        lines = fd.readlines()
        for line in lines:
            keymap = line.split(": ")
            if len(keymap) == 2:
                key = keymap[0].strip("\t")
                value = keymap[1].rstrip("\n")
                self.data[key] = value
        fd.close()

    def __getitem__(self, index):
        """ Overload [] operator, access to the data like a mamp
        
        Example 1: Is easy to get the "Processor" value with,
            cpu = TCpuinfo()
            print cpu["Processor"] 
        
            The result should be like this
                ARMv7 Processor rev 2 (v7l)
        """
        return self.data[index]

class TCmdline:
    """ Helper class to parse the /proc/cmdline

    On Linux systems information about the kernel command line in the
    computer can be gleaned from /proc/cmdline.

    """
    def __init__(self):
        fd = open("/proc/cmdline", "r")
        self.cmdline = fd.read()
        fd.close()

    def checkparam(self, param):
        """ Check for the existence of a kernel parameter

        Return True if parameter is in cmdline, otherwise returns False

        Keyword arguments:
            - param : The paramater to be found.

        """
        if  (self.cmdline.find(param) == -1) :
            return False
        return True

class TMmap:
    """ Simple helper class to read/write from/to any location in memory

    References:
        http://www.lartmaker.nl/lartware/port/devmem2.c

    """
    MAP_MASK = mmap.PAGESIZE - 1
    WORD = 4
    def read(self, addr):
        """ Read from any location in memory

        Returns the readed value in hexadecimal format

        Keyword arguments:
            addr -- The memory address to be readed
        """
        fd = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
        # Map one page
        mm = mmap.mmap(fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE
                       | mmap.PROT_READ, offset=addr & ~self.MAP_MASK)
        mm.seek(addr & self.MAP_MASK)
        retval = struct.unpack('I', mm.read(self.WORD))
        mm.close()
        os.close(fd)
        return "%X" % retval[0]
