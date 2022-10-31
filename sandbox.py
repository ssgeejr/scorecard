#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import re

import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path


def openConnection():
    config = configparser.ConfigParser()
    config.read('C:\\dev\\wmmc\\tethys\\tethys.ini')
    print('user: %s' % config['tethys']['user'])
    print('host: %s' % config['tethys']['host'])
    print('db: %s' % config['tethys']['db'])

    return mysql.connector.connect(user=config['tethys']['user'],
                                   password=config['tethys']['passwd'],
                                   host=config['tethys']['host'],
                                   database=config['tethys']['db'])


def sandbox():
    print('here we go')
    try:
        cnx = openConnection()
        mycursor = cnx.cursor()
        print('time to do it')
        '''
        SELECT
        scorecardid,
        pluginid,
        host,
        riskid,
        dtkey,
        rptdate,
        cve,
        cvss,
        protocol,
        port,
        name,
        synopsis,
        description,
        solution,
        see_also,
        plugin_output,
        hash
        FROM
        scorecard;
        '''

        sql = ("select"
               + " host,"
               + " plugin_output"
               + " from"
               + " scorecard"
               + " where"
               + " dtkey = '0422B'"
               + " and riskid = 0"
               + " and name like '%adobe%'"
               + " and host = 'cfme-citrix1.inhouse.wmmc'")

        print(sql)
        mycursor.execute(sql)
        #        results = mycursor.fetchall()
        results = mycursor.fetchone()
        for row in results:
            xlarge = row[1]
            xsmall = xlarge.decode("utf-8")
            #           print(xlarge)
            re.findall('File', xlarge)


    except Error as e:
        print('###---------- [ERR] SANDBOX ----------###')
        print(e)


def searchtest():
    pct = format(432.456, ".2f")
    print(pct)
    dtkey = '0422B'
    try:
        cnx = openConnection()
        mycursor = cnx.cursor()

        sql = "select keyindex from scorecard_xref where dtkey ='%s'"
        print(sql)
        mycursor.execute(sql % (dtkey))
        results = mycursor.fetchall()
        keyindex = -1
        for row in results:
            keyindex = row[0]
        if keyindex > -1:
            print('ERROR FOUND EXISTING DATE KEY')
            sys.exit(1)

        sql = "select max(keyindex) from scorecard_xref"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        for row in results:
            keyindex = row[0]

        print('KEY INDEX [', keyindex, ']')
        keyindex += 1
        print('NEW KEY INDEX [', keyindex, ']')
        sql = "insert into scorecard_xref(dtkey,keyindex) values('%s',%s)"
        mycursor.execute(sql % (dtkey, keyindex))
        cnx.commit()
    except Error as e:
        print('###---------- [ERR] COMPILE DATA ----------###')
        print(e)


def findPreviousDate():
    pct = format(432.456, ".2f")
    print(pct)
    dtkey = 'pppppp'
    try:
        config = configparser.ConfigParser()
        config.read('C:\\dev\\wmmc\\tethys\\tethys.ini')
        print('user: %s' % config['tethys']['user'])
        print('host: %s' % config['tethys']['host'])
        print('db: %s' % config['tethys']['db'])

        cnx = mysql.connector.connect(user=config['tethys']['user'],
                                      password=config['tethys']['passwd'],
                                      host=config['tethys']['host'],
                                      database=config['tethys']['db'])
        mycursor = cnx.cursor()

        sql = "select keyindex from scorecard_xref where dtkey ='%s'"
        print(sql)
        mycursor.execute(sql % (dtkey))
        results = mycursor.fetchall()
        keyindex = -1
        for row in results:
            keyindex = row[0]
        if keyindex == -1:
            print('ERROR FINDING DATA REFERENCE')
            sys.exit(1)
        print('KEY INDEX [', keyindex, ']')

    except Error as e:
        print('###---------- [ERR] COMPILE DATA ----------###')
        print(e)


if __name__ == "__main__":
    sandbox()
