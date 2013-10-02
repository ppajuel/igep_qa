#!/bin/sh

# The first line contains the sender IP address
IPADDR=$(head -n 1 /tmp/log_test.txt)

# Print all except parameters
tail -n+2 /tmp/log_test.txt

# Wait client disconnection
echo -e "Waiting for disconnection ..."
while [ $? -eq 0 ]; do
    ping -c 2 ${IPADDR} -W 1 > /dev/null
done

echo "disconnected!"
