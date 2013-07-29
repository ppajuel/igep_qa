#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup (name='igep_qa',
       version='0.1',
       description=u'IGEP Quality Assurance scripts',
       long_description=u'This is overall test software for IGEP Technology '
                        u'based devices, which defines test scope, test strategy, '
                        u'test configurations as well as test execution cycles. It '
                        u'will give readers an overview of validation activities done '
                        u'in any IGEP Technology based devices.',
       author='Enric Balletbo i Serra',
       author_email='eballetbo@iseebcn.com',
       url='',
       packages = ['igep_qa', 'igep_qa.helpers', 'igep_qa.runners', 'igep_qa.suites', 'igep_qa.tests'],
       data_files = [('/usr/share/igep_qa/contrib', ['contrib/dtmf.wav']),
                     ('/usr/share/igep_qa/contrib', ['contrib/test.wav']),
                     ('/etc/init.d', ['scripts/igep-qa.sh'])],
       license='LICENSE',
       classifiers = [
         'Intended Audience :: Developers',
         'License :: OSI Approved :: GNU General Public License (GPL)',
         'Natural Language :: English',
         'Operating System :: OS Independent',
         'Programming Language :: Python',
         'Topic :: Software Development :: Quality Assurance',
      ],
)
