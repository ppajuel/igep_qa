#!/usr/bin/env python

"""
Audio Test Cases modules for unittest

"""

import os
import commands
import unittest

from igep_qa.helpers.common import is_in_path

class TestAudio(unittest.TestCase):
    """ Generic tests for audio interfaces.

    Keyword arguments:
        - testname : The name of the test to be executed.
        - device : Select the PCM device by name. This parameter is passed to
                   aplay and arecord using the -D option.
        - testdescription: Optional test description to overwrite the default.

    """
    def __init__(self, testname, device = '', testdescription = ''):
        super(TestAudio, self).__init__(testname)
        self.device = device
        # if not empty, add the -D option
        if device:
            self.device = '-D%s' % device
        # Overwrite test short description
        if testdescription:
            self._testMethodDoc = testdescription

    def test_audio_loopback(self):
        """ Test Audio : Loopback, sound sent to audio-out should return in audio-in

        Type: Functional

        Prerequisite commands:
            - aplay
            - arecord
            - multimon

        Prerequitsite files:
            - dtmf.wav (on contrib/dtmf.wav)

        Requirements:
            - Audio Mini jack-Stereo loopback cable.

        Description:
            - Connect the cable between Audio IN and Audio OUT connectors.
            - A sound with recorded DTMF tones is reproduced through Audio OUT
              and is simultaneously recorded via Audio IN.
            - Using demodulator multimon, it demodulates the recorded tune and
              gets the DMTF digits.

        """
        # Ensure requirements are installed.
        required = ["aplay", "arecord", "multimon"]
        files = "/usr/share/igep_qa/contrib/dtmf.wav"
        for req in required:
            if not is_in_path(req):
                raise Exception("Can't find %s" % req)
        if not os.path.isfile(files):
            raise Exception("Can't find %s" % files)
        commands.getoutput("rm -f /tmp/recorded.wav")
        commands.getoutput("aplay %s -t wav -v "
                           "/usr/share/igep_qa/contrib/dtmf.wav & arecord %s "
                           "-t wav -c 1 -r 8000 -f S16_LE -d 5 -v "
                           "/tmp/recorded.wav" % (self.device, self.device))
        commands.getoutput("multimon -t wav -a DTMF recorded.wav | grep 'DTMF: 5'")
        retval = commands.getstatusoutput("multimon -t wav -a DTMF "
                                          "/tmp/recorded.wav | grep 'DTMF: 5'")
        
        self.failUnless(retval[0] == 0, "failed: No DTMF found in recorded "
                        "file")

    def test_audio_playwav(self):
        """ Test Audio : Play a wav file

        Type: Functional

        Prerequisite commands:
            - aplay

        Prerequitsite files:
            - test.wav (on contrib/test.wav)

        Description:
            - This test only plays a wav file, a user must confirm that the file is played.

        """
        # Ensure requirements are installed.
        required = ["aplay"]
        files = "/usr/share/igep_qa/contrib/test.wav"
        for req in required:
            if not is_in_path(req):
                raise Exception("Can't find %s" % req)
        if not os.path.isfile(files):
            raise Exception("Can't find %s" % files)
        retval = commands.getstatusoutput("aplay %s -t wav "
                                          "/usr/share/igep_qa/contrib/test.wav"
                                           % self.device)
        self.failUnless(retval[0] == 0, "failed: Playing test.wav.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
