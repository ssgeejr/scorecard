#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector
from mysql.connector import connect, Error
from pathlib import Path


dtkey = time.strftime('%m%y')
userDefinedKey = False

def fetchrefid(risk):
    result = -99;
    if risk == 'Critical': result = 0
    elif risk == 'High': result = 1
    elif risk == 'Medium': result = 2
    elif risk == 'Low': result = 3
    elif risk == 'None': result = -1
    return result

def fetchTableName(key):
    tablename = datetime.date(1900, int(key[:2]), 1).strftime('%b').lower() + key[2:]
    print(tablename)
    return tablename


def fetchFileStack():
   global dtkey
   global userDefinedKey 
   working_dir = "/opt/apps/sc.data"
   os.chdir(working_dir)
   for file in glob.glob("*.csv"):
       print('***** LOADING DATA FILE ', file, ' *****')
       old_file = os.path.join(working_dir,file)
       new_file = os.path.join(working_dir,file+'.old')
       print('Using data file: ', os.path.basename(old_file))

       if userDefinedKey:
           print('User Defined Key: ',dtkey)
       else:
           dtkey = Path(old_file).stem

       loadRawData(old_file)

       print('New File: ',new_file)
       print('***** FILE LOAD COMPLETED - RENAMING TO *.old *****')
       os.rename(old_file, new_file)

def loadRawData(datafile):
   global dtkey

   dt = time.strftime('%Y%m%d') 

   with open(datafile, mode ='r')as file:

   # reading the CSV file
       csvFile = csv.reader(file)
   


       print('USING DTKEY: ', dtkey)
       #return
   # displaying the contents of the CSV file
       try:
           cnx = mysql.connector.connect(user='scorecard', 
           password='scorecard',
           host='127.0.0.1',
           database='scorecard')
           print(cnx)
           mycursor = cnx.cursor()



           print('>>DTKEY: ',dtkey)
           tablename = fetchTableName(dtkey)
           print('Dropping/Creating Table: ', tablename)
           dropTable = ("DROP TABLE IF EXISTS " + tablename )
           createTable = ("CREATE TABLE " + tablename + " ("
           "datakey varchar(46) NOT NULL,"
           "pluginid varchar(8) NOT NULL,"
           "host varchar(32) NOT NULL,"
           "riskid int NOT NULL,"
           "dtkey varchar(8) NOT NULL,"
           "rptdate DATE NOT NULL,"
           "PRIMARY KEY (datakey)"
           ");")

           print(dropTable)
           mycursor.execute(dropTable)
           cnx.commit()

           print(createTable)
           mycursor.execute(createTable)
           cnx.commit()

           sql = "insert ignore into " + tablename + "(datakey,pluginid,host,riskid,dtkey,rptdate) values (%s, %s, %s, %s, %s, %s)"
           print(sql)

           xref = "insert ignore into plugin (pluginid,vulname,risk,riskid) values(%s,%s,%s,%s)"
           count = 0
           loaded_records = 0
           for lines in csvFile:
               if count > 0:
                   datakey = lines[0]+lines[4] 
                   refid = fetchrefid(lines[3])
                   if refid > -1: 
                      record = (datakey,lines[0],lines[4],refid, dtkey,dt)
                      vulname = lines[7]
                      xrecord = (lines[0],vulname[:64],lines[3],refid)
           #        print(record)
                   #print(lines[0] + ' ' + lines[4] + ' ' + dt)
                      mycursor.execute(sql, record)
                      mycursor.execute(xref, xrecord)
                      loaded_records+=1
                   #if count > 10: return
                      if (loaded_records % 1000) == 0:
                          cnx.commit()
                          print("commiting another 1000 records: " , loaded_records)
               count+=1
           cnx.commit()
           print("Total records scanned: " , count)
           print("Total records loaded: " , loaded_records)
       except Error as e:
           print('Error at line: ', count)
           print('******** INPUT LINE **********')
           print(lines)
           print('******************************')
           print(e)
       


def main(argv):
   global dtkey
   global userDefinedKey
   try:
      opts, args = getopt.getopt(argv,"hp:",["pkey="])
   except getopt.GetoptError:
      print ('dataloader.py -p <date>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('dataloade.py -p <date>')
         sys.exit()
      elif opt in ("-p", "--pkey"):
         userDefinedKey = True 
         dtkey = arg
   fetchFileStack()

if __name__ == "__main__":
    main(sys.argv[1:])
