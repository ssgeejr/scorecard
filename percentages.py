#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector
from mysql.connector import connect, Error
from datetime import datetime, date, timedelta
from pathlib import Path

dtval = '0521'



def getLastMonth(month):
    my_date = datetime.strptime(month, "%m%y")
    last_month = my_date - timedelta(1)
    # return str(last_month.strftime('%m%y'))
    return ((my_date.strftime('%b').lower()) + my_date.strftime("%y"), (last_month.strftime('%b').lower()) + last_month.strftime("%y"))

def main():
    try:
        cnx = mysql.connector.connect(user='scorecard',
                                      password='scorecard',
                                      host='tethys',
                                      database='scorecard')
        print(cnx)
        mycursor = cnx.cursor()

        riskCount = {}

        fetchRiskCount = ("select"
                          " riskid,"
                          " count(*)"
                          " from"
                          " jul21 "
                          " where riskid >= 0"
                          " group by riskid"
                          " order by riskid asc")
        print(fetchRiskCount)

        adate,xdate = getLastMonth(dtval)
        print('This Month %s && Last Month %s' % (adate, xdate))

        fetchMonthlyChanges = ("select"
            " count(*)"
            " from"
            " %s"
            " where"
            " riskid = %s"
            " and"
            " datakey not in ("
            " select"
            " datakey"
            " from"
            " %s"
            " where"
            " riskid = %s"
            ")")

        print(fetchMonthlyChanges)
        # riskidkey = ('0','1','2','3')

        mycursor.execute(fetchRiskCount)
        results = mycursor.fetchall()
        monthlyData = "insert ignore into scorecard(dtkey,riskid,total,new, closed) values (%s, %s, %s, %s, %s)"
        riskCount = {}
        for row in results:
            z_riskid = row[0]
            z_total = row[1]
            z_new = 0
            z_closed = 0
            riskCount[row[0]] = row[1]
            print("RiskID: %s, Count: %s" % (row[0], row[1]))

            changeQuery = (fetchMonthlyChanges % (adate, row[0], xdate, row[0]))
            try:
                mycursor.execute(changeQuery)
                results = mycursor.fetchall()
                for new in results:
                    print('NEW %s >> %s' % (row[0], new[0]))
                    z_new = new[0]
            except Error as e:
                print(e)
                z_new = 0

            try:
                changeQuery = (fetchMonthlyChanges % (xdate, row[0], adate, row[0]))
                mycursor.execute(changeQuery)
                results = mycursor.fetchall()
                for closed in results:
                    print('CLOSED %s >> %s' % (row[0], closed[0]))
                    z_closed = closed[0]
            except Error as e:
                print(e)
                z_closed = 0

            datavalues = (dtval, z_riskid, z_total, z_new, z_closed)
            mycursor.execute(monthlyData, datavalues)
        cnx.commit()

        for rid, rcnt in riskCount.items():
            fetchTop10 = ("select count(*), a.pluginid, b.vulname from"
                          " %s a, plugin b"
                          " where"
                          " a.riskid = %s"
                          " and a.pluginid = b.pluginid"
                          " group by"
                          " a.pluginid"
                          " order by"
                          " count(*) desc" % (adate, rid))
            print(fetchTop10)

            mycursor.execute(fetchTop10)
            results = mycursor.fetchall()
            key = 0
            currentotal = 0
            print('*************************************************************')
            riskTopData = "insert ignore into carddata(dtkey,riskid,pluginid,total,pct) values (%s, %s, %s, %s, %s)"
            for row in results:
                key += 1
                percent = round(((row[0] / rcnt) * 100))
                currentotal += row[0]
                print("RiskID %s, Risk Total %s, Total: %s , Pct: %s, Plugin-ID: %s, Vulnerability: %s " % (rid, rcnt, row[0], percent, row[1], row[2]))

                topDataVal = (dtval, rid, row[1], row[0], percent)
                mycursor.execute(riskTopData, topDataVal)

                if key == 10:
                    break

            cnx.commit()


            print(currentotal)
            percent = (currentotal / rcnt) * 100
            print('Total Pct for Top 10: %s' % (round(percent)))
            print('______________________________________________')


    except Error as e:
        print('Error at line: ', count)
        print('******** INPUT LINE **********')
        print(lines)
        print('******************************')
        print(e)


def example():
    critical = [566, 565, 422, 81, 57, 43, 43, 43, 42, 42]
    total = 2981

    print("***** CRITICAL *****")
    for num in critical:
        quotient = num / total
        percent = quotient * 100
        print("Total: %s , Pct: %s" % (num, round(percent)))

    critical = [598, 593, 590, 590, 590, 587, 583, 580, 577, 285]
    total = 16520

    print("***** HIGH *****")
    for num in critical:
        quotient = num / total
        percent = quotient * 100
        print("Total: %s , Pct: %s" % (num, round(percent)))


if __name__ == "__main__":
    main()