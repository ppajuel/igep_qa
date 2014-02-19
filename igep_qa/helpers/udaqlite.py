#!/usr/bin/env python

import argparse
import sys
import socket
import SocketServer

from ctypes import c_long, byref, CDLL

class EdreQueryDeviceCodes():
    """
    Device related query codes

        - BRDTYPE Query the device type.
        - BRDREV Query the device revision.
        - BRDYEAR Query the year the device was manufactured.
        - BRDMONTH Query the month the device was manufactured.
        - BRDDAY Query the day the device was manufactured.
        - BRDSERIALNO Query the device serial number.
        - BRDBUSTYPE Query the device bus type.
        - BRDDRVTYPE Query the device driver type.
        - BRDBASEADDR Query the device base address. Only related to ISA type devices.
        - BRDINDEX Query the device index in the current device list.

    """
    BRDTYPE = 10
    BRDREV = 11
    BRDYEAR = 12
    BRDMONTH = 13
    BRDDAY = 14
    BRDSERIALNO = 15
    BRDBUSTYPE = 16
    BRDDRVTYPE = 17
    BRDBASEADDR = 18
    BRDINDEX = 19

class uDAQliteServer(SocketServer.BaseRequestHandler):
    """
    The uDAQliteServer class for our ammeter server.

    The uDAQ-Lite is a low cost USB data acquisition device that incorporates A/D,
    D/A, digital I/O and counter-timer functions. It supports 8 analog input
    channels, 2 analog output channels, 8 input and 8 digital I/O and 1 counter
    timer channel.

    Here, the uDAQ-Lite, is used as a ammeter, using a shunt resitor to measure
    the current.

    """
    def handle(self):
        """
        Sends to client the value of current in amps.

        At the moment the server is not as parametric as should and there some
        fixed values:
            - port: 1
            - range: 3 for Bipolar differential
            - gain: 3 for -1.25V - +1.25 V (Bipolar differential)
            - shunt: 0.15 Ohms shunt resistor

        """
        PORT, GAIN, RANGE, SHUNT = 1, 3, 3, 0.15
        data = c_long()
        # Open shared library
        edre = CDLL("/usr/lib/libedreapi-2.0.11.so.0")
        # Query for serial number
        query = edre.EDRE_Query
        serialnum = query(0, EdreQueryDeviceCodes.BRDSERIALNO, 0);
        #  Read a A/D voltage
        single = edre.EDRE_ADSingle
        err = single(serialnum, PORT, GAIN, RANGE, byref(data))
        if err:
            retval = edre.ShowError(err)
        else:
            # send the current value
            retval = '{0:.3g}'.format((data.value / 1000000.0) / SHUNT)
        self.request.sendall(retval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='description', epilog='eplilog')

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-c', nargs=2, dest='runClient', help='Run as a client.', metavar=("<ip>", "<port>"))
    group.add_argument('-s', nargs=2, dest='runServer', help='Run as a server.', metavar=("<ip>", "<port>"))

    args = parser.parse_args()

    if args.runClient:
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            sock.connect((args.runClient[0], int(args.runClient[1])))
            sock.sendall("\n")
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
        print received
    elif args.runServer:
        # Create the server, binding to 'host' on port 'port'
        server = SocketServer.TCPServer((args.runServer[0], int(args.runServer[1])), uDAQliteServer)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    else:
        print parser.print_help()
        sys.exit(1)
