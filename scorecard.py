#!/usr/bin/env python3

import csv, time
import mysql.connector
from mysql.connector import connect, Error


def main():
   dt = time.strftime('%Y%m%d') 
   # opening the CSV file
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
           count = 0
           for lines in csvFile:
               if count > 0:
                   record = (lines[0],lines[4],dt)
                   print(record)
                   #print(lines[0] + ' ' + lines[4] + ' ' + dt)
                   mycursor.execute(sql, record)
                   cnx.commit()
               count+=1
       except Error as e:
           print(e)
       


if __name__ == "__main__":
    main()
