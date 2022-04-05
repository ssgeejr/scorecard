#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector, configparser
from mysql.connector import connect, Error
from pathlib import Path

dtkey = time.strftime('%m%y')
userDefinedKey = False
configFile = 'db.ini'

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


def validateData(a_list, key):
    try:
        return a_list[key]
    except IndexError:
        return ''


def fetchFileStack():
    global dtkey
    global userDefinedKey
    #   working_dir = "/opt/apps/sc.data"
    working_dir = "C:/dev/wmmc/tethys_data"
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

        loadScoredataData(old_file)

        print('New File: ', new_file)
        print('***** FILE LOAD COMPLETED - RENAMING TO *.old *****')
#      os.rename(old_file, new_file)


def loadScoredataData(datafile):
    global dtkey

    dt = time.strftime('%Y%m%d')

    with open(datafile, mode='r') as file:

        # reading the CSV file
        csvFile = csv.reader(file)
        count = 0
        print('USING DTKEY: ', dtkey)
        # return
        # displaying the contents of the CSV file
        try:
            config = configparser.ConfigParser()
            #config.read('db.ini')

            print('USING CONFIG FILE: ', configFile)
            config.read(os.path.join(os.path.dirname(__file__), configFile))

            cnx = mysql.connector.connect(user=config['tethys']['user'],
                                          password=config['tethys']['passwd'],
                                          host=config['tethys']['host'],
                                          database=config['tethys']['db'],
                                          autocommit=config['tethys']['commit'])

#            cnx.autocommit = True

            print(cnx)
            mycursor = cnx.cursor()

            sql = ("insert into scorecard"
              +" (dtkey,"
              +" rptdate,"
              +" pluginid,"
              +" cve,"
              +" cvss,"
              +" riskid,"
              +" host,"
              +" protocol,"
              +" port,"
              +" name,"
              +" synopsis,"
              +" description,"
              +" solution,"
              +" see_also,"
              +" plugin_output)"
              +" values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

            print(sql)

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

            for lines in csvFile:
                if count > 0:
                    datakey = lines[0] + lines[4]
                    riskid = fetchRiskID(lines[3])
                    if riskid > -1:
                        '''
                        print("*************************************************");
                        print("datakey: " + datakey);
                        print("_________________________________________________");
                        print("dtkey: " + dtkey);
                        print("_________________________________________________");
                        print("dt: " + dt);
                        print("_________________________________________________");
                        print("[0]Plugin ID: " + lines[0]);
                        print("_________________________________________________");
                        print("[1]CVE: " + validateData(lines, 1));
                        print("_________________________________________________");
                        print("[2]CVSS: " + validateData(lines, 2));
                        print("_________________________________________________");
                        print("[3]Risk: " + lines[3]);
                        print("_________________________________________________");
                        print("[4]Host: " + lines[4]);
                        print("_________________________________________________");
                        print("[5]Protocol: " + validateData(lines, 5));
                        print("_________________________________________________");
                        print("[6]Port: " + validateData(lines, 6));
                        print("_________________________________________________");
                        print("[7]Name: " + validateData(lines, 7));
                        print("_________________________________________________");
                        print("[8]Synopsis: " + validateData(lines, 8));
                        print("_________________________________________________");
                        print("[9]Description: " + validateData(lines, 9));
                        print("_________________________________________________");
                        print("[10]Solution: " + validateData(lines, 10));
                        print("_________________________________________________");
                        print("[11]See Also: " + validateData(lines, 11));
                        print("_________________________________________________");
                        print("[12]Plugin Output: " + validateData(lines, 12));
                        '''


                        values = (
                            dtkey, dt, lines[0], validateData(lines, 1), validateData(lines, 2),
                            riskid, lines[4], validateData(lines, 5), validateData(lines, 6),
                            validateData(lines, 7), validateData(lines, 8), validateData(lines, 9),
                            validateData(lines, 10), validateData(lines, 11), validateData(lines, 12)
                        )

                        print(sql % values)
                        mycursor.execute(sql, values)

                        # print(lines[0] + ' ' + lines[4] + ' ' + dt)
                        loaded_records += 1
                        # if count > 10: return
                        if (loaded_records % 1000) == 0:
                            print("commiting another 1000 records: ", loaded_records)
                            cnx.commit()
                count += 1

            cnx.commit()
            print("Total records scanned: ", count)
            print("Total records loaded: ", loaded_records)
        except Error as e:
            print('Error at line: ', count)
            print(e)




def main(argv):
    global dtkey
    global userDefinedKey
    global configFile
    try:
        opts, args = getopt.getopt(argv, "h:c:p")
    except getopt.GetoptError:
        print('dataloader.py -h \nHelp Message')
        print('dataloader.py -p <date>')
        print('dataloader.py -cconfig.ini')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('dataloade.py -p <date>')
            sys.exit()
        elif opt in "-c":
            configFile = arg
            print(configFile)
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
