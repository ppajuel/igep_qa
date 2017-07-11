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
    def __init__(self, testname, device='', testdescription=''):
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
        files = "/usr/igep_qa/contrib/dtmf.wav"
        for req in required:
            if not is_in_path(req):
                raise Exception("Can't find %s" % req)
        if not os.path.isfile(files):
            raise Exception("Can't find %s" % files)
        commands.getoutput("rm -f /tmp/recorded.wav")
        commands.getoutput("aplay %s -t wav -v "
                           "/usr/igep_qa/contrib/dtmf.wav & arecord %s "
                           "-t wav -c 1 -r 8000 -f S16_LE -d 5 -v "
                           "/tmp/recorded.wav" % (self.device, self.device))

        retval = commands.getstatusoutput("multimon -t wav -a DTMF "
                                          "/tmp/recorded.wav | grep 'DTMF: 5'")

        self.failUnless(retval[0] == 0, "failed: No DTMF found in recorded "
                        "file")

    def test_audio_workaround_loopback(self):
        """ Test Audio WORKAROUND: Loopback, sound sent to audio-out should return in audio-in

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
            Sometimes, IGEP0046 with BASE0040 hangs during test_audio_loopback due a Kernel bug.
            test_audio_workaround_loopback avoids hang issue and test multiple times audio
            loopback to difer between Hardware error and Software error.

            - Connect the cable between Audio IN and Audio OUT connectors.
            - A sound with recorded DTMF tones is reproduced through Audio OUT
              and is simultaneously recorded via Audio IN.
            - Using demodulator multimon, it demodulates the recorded tune and
              gets the DMTF digits.

        """
        import subprocess

        # Ensure requirements are installed.
        required = ["aplay", "arecord", "multimon"]
        files = "/usr/igep_qa/contrib/dtmf.wav"
        for req in required:
            if not is_in_path(req):
                raise Exception("Can't find %s" % req)
        if not os.path.isfile(files):
            raise Exception("Can't find %s" % files)

        for retry in range(3):
            commands.getoutput("rm -f /tmp/recorded.wav")
            fd = os.open("/tmp/foo.txt", os.O_RDWR|os.O_CREAT)
            subprocess.Popen(["aplay", "-t", "wav", "-v", "/usr/igep_qa/contrib/dtmf.wav"],
                           stdin=None, stdout=fd, stderr=fd)
            commands.getoutput("arecord %s -t wav -c 1 -r 8000 -f S16_LE -d 5 -v "
                           "/tmp/recorded.wav" % self.device)
            commands.getoutput("killall aplay")
            os.close(fd)

            retval = commands.getstatusoutput("multimon -t wav -a DTMF "
                                  "/tmp/recorded.wav | grep 'DTMF: 5'")
            if retval[0] == 0:
                break

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
        files = "/usr/igep_qa/contrib/test.wav"
        for req in required:
            if not is_in_path(req):
                raise Exception("Can't find %s" % req)
        if not os.path.isfile(files):
            raise Exception("Can't find %s" % files)
        retval = commands.getstatusoutput("aplay %s -t wav "
                                          "/usr/igep_qa/contrib/test.wav"
                                           % self.device)
        self.failUnless(retval[0] == 0, "failed: Playing test.wav.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
