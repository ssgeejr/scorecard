#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime, configparser
import mysql.connector
from mysql.connector import connect, Error
from datetime import datetime, date, timedelta
from pathlib import Path


config = configparser.ConfigParser()
dtkey: str = time.strftime('%m%y')


def selfConfig():
    configFile: str = 'tethys.ini'
    print('**********************************************************')
    print('Configuration File: ', configFile)
    config.read(configFile)

def testBuildParsing():
    item = ('Microsoft Windows 10 Enterprise Build 19045',
            'Microsoft Windows 10 Enterprise Build 19045',
            'Microsoft Windows 10 Enterprise Build 19045',
            'Microsoft Windows 10 Enterprise Build 19044')
    for os in item:
        if os.find(' Build') > 0:
            print(os[0:os.find(' Build')])



def main():
    selfConfig()
    try:
        print(config['tethys']['user'])
        print(config['tethys']['passwd'])
        print(config['tethys']['host'])
        print(config['tethys']['db'])
        cnx = mysql.connector.connect(user=config['tethys']['user'],
                                      password=config['tethys']['passwd'],
                                      host=config['tethys']['host'],
                                      database=config['tethys']['db'])
        mycursor = cnx.cursor()
        datafile = "C:\dloads\hosts_Oct1123.csv"
        print(f'Attempting to open data in readonly mode {datafile}')
        hostEntrySQL = "insert ignore into hosts(dtkey,name,ip,os,osbuild) values (%s, %s, %s, %s, %s)"
        print("***** ATTEMPTING TO SCRUB ALL PRIOR HOSTS *****")
        scrubTable = "delete from hosts where 1=1"
        mycursor.execute(scrubTable)
        cnx.commit()
        print("************************************************")
        xray = 999
        with open(datafile, mode='r') as file:
            csvFile = csv.reader(file)
            count = 0
            print('USING DTKEY: ', dtkey)
            try:
                loaded_records = 0
                for lines in csvFile:
                    if count > 0:
                        os = lines[2]
                        if os.find(' Build') > 0:
                            print(os[0:os.find(' Build')] + ' XXXX ' + os)
                            os = os[0:os.find(' Build')]

#                        print('DTKEY: %s, Hostname: %s, IP: %s, OS: %s', (dtkey,lines[0],lines[1],os,lines[2]))
                        values = (dtkey,lines[0],lines[1],os,lines[2])
                        mycursor.execute(hostEntrySQL, values)
                        loaded_records += 1
                        if (loaded_records % 250) == 0:
                            print(".....committing 250 records: ", loaded_records)
                            cnx.commit()
                            return 0
                    count += 1
                cnx.commit()
                print("Total records scanned: ", (count-1))
                print("Total records committed: ", loaded_records)

            except Error as e:
                print('Error at line: ', count)
                print(e)

    except Error as e:
        print('Error at line: ', "XXXXXXXXX")
        print('******** INPUT LINE **********')
        print("XXXXXXXXX")
        print('******************************')
        print(e)

if __name__ == "__main__":
    main()
