#!/bin/sh
### BEGIN INIT INFO
# Provides:          igep-qa.sh
# Required-Start:    mountnfs.sh
# Should-Start:
# Required-Stop:
# Should-Stop:
# Default-Start:     2 5
# Default-Stop:
# Short-Description: IGEP-QA init script for IGEP-technology devices.
# Description:       This script should be placed in /etc/init.d
### END INIT INFO

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin

NAME="igep-qa"
# Terminal
XTERM="xterm -display :0 -hold -fg white -bg black"
# Python binary
PYTHONBIN="/usr/bin/python"
# Testsuite path
TESTSUITE="/usr/lib/python2.7/site-packages/igep_qa/suites"

# Read configuration variable file if it is present
#[ -r /etc/default/${NAME} ] && . /etc/default/${NAME}

#
# Function that starts the script
#
do_start() {
	echo "Starting ${NAME} ..."
	read CMDLINE < /proc/cmdline
	echo "Running ${NAME} ..."
	# TODO: remove sleep and use more elegant solution
	sleep 5
	for x in ${CMDLINE}; do
		case ${x} in
			autotest=IGEP0020)
				exec ${XTERM} -e ${PYTHONBIN} ${TESTSUITE}/board_igep0020.py >/dev/null 2>&1 || status=$?
				exit ${status};
				;;
			autotest=IGEP0020_RC80C01)
				${PYTHONBIN} ${TESTSUITE}/board_igep0020.py RC80C01 >/dev/null 2>&1 || status=$?
				exit ${status};
				;;
			autotest=IGEP0033)
				${PYTHONBIN} ${TESTSUITE}/board_igep0033.py >/dev/tty0 2>&1 || status=$?
				exit ${status};
				;;
		esac
	done
}

do_start
