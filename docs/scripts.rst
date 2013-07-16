Scripts
=======

A collection of scripts.

igep-qa.sh
----------

A init script to use in a Sys-V init system for autoexecuting a Test Suite at
bootup. The script reads the kernel cmdline and if founds the 'autotest'
command lauches the Test Suite. E.g.

    autotest=IGEP0020

launches the Test Suite for IGEP0020 board.

The script should be placed into /etc/init.d and you should add the necessary
links to the script.

