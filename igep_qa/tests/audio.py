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

    """
    def setUp(self):
        """ Ensure requirements are installed.

        """
        required = ["aplay", "arecord", "multimon"]
        files = "/opt/igep-qa/contrib/dtmf.wav"
        for req in required:
            if not is_in_path(req):
                raise Exception("Can't find %s" % req)
        if not os.path.isfile(files):
            raise Exception("Can't find %s" % files)

    def test_audio_loopback(self):
        """ Audio IN/OUT loopback

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
        commands.getoutput("rm -f /tmp/recorded.wav")
        commands.getoutput("aplay -t wav -v /usr/share/igep_qa/contrib/dtmf.wav & arecord -t wav -c 1 "
                           "-r 8000 -f S16_LE -d 5 -v /tmp/recorded.wav")
        commands.getoutput("multimon -t wav -a DTMF recorded.wav | grep 'DTMF: 5'")
        retval = commands.getstatusoutput("multimon -t wav -a DTMF "
                                          "/tmp/recorded.wav | grep 'DTMF: 5'")
        
        self.failUnless(retval[0] == 0, "failed: No DTMF found in recorded "
                        "file")

if __name__ == '__main__':
    unittest.main(verbosity=2)