#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path

dtkey = ''
configFile = 'db.ini'
config = configparser.ConfigParser()

### **********[[COMPILE_DATA]]**********
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

        sql = ("select"
               + " dtkey"
               + " from"
               + " scorecard_xref"
               + " where"
               + " keyindex = "
               + " (select"
               + " (keyindex - 1)"
               + " from"
               + " scorecard_xref"
               + " where"
               + " dtkey = '%s')" )
        olddtkey = ''
        '''
        print(sql % (dtkey))
        mycursor.execute(sql % (dtkey))
        results = mycursor.fetchall()
        for row in results:
            olddtkey = row[0]
        print('olddtkey: ', olddtkey)
        '''

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

        totals = []
        total_new = []
        totals_closed = []
        grandTotal = 0
        grandTotal_new = 0
        grantTotal_closed = 0

        '''
        print(sql % (dtkey))
        mycursor.execute(sql % (dtkey))
        results = mycursor.fetchall()
        
        grandTotal = 0
        for row in results:
            totals.insert(row[0], row[1])
            grandTotal += row[1]
        '''

        grandTotal = 24016
        totals.insert(0, 2287)
        totals.insert(1, 9426)
        totals.insert(2, 11473)
        totals.insert(3, 830)
        olddtkey = '0322B'

        print('Critical >> %s' % (totals[0]))
        print('High >> %s' % (totals[1]))
        print('Medium >> %s' % (totals[2]))
        print('Low >> %s' % (totals[3]))
        print('Grand Total >> %s' % (grandTotal))

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

# ------------- NEW ITEMS -------------
        rid = 0
        for rid in range(4):
#            print('RID %s' % (rid))
#            print(sql % (dtkey, rid, olddtkey, rid))
            mycursor.execute(sql % (dtkey, rid, olddtkey, rid))
            results = mycursor.fetchall()
            for row in results:
                total_new.insert(row[0], row[1])
                grandTotal_new += row[1]
            rid += 1
        print('------------- NEW ITEMS -------------')
        print('Critical >> %s' % (total_new[0]))
        print('High >> %s' % (total_new[1]))
        print('Medium >> %s' % (total_new[2]))
        print('Low >> %s' % (total_new[3]))
        print('Grand Total >> %s' % (grandTotal_new))
        print('-------------------------------------')

# ------------- CLOSED ITEMS -------------
        rid = 0
        for rid in range(4):
#            print('RID %s' % (rid))
#            print(sql % (olddtkey, rid, dtkey, rid))
            mycursor.execute(sql % (olddtkey, rid, dtkey, rid))
            results = mycursor.fetchall()
            for row in results:
                totals_closed.insert(row[0], row[1])
                grantTotal_closed += row[1]
            rid += 1

        print('------------- CLOSED ITEMS -------------')
        print('Critical >> %s' % (totals_closed[0]))
        print('High >> %s' % (totals_closed[1]))
        print('Medium >> %s' % (totals_closed[2]))
        print('Low >> %s' % (totals_closed[3]))
        print('Grand Total >> %s' % (grantTotal_closed))
        print('-------------------------------------')

# ------------- CALCULATE PERCENTAGES -------------
# -- NOT VALID FOR BI-WEEKLY CALCULATIONS

    except Error as e:
        print('###---------- [ERR] COMPILE DATA ----------###')
        print(e)


### **********[[MAIN]]**********
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

### **********[[CONSTRUCTOR]]**********
if __name__ == "__main__":
    main(sys.argv[1:])