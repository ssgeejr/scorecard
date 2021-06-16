#!/usr/bin/env python3

import csv, time
import mysql.connector
from mysql.connector import connect, Error

def test_loadXRef():
    print("VALUE: ", fetchrefid('None'))
    print("VALUE: ", fetchrefid('Medium'))
    print("VALUE: ", fetchrefid('XNone'))


def fetchrefid(risk):
    result = -99;
    if risk == 'Critical': result = 0
    elif risk == 'High': result = 1
    elif risk == 'Medium': result = 2
    elif risk == 'Low': result = 3
    elif risk == 'None': result = -1
    return result

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
           xref = "insert ignore into plugin (pluginid,vulname,risk,riskid) values(%s,%s,%s,%s)"
           count = 0
           for lines in csvFile:
               if count > 0:
                   vulname = lines[7]
                   record = (lines[0],vulname[:64],lines[3],fetchrefid(lines[3]))
                   #print(record)
                   mycursor.execute(xref, record)
                   cnx.commit()
                   if (count % 1000) == 0:
                       print("commiting another 1000 records: " , count)
                   #if (count > 10): return
               count+=1

           cnx.commit()
           print("Total xref records loaded: " , count)
       except Error as e:
           print(" ***** ERROR FOUND ***** ")
           print("Error found at: ", count)
           print(lines)
           print(" *********************** ")
           print(e)

       
if __name__ == "__main__":
    loadXRef()
