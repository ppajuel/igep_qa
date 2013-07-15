#!/usr/bin/env python

""" 
This provides helper functions for MADC module.

See: The TPS65950 Technical Reference Manual (TPS65950 ES 1.2 TRM vG )

"""

import struct
import fcntl

# from twl4030-madc.h
# struct twl4030_madc_user_parms {
#    int channel;
#    int average;
#    int status;
#    u16 result;
# };

class QMadc:
    """ Monitoring analog-to-digital converter
    
    The TPS65950 realizes analog-to-digital conversion of different signals
    like battery temperature, battery voltage and external signals. The MADC
    driver is used to monitor these signals.

    """
    def __init__(self, channel):
        """ Initialitze analog-to-digital converter

        The MADC allows 16 input channels for conversion. Of these, seven are
        external analog input channels (ADCIN0 and ADCIN2 to ADCIN7).
        See: The TPS65950 Technical Reference Manual (TPS65950 ES 1.2 TRM vG)
        
        Keyword arguments:
            - channel: The analog-to-digital converter

        """
        self.fd = open("/dev/twl4030-madc", "r+");
        self.channel = channel

    def __del__(self):
        self.fd.close()

    def raw_read(self):
        """ Read value from analog-to-digital converter
        
        Returns the average of 4 readings if average is True or the value of
        one read if average is False.

        """
        retval = struct.pack("iiiL", self.channel, 0, 0, 0)
        retval = fcntl.ioctl(self.fd, 0x6000, retval)
        retval = struct.unpack("iiiL", retval)
        # check for status of conversion
        if retval[2] == -1:
            raise Exception("Failed reading frommm analog-to-digital "
                            "converter")
        return retval[3]

    def voltage(self):
        """ Get the voltage value from analog-to-digital converter

        Returns the voltage from analog-to-digital converter rounded to 2
        decimals

        Analog Input (V) = conv_result * step_size/R
        Where:

            - conv_result = decimal value of 10-bit conversion result
            - step_size = 1.5/(2 10 - 1)
            - R = Prescaler ratio for input channel as given in Table 9-4

        Example 1: A 10-bit conversion result of 1010101010 for ADCIN12
        corresponds to a 4.0 V input VBAT level.

        Example 2: After a software/GP conversion on ADCIN9, the results are
        read as GPCH9_MSB = 0xB5 (on 8 bits, GPCH9_MSB[7:0]) and
        GPCH9_LSB = 0xC0 (on 2 bits, GPCH9_MSB[7:6]). This corresponds to
        the 1-bit conversion result of 1011010111 with a conv_result of
        727. With R = 1/3 for ADCIN9, the actual voltage of the backup
        battery equals approximately 3.2 V.

        See: Chapter 9.4.7 Interpretation of MADC Result Registers

        Attention: Note that the ADCIN9 (voltage of the backup battery) reads
        random values when nothing is connected to the BKBAT line.

        """
        step_size = 1.5 / 1023
        conv_result = self.raw_read()
        if (self.channel == 0 | self.channel == 1):
            retval = conv_result * step_size
        elif (self.channel > 1 | self.channel < 8):
            # channel 2 to 7 
            retval = conv_result * step_size / 0.6
        elif (self.channel == 8):
            retval = conv_result * step_size / 0.21
        elif (self.channel == 9):
            retval = conv_result * step_size / 0.33
        elif (self.channel == 11):
            retval = conv_result * step_size / 0.15
        elif (self.channel == 12):
            retval = conv_result * step_size / 0.25
        elif (self.channel == 15):
            retval = conv_result * step_size / 0.45
        return round(retval, 2)

if __name__ == '__main__':
    # Read battery backup
    madc = QMadc(9)
    print madc.raw_read()
    print madc.voltage()
