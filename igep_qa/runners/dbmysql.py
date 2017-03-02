#!/usr/bin/env python

"""
Mysql DB Test Runner for unittest module

"""

import ConfigParser
import commands
import sys
import unittest

import mysql.connector
from mysql.connector import errorcode

from igep_qa.helpers.am33xx import cpu_is_am33xx
from igep_qa.helpers.am33xx import am335x_get_mac_id0
from igep_qa.helpers.am33xx import am335x_get_mac_id1
from igep_qa.helpers.common import get_hwaddr
from igep_qa.helpers.omap import cpu_is_omap5
from igep_qa.helpers.omap import omap3_get_dieid, omap5_get_dieid
from igep_qa.helpers.omap import machine_is_igep0020
from igep_qa.helpers.omap import machine_is_igep0032

PASS = '\033[32mPASS\033[0m\n'
FAIL = '\033[31mFAIL\033[0m\n'
ERROR = '\033[31mERROR\033[0m\n'

FANCYFAIL = """--------------------------------
\033[31m################################\033[0m

\033[31m########    ###    #### ##      \033[0m
\033[31m##         ## ##    ##  ##      \033[0m
\033[31m##        ##   ##   ##  ##      \033[0m
\033[31m######   ##     ##  ##  ##      \033[0m
\033[31m##       #########  ##  ##      \033[0m
\033[31m##       ##     ##  ##  ##      \033[0m
\033[31m##       ##     ## #### ########\033[0m

\033[31m################################\033[0m
"""

FANCYPASS = """-------------------------------------
\033[32m#####################################\033[0m

\033[32m########     ###     ######   ###### \033[0m
\033[32m##     ##   ## ##   ##    ## ##    ##\033[0m
\033[32m##     ##  ##   ##  ##       ##      \033[0m
\033[32m########  ##     ##  ######   ###### \033[0m
\033[32m##        #########       ##       ##\033[0m
\033[32m##        ##     ## ##    ## ##    ##\033[0m
\033[32m##        ##     ##  ######   ###### \033[0m

\033[32m#####################################\033[0m
"""

def updatedb(tests):
    # parse testsuite.conf configuration file
    config = ConfigParser.ConfigParser()
    # TODO : handle configuration file problems
    config.read('/etc/testsuite.conf')
    cfg = { }
    cfg['user'] = config.get('mysqld', 'user')
    # TODO : disabled password because don't work on DUT
    # cfg['password'] = config.get('mysqld', 'password') don't work for now on DUT!
    cfg['password'] = ''
    cfg['host'] = config.get('mysqld', 'host')
    cfg['database'] = config.get('mysqld', 'database')
    # TODO : disabled raise_on_warning because don't work on DUT
    # cfg['raise_on_warnings'] = config.get('mysqld', 'raise_on_warnings')
    interface = 'eth0'
    ipaddr = config.get('default', 'ipaddr')

    # ensure connection to server
    retval = commands.getstatusoutput("ifconfig %s %s" % (interface, ipaddr))
    if retval[0] != 0:
        return -1

    # connection to the database
    try:
        cnx = mysql.connector.connect(**cfg)
        cursor = cnx.cursor()

        # query of from server
        query = ("SELECT number FROM of ORDER BY id DESC LIMIT 1")
        cursor.execute(query)
        row = cursor.fetchone()
        if row is None:
            return -1
        num = row[0]

        # query sn from server
        query = ("SELECT number FROM sn ORDER BY id DESC LIMIT 1")
        cursor.execute(query)
        row = cursor.fetchone()
        if row is None:
            return -1
        snnum = row[0]

        # insert
        if machine_is_igep0020():
            add_testsuite = ("INSERT INTO testsuite"
                "(datetime, of, dieid, mac) "
                " VALUES (NOW(), %s, %s, %s)")
            data_testsuite = (num, omap3_get_dieid(), get_hwaddr("wlan0"))
        elif machine_is_igep0032():
            add_testsuite = ("INSERT INTO testsuite"
                "(datetime, of, dieid, mac) "
                " VALUES (NOW(), %s, %s, %s)")
            data_testsuite = (num, omap3_get_dieid(), '')
        elif cpu_is_am33xx():
            add_testsuite = ("INSERT INTO testsuite"
                "(datetime, of, dieid, mac) "
                " VALUES (NOW(), %s, %s, %s)")
            data_testsuite = (num, am335x_get_mac_id0(), am335x_get_mac_id1())
        elif cpu_is_omap5():
            add_testsuite = ("INSERT INTO testsuite"
                "(datetime, of, dieid, mac) "
                " VALUES (NOW(), %s, %s, %s)")
            data_testsuite = (num, omap5_get_dieid(), get_hwaddr("wlan0"))
        else:
            add_testsuite = ("INSERT INTO testsuite"
                "(datetime, of) "
                " VALUES (NOW(), %s)")
            data_testsuite = (num)
        cursor.execute(add_testsuite, data_testsuite)

        # insert test cases
        testsuite_id = cursor.lastrowid
        for t in tests:
            add_testcase = ("INSERT INTO testcase "
                   "(name, result, testsuite_id) "
                   "VALUES (%s, %s, %s)")
            data_testcase = (t['name'], t['result'], testsuite_id)
            # Insert new test
            cursor.execute(add_testcase, data_testcase)
        # Make sure data is committed to the database
        cnx.commit()
        # Close connections
        cursor.close()
        cnx.close()
        return 0
    # exception
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exists")
        else:
            print err
        cursor.close()
        cnx.close()
        return -1

class dbmysqlTestRunner:
    """ A Test Runner that pushes the results in a MySQL database.

    The module requires a configuration file (/etc/testsuite.conf) that consists of
    [mysqld] section followed by user, host and database name in the style of
    RFC 822. E.g.

    .. code-block:: ini

        [mysqld]
        user = username
        host = 127.0.0.1
        database = mydb

    """
    def __init__(self, stream=sys.stderr, verbosity=0):
        self.stream = stream
        self.verbosity = verbosity
        # A list of testcases
        self.tests = [ ]

    def writeUpdate(self, message):
        self.stream.write(message)

    def addNewTestCase(self, data):
        """ Append a new test case to the list of test cases ran by the test suite.

        """
        self.tests.append(data)

    def run(self, test):
        """ Run the given test case or test suite.

        """
        result = TextTestResult(self)
        test(result)
        result.testsRun
        # update database
        self.writeUpdate("Getting OF from server : ")
        if not updatedb(self.tests):
            self.writeUpdate(PASS)
        else:
            self.writeUpdate(FAIL)
        if (len(result.failures) + len(result.errors)):
            self.writeUpdate(FANCYFAIL)
        else:
            self.writeUpdate(FANCYPASS)

        return result

class TextTestResult(unittest.TestResult):
    """ Report test result in a human-readable format.

    """
    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner
        self.result = ERROR

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        # display: print test short description
        self.runner.writeUpdate("%s : " % test.shortDescription())

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.result = PASS

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.result = ERROR

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.result = FAIL

    def stopTest(self, test):
        unittest.TestResult.stopTest(self, test)
        # display: print test result
        self.runner.writeUpdate(self.result)
        # db: add new test case to the test suite
        dbdata = { }
        dbdata['name'] = test.shortDescription()
        dbdata['result'] = self.result
        self.runner.addNewTestCase(dbdata)
