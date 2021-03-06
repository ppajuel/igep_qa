#!/bin/sh
### BEGIN INIT INFO
# Provides:          igep-qa.sh
# Required-Start:    mountnfs.sh
# Should-Start:
# Required-Stop:
# Should-Stop:
# Default-Start:     5
# Default-Stop:
# Short-Description: IGEP-QA init script for IGEP-technology devices.
# Description:       This script should be placed in /etc/init.d
### END INIT INFO
#set -x

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
				# Set display depth to 16 bits per pixel, otherwise letters in red color
				# are not printed
				fbset -depth 16
				# Clear the tty0 terminal
				clear > /dev/tty0
				exec ${XTERM} -e ${PYTHONBIN} ${TESTSUITE}/board_igep0020.py >/dev/null 2>&1 || status=$?
				exit ${status};
				;;
			autotest=IGEP0020_RC80C01)
				# Set display depth to 16 bits per pixel, otherwise letters in red color
				# are not printed
				fbset -depth 16
				# Clear the tty0 terminal
				clear > /dev/tty0
				${PYTHONBIN} ${TESTSUITE}/board_igep0020.py RC80C01 >/dev/null 2>&1 || status=$?
				exit ${status};
				;;
			autotest=IGEP0033)
				# Set display depth to 16 bits per pixel, otherwise letters in red color
				# are not printed
				fbset -depth 16
				# Clear the tty0 terminal
				clear > /dev/tty0
				${PYTHONBIN} ${TESTSUITE}/board_igep0033.py >/dev/tty0 2>&1 || status=$?
				exit ${status};
				;;
			autotest=IGEP0050)
				# Set display depth to 16 bits per pixel, otherwise letters in red color
				# are not printed
				fbset -depth 16
				# Clear the tty0 terminal
				clear > /dev/tty0
				${PYTHONBIN} ${TESTSUITE}/board_igep0050.py >/dev/tty0 2>&1 || status=$?
				exit ${status};
				;;
			autotest=IGEP0050_RB20)
				# Set display depth to 16 bits per pixel, otherwise letters in red color
				# are not printed
				fbset -depth 16
				# Clear the tty0 terminal
				clear > /dev/tty0
				${PYTHONBIN} ${TESTSUITE}/board_igep0050.py RB20 >/dev/tty0 2>&1 || status=$?
				exit ${status};
				;;
			autotest=BASE0010)
				# Set display depth to 16 bits per pixel, otherwise letters in red color
				# are not printed
				fbset -depth 16
				# Clear the tty0 terminal
				clear > /dev/tty0
				${PYTHONBIN} ${TESTSUITE}/board_base0010.py >/dev/tty0 2>&1 || status=$?
				exit ${status};
				;;
			autotest=SLNK0010)
				# Set display depth to 16 bits per pixel, otherwise letters in red color
				# are not printed
				fbset -depth 16
				# Clear the tty0 terminal
				clear > /dev/tty0
				${PYTHONBIN} ${TESTSUITE}/board_slnk0010.py >/dev/tty0 2>&1 || status=$?
				exit ${status};
				;;
			autotest=IGEP0034)
				# Set display depth to 16 bits per pixel, otherwise letters in red color
				# are not printed
				fbset -depth 16
				# Clear the tty0 terminal
				clear > /dev/tty0
				# FIXME: Enable USB Host power to avoid "musb-hdrc musb-hdrc.2.auto: Babble" issue
				echo enabled > /sys/devices/platform/regulators/regulators\:fixedregulator\@4/regulator/regulator.19/userspace-consumer\@1-usb_power/state
				sleep 4
				read BOARDMODEL < /sys/firmware/devicetree/base/model
				if [ "$BOARDMODEL" = "ISEE IGEP SMARC AM3354 Kit" ]; then
					# fb-test is a dependency for IGEP0034 (FULL) test
					if [ -f /usr/bin/fb-test ]; then
						exec sh -c "${PYTHONBIN} ${TESTSUITE}/board_igep0034.py" >/dev/tty1 2>&1 || status=$?
						exit ${status};
					else
						echo "${NAME}: Error /usr/bin/fb-test is not found. Aborted IGEP0034 (FULL) test."
					fi
				fi
				if [ "$BOARDMODEL" = "ISEE IGEP SMARC AM3352 Lite Kit" ]; then
					clear > /dev/ttyO0
					exec sh -c "${PYTHONBIN} ${TESTSUITE}/board_igep0034.py LITE" >/dev/ttyO0 2>&1 || status=$?
					exit ${status};
				fi
				;;
			autotest=IGEP0046)
				# Clear the tty0 terminal
				reset > /dev/tty0
				read BOARDMODEL < /proc/device-tree/model
				if [ "$BOARDMODEL" = "ISEE IGEP i.MX6 Quad SMARC Kit Rev C2" ]; then
					# /usr/bin/gst-launch is a dependency for IGEP0046 test
					if [ -f /usr/bin/gst-launch ]; then
						# Enable DVI fb-test pattern
						/bin/echo 0 > /sys/class/graphics/fb2/blank
						/usr/bin/gst-launch filesrc location=/usr/igep_qa/contrib/fb-test-720p.png ! pngdec ! ffmpegcolorspace ! freeze ! imxv4l2sink device=/dev/video19 &

						exec sh -c "${PYTHONBIN} ${TESTSUITE}/board_igep0046.py QuadC2" >/dev/tty1 2>&1 || status=$?
						exit ${status};
					else
						echo "${NAME}: Error /usr/bin/gst-launch is not found. Aborted ${BOARDMODEL} test."
					fi
				fi
				if [ "$BOARDMODEL" = "ISEE IGEP i.MX6 Quad SMARC Kit Rev D102" ]; then
					# /usr/bin/gst-launch is a dependency for IGEP0046 test
					if [ -f /usr/bin/gst-launch ]; then
						# Enable DVI fb-test pattern
						/bin/echo 0 > /sys/class/graphics/fb2/blank
						/usr/bin/gst-launch filesrc location=/usr/igep_qa/contrib/fb-test-720p.png ! pngdec ! ffmpegcolorspace ! freeze ! imxv4l2sink device=/dev/video19 &

						exec sh -c "${PYTHONBIN} ${TESTSUITE}/board_igep0046.py QuadD102" >/dev/tty1 2>&1 || status=$?
						exit ${status};
					else
						echo "${NAME}: Error /usr/bin/gst-launch is not found. Aborted ${BOARDMODEL} test."
					fi
				fi
				if [ "$BOARDMODEL" = "ISEE IGEP i.MX6 DualLite SMARC Kit Rev D102" ]; then
					exec sh -c "${PYTHONBIN} ${TESTSUITE}/board_igep0046.py DualLiteD102" >/dev/tty1 2>&1 || status=$?
					exit ${status};
				fi
				;;
		esac
	done
}

do_start
