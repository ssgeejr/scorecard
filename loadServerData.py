#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path

configFile = 'db.ini'
working_dir = "/opt/apps/server.data"
config = configparser.ConfigParser()
cdir = os.path.dirname(os.path.abspath(__file__))


def fetchFileStack():
    global dtkey
    print('hi')
    os.chdir(working_dir)
    for file in glob.glob("*.csv"):
        print('***** LOADING DATA FILE ', file, ' *****')
        old_file = os.path.join(working_dir, file)
        new_file = os.path.join(working_dir, file + '.old')
        print('Using data file: ', os.path.basename(old_file))
        dtkey = int(Path(old_file).stem)
        print('dtkey: ', dtkey)
        loadServerData(old_file)

        print('New File: ', new_file)
        print('***** FILE LOAD COMPLETED - RENAMING TO *.old *****')
#        os.rename(old_file, new_file)



def loadServerData(serverFile):
    global dtkey
    count = 0
    with open(serverFile, mode='r') as file:
        csvFile = csv.reader(file)
        try:
            print('Server File: ' + serverFile)
#            print('**********************************************************')
#            print('Configuration File: ', configFile)
            config_source = os.path.join(cdir, configFile)
 #           print('Configuration Source: ', config_source)
            config.read(config_source)
#            print('**********************************************************')
            cnx = mysql.connector.connect(user=config['tethys']['user'],
                                      password=config['tethys']['passwd'],
                                      host=config['tethys']['host'],
                                      database=config['tethys']['db'])
#            print(cnx)
            print('**********************************************************')
            mycursor = cnx.cursor()

            sql = ("insert into servers"
                   + " (did,"
                   + " ip,"
                   + " name,"
                   + " os)"
                   + " values(%s,%s,%s,%s)")
            print(sql)
            loaded_records = 0
            for row in csvFile:
                if count > 0:
                    ip = row[0]
                    name = row[1]
                    sos = row[2].replace('\r\n', ', ').replace('\n', ', ').replace('\r', ', ')
                    if not name:
                        name = ip
                    if not sos:
                        sos = 'UNKNOWN'
#                    print("IP, Name, OS: %s, %s, %s" % (ip, name, sos))
                    values = (dtkey, ip, name, sos)
                    mycursor.execute(sql, values)
                    loaded_records += 1
                    if (loaded_records % 100) == 0:
                        print("committing another 100 records: ", loaded_records)
                        cnx.commit()
                count = count+1

            cnx.commit()
            print("Total records loaded: ", loaded_records)
        except Error as e:
            print('Error at line: ', count)
            print(e)


def main(argv):
    global dtkey
    global userDefinedKey
    global configFile
    global working_dir
    try:
        opts, args = getopt.getopt(argv, "h:c:w:")
    except getopt.GetoptError as e:
        print('>>>> ERROR: %s' % str(e))
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('dataloader.py -h \nHelp Message')
            print('dataloader.py -c{config.file}')
            print('dataloader.py -w{working.dir}')
            sys.exit()
        elif opt in "-c":
            configFile = arg
            print(configFile)
        elif opt in "-w":
            working_dir = arg
            print(working_dir)

    fetchFileStack()


if __name__ == "__main__":
    main(sys.argv[1:])
