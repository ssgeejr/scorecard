#!/usr/bin/env python3

import csv, time, sys, getopt
import mysql.connector
from mysql.connector import connect, Error


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

def loadRawData():
   global userDefinedKey 
   if userDefinedKey:
       print('using User Defined Key')

   dt = time.strftime('%Y%m%d') 
   #dtkey = time.strftime('%m%y')
   # opening the CSV file
   #with open('../sc.data/data.csv.old', mode ='r')as file:

   return


   with open('../sc.data/data.csv', mode ='r')as file:

   # reading the CSV file
       csvFile = csv.reader(file)
   
   # displaying the contents of the CSV file
       try:
           cnx = mysql.connector.connect(user='scorecard', 
           password='scorecard',
           host='127.0.0.1',
           database='scorecard')
           print(cnx)
           mycursor = cnx.cursor()
           sql = "insert ignore into rawdata(datakey,pluginid,host,riskid,rptdatekey,rptdate) values (%s, %s, %s, %s, %s, %s)"
           count = 0
           for lines in csvFile:
               if count > 0:
                   datakey = dtkey+lines[0]+lines[4] 
                   record = (datakey,lines[0],lines[4],fetchrefid(lines[3]),dtkey,dt)
           #        print(record)
                   #print(lines[0] + ' ' + lines[4] + ' ' + dt)
                   mycursor.execute(sql, record)
                   #if count > 10: return
                   if (count % 1000) == 0:
                       cnx.commit()
                       print("commiting another 1000 records: " , count)
               count+=1

           print("Total records loaded: " , count)
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
   print ('Month Year Key: ', dtkey)
   loadRawData()

if __name__ == "__main__":
    main(sys.argv[1:])
