#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector
from mysql.connector import connect, Error
from pathlib import Path

dtkey = time.strftime('%m%y')
userDefinedKey = False


def fetchRiskID(risk):
    result = -99;
    if risk == 'Critical':
        result = 0
    elif risk == 'High':
        result = 1
    elif risk == 'Medium':
        result = 2
    elif risk == 'Low':
        result = 3
    elif risk == 'None':
        result = -1
    return result


def fetchTableName(key):
    tablename = datetime.date(1900, int(key[:2]), 1).strftime('%b').lower() + key[2:]
    print(tablename)
    return tablename


def fetchFileStack():
    global dtkey
    global userDefinedKey
    #   working_dir = "/opt/apps/sc.data"
    working_dir = "/opt/apps/sc.data"
    os.chdir(working_dir)
    for file in glob.glob("*.csv"):
        print('***** LOADING DATA FILE ', file, ' *****')
        old_file = os.path.join(working_dir, file)
        new_file = os.path.join(working_dir, file + '.old')
        print('Using data file: ', os.path.basename(old_file))

        if userDefinedKey:
            print('User Defined Key: ', dtkey)
        else:
            dtkey = Path(old_file).stem

        testRawData(old_file)
        #      loadRawData(old_file)

        print('New File: ', new_file)
        print('***** FILE LOAD COMPLETED - RENAMING TO *.old *****')


#      os.rename(old_file, new_file)


def testRawData(datafile):
    global dtkey

    dt = time.strftime('%Y%m%d')

    with open(datafile, mode='r') as file:

        # reading the CSV file
        csvFile = csv.reader(file)

        print('USING DTKEY: ', dtkey)
        # return
        # displaying the contents of the CSV file
        try:

            print('>>DTKEY: ', dtkey)
            tablename = fetchTableName(dtkey)

            sql = "insert ignore into " + tablename + "(datakey,pluginid,host,riskid,dtkey,rptdate) values (%s, %s, %s, %s, %s, %s)"
            print(sql)

            xref = "insert ignore into plugin (pluginid,vulname,risk,riskid) values(%s,%s,%s,%s)"
            count = 0
            loaded_records = 0

            """
            0: 'Plugin ID'
            1: 'CVE'
            2: 'CVSS'
            3: 'Risk'
            4: 'Host'
            5: 'Protocol'
            6: 'Port'
            7: 'Name'
            8: 'Synopsis'
            9: 'Description'
            10: 'Solution'
            11: 'See Also'
            12: 'Plugin Output'
            """

            logfile = open("/tmp/output.sample.log", "w") 
            data = {}
            cvecnt = 0
            for lines in csvFile:

                if count > 0:
                    datakey = lines[0] + lines[4]
                    riskid = fetchRiskID(lines[3])
                    if riskid > -1:
                        record = (datakey, lines[0], lines[4], riskid, dtkey, dt)
                        vulname = lines[7]
                        xrecord = (lines[0], vulname[:64], lines[3], riskid)

                        #                        print(lines)

                        for x in range(13):
                            data[x] = fetchIndex(lines, x)
                        #print("***************************************")
                        #print(data[11])
                        #print("***************************************")
                        #if data[1] == 'CVE-2021-34456':
                        if data[0] == '156617':

                           logmsg = ("\n*************************************************"
                              +"\nPlugin ID: " + data[0]
                              +"\n_________________________________________________"
                              +"\nCVE: " + data[1]
                              +"\n_________________________________________________"
                              +"\nCVSS: " + data[2]
                              +"\n_________________________________________________"
                              +"\nRisk: " + data[3]
                              +"\n_________________________________________________"
                              +"\nHost: " + data[4]
                              +"\n_________________________________________________"
                              +"\nProtocol: " + data[5]
                              +"\n_________________________________________________"
                              +"\nPort: " + data[6]
                              +"\n_________________________________________________"
                              +"\nName: " + data[7]
                              +"\n_________________________________________________"
                              +"\nSynopsis: " + data[8]
                              +"\n_________________________________________________"
                              +"\nDescription: " + data[9]
                              +"\n_________________________________________________"
                              +"\nSolution: " + data[10]
                              +"\n_________________________________________________"
                              +"\nSee Also: " + data[11]
                              +"\n_________________________________________________"
                              +"\nPlugin Output: " + data[12])

                           #print(logmsg)
                           logfile.write(logmsg)
                           #print('******************************************************')
                           #print('******************************************************')
                           cvecnt += 1
                           print('***************** cvecnt[', cvecnt, '] ******************')
                           if cvecnt > 10: break

                        # print(lines[0] + ' ' + lines[4] + ' ' + dt)
                        loaded_records += 1
                        # if count > 10: return
                        if (loaded_records % 1000) == 0:
                            print("commiting another 1000 records: ", loaded_records)
                """
                else:
                    print('Plugin ID', lines[0]
                          + '\nCVE', lines[1]
                          + '\nCVSS', lines[2]
                          + '\nRisk', lines[3]
                          + '\nHost', lines[4]
                          + '\nProtocol', lines[5]
                          + '\nPort', lines[6]
                          + '\nName', lines[7]
                          + '\nSynopsis', lines[8]
                          + '\nDescription', lines[9]
                          + '\nSolution', lines[10]
                          + '\nSee Also', lines[11]
                          + '\nPlugin Output', lines[12])
                """
                count += 1
            print('>>>>>>>>>>>>CLOSING LOG FILE<<<<<<<<<<<<<<<<<')
            logfile.close()
            print("Total records scanned: ", count)
            print("Total records loaded: ", loaded_records)
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
        opts, args = getopt.getopt(argv, "hp:", ["pkey="])
    except getopt.GetoptError:
        print('dataloader.py -p <date>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('dataloade.py -p <date>')
            sys.exit()
        elif opt in ("-p", "--pkey"):
            userDefinedKey = True
            dtkey = arg
    fetchFileStack()


def fetchIndex(line, index):
    try:
        return line[index]
    except IndexError:
        return ''


if __name__ == "__main__":
    main(sys.argv[1:])
