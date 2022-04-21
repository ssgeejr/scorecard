#!/usr/bin/env python3


import csv, time, sys, getopt, glob, os, datetime
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path

dtkey = '0422A'
configFile = 'db.ini'
config = configparser.ConfigParser()

def compileData():
    global dtkey
    global configFile
    cdir = os.path.dirname(os.path.abspath(__file__))
    print('###---------- COMPILE DATA ----------###')
    print('Using Dataset Key: ', dtkey)


    try:
        print('**********************************************************')
        print('Configuration File: ', configFile)
        config_source = os.path.join(cdir, configFile)
        print('Configuration Source: ', config_source)
        config.read(config_source)
        print('user: %s' % config['tethys']['user'])
        print('host: %s' % config['tethys']['host'])
        print('db: %s' % config['tethys']['db'])
        print('**********************************************************')

        cnx = mysql.connector.connect(user=config['tethys']['user'],
                                      password=config['tethys']['passwd'],
                                      host=config['tethys']['host'],
                                      database=config['tethys']['db'])
        mycursor = cnx.cursor()

# ------------- TOTALS -------------

        sql = ("select"
               + " riskid as rid,"
               + " count(distinct hash) as total"
               + " from"
               + " scorecard"
               + " where"
               + " dtkey = '%s'"
               + " group by"
               + " riskid"
               + " order by"
               + " riskid")
        '''
        print(sql % (dtkey))
        mycursor.execute(sql % (dtkey))
        results = mycursor.fetchall()
        totals = {}
        grandTotal = 0
        for row in results:
            totals[row[0]] = row[1]
            grandTotal += row[1]

        print('Critical >> %s' % (totals[0]))
        print('High >> %s' % (totals[1]))
        print('Medium >> %s' % (totals[2]))
        print('Low >> %s' % (totals[3]))
        print('Grand Total >> %s' % (grandTotal))
        '''

# ------------- NEW TOTALS -------------

        sql = ("select "
               + " riskid as rid,"
               + " count(distinct hash) as total"
               + " from"
               + " scorecard"
               + " where"
               + " dtkey = '%s'"
               + " and riskid = %s"
               + " and hash not in ("
               + " select"
               + " distinct hash"
               + " from "
               + " scorecard"
               + " where"
               + " dtkey = '%s'"
               + " and riskid = %s"
               + " )"
               + " group by"
               + " rid")

        #need to get the last month keys :(
        rid = 0
        for rid in range(4):
            print('RID %s' % (rid))
            print(sql % (dtkey, rid, '0322B', rid))
            rid += 1


    except Error as e:
        print('###---------- [ERR] COMPILE DATA ----------###')
        print(e)


def main(argv):
    global dtkey
    global configFile
    try:
        opts, args = getopt.getopt(argv, "k:c:")
    except getopt.GetoptError as e:
        print('>>>> ERROR: %s' % str(e))
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-k':
            dtkey = arg
        elif opt in "-c":
            configFile = arg

#    print(dtkey)
#    print(configFile)

    compileData()

if __name__ == "__main__":
    main(sys.argv[1:])