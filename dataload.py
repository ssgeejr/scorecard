#!/usr/bin/env python3

import csv, time
import mysql.connector
from mysql.connector import connect, Error


def fetchrefid(risk):
    result = -99;
    if risk == 'Critical': result = 0
    elif risk == 'High': result = 1
    elif risk == 'Medium': result = 2
    elif risk == 'Low': result = 3
    elif risk == 'None': result = -1
    return result


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
           sql = "insert ignore into rawdata(datakey,pluginid,host,riskid,rptdate) values (%s, %s, %s, %s, %s)"
           count = 0
           for lines in csvFile:
               if count > 0:
                   datakey = lines[0]+lines[4] 
                   record = (datakey,lines[0],lines[4],fetchrefid(lines[3]),dt)
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
       

if __name__ == "__main__":
    main()
