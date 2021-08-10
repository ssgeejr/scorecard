#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector
from mysql.connector import connect, Error
from datetime import datetime, date, timedelta
from pathlib import Path

dtval = '0721'



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

        fetchClosedByRisk = ("select"
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
        print(fetchClosedByRisk)
        xxx = ('0','1','2','3')
        for row in xxx:
            output = (fetchClosedByRisk % (adate, row[0], xdate, row[0]))
            print(output)




        exit(0)




#TODO
# CALCULATE OLD/NEW
## NEW ITEMS
# select
#         count(*)
#     from
#     jul21
# where
# riskid = X
# and
# datakey not in (
#     select
#     datakey
#     from
#     jun21
#     where
#     riskid = X
# )
## CLOSED ITEMS
# select
#     count(*)
# from
#     jun21
# where
# riskid = X
# and
# datakey not in (
#     select
#     datakey
#     from
#     jul21
#     where
#     riskid = X
# )



        mycursor.execute(fetchRiskCount)
        results = mycursor.fetchall()
        monthlyData = "insert ignore into scorecard(dtkey,riskid,total) values (%s, %s, %s)"
        for row in results:
            print("RiskID: %s, Count: %s" % (row[0], row[1]))
            riskCount[row[0]] = row[1]
            dataset = (dtval, row[0], row[1])
            mycursor.execute(monthlyData, dataset)
        cnx.commit()
        print(riskCount)

        for rid, rcnt in riskCount.items():
            fetchTop10 = ("select count(*), a.pluginid, b.vulname from"
                          " jul21 a, plugin b"
                          " where"
                          " a.riskid = %s"
                          " and a.pluginid = b.pluginid"
                          " group by"
                          " a.pluginid"
                          " order by"
                          " count(*) desc" % (rid))
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