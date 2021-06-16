#!/usr/bin/env python3

import csv, time
import mysql.connector
from mysql.connector import connect, Error




def XXXmainXXX():
    cntr=0
    while cntr < 1000:
        if (cntr % 100) == 0:
            print("modulous found: %s" , (cntr))
        cntr += 1




def main():
   dt = time.strftime('%Y%m%d') 
   # opening the CSV file
   #with open('../sc.data/data.csv.old', mode ='r')as file:
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
           sql = "insert into rawdata(pluginid,host,rptdate) values (%s, %s, %s)"
           #sql = "insert into rawdata(pluginid,host,vulname,rptdate) values (%s, %s, %s, %s)"
           count = 0
           for lines in csvFile:
               if count > 0:
                   record = (lines[0],lines[4],dt)
                   #print(record)
                   #print(lines[0] + ' ' + lines[4] + ' ' + dt)
                   mycursor.execute(sql, record)
                   if (count % 1000) == 0:
                       cnx.commit()
                       print("commiting another 1000 records: " , count)
               count+=1

           cnx.commit()
           print("Total records loaded: " , count)
       except Error as e:
           print('Error at line: ', count)
           print('******** INPUT LINE **********')
           print(lines)
           print('******************************')
           print(e)
       

def loadXRef():
   # opening the CSV file
   with open('../sc.data/data.csv.old', mode ='r')as file:

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
           xref = "insert ignore into plugin (pluginid,name) values(%s,%s)"
           count = 0
           for lines in csvFile:
               if count > 0:
                   vulname = lines[7]
                   record = (lines[0],vulname[:64])
                   print(record)
                   mycursor.execute(xref, record)
                   cnx.commit()
               count+=1

           cnx.commit()
           print("Total xref records loaded: " , count)
       except Error as e:
           print(e)
       
if __name__ == "__main__":
    main()
