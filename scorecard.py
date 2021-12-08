#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector
from mysql.connector import connect, Error
from datetime import datetime, date, timedelta
from pathlib import Path

dtval = '0921'

def main():
    try:
        cnx = mysql.connector.connect(user='scorecard',
                                      password='scorecard',
                                      host='tethys',
                                      database='scorecard')
        print(cnx)
        mycursor = cnx.cursor()

        riskCount = {}

        fetchMonthlyTotal = ("select"
                          " riskid,"
                          " count(*)"
                          " from"
                          " jul21"
                          " where"
                          " riskid >= 0"
                          " group"
                          " by"
                          " riskid"
                          " order"
                          " by"
                          " riskid"
                          " asc")

        print(fetchMonthlyTotal)

        mycursor.execute(fetchMonthlyTotal)
        results = mycursor.fetchall()
        monthlyData = "insert ignore into scorecard(dtkey,riskid,total,new, closed) values (%s, %s, %s, %s, %s)"
        riskCount = {}
        for row in results:
#            z_riskid = row[0]
#            z_total = row[1]

 #           changeQuery = (fetchMonthlyChanges % (xdate, row[0], adate, row[0]))
 #           mycursor.execute(changeQuery)
 #           results = mycursor.fetchall()
            print('RISKID %s COUNT %s' % (row[0], row[1]))
        print('______________________________________________')


    except Error as e:
        print('Error at line: ', count)
        print('******** INPUT LINE **********')
        print(lines)
        print('******************************')
        print(e)

if __name__ == "__main__":
    main()
