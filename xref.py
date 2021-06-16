#!/usr/bin/env python3

import csv, time
import mysql.connector
from mysql.connector import connect, Error

def loadXRef():
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
           xref = "insert ignore into plugin (pluginid,vulname) values(%s,%s)"
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
    loadXRef()
