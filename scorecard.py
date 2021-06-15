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
       for lines in csvFile:
           print(lines[0] + ' ' + lines[4] + ' ' + dt)



def db():
   try:
       with connect(
           host="localhost",
           user=input("Enter username: "),
           password=getpass("Enter password: "),
       ) as connection:
           print(connection)
   except Error as e:
       print(e)
   


if __name__ == "__main__":
#    main()
    db()
