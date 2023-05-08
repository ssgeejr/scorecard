#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os, datetime
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path


class DataEngine:
    def __init__(self):
        self.dtkey = time.strftime('%m%y')
        self.userDefinedKey = False
        self.configFile = 'db.ini'
        self.working_dir = "/opt/apps/sc.data"
        self.config = configparser.ConfigParser()
        self.cdir = os.path.dirname(os.path.abspath(__file__))

    def fetchRiskID(self, risk):
        result = -99
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

    def validateData(self, a_list, key):
        try:
            return a_list[key]
        except IndexError:
            return ''

    def fetchFileStack(self):
        os.chdir(self.working_dir)
        loadfile_list = []
        for file in glob.glob("*.csv"):
            print('***** LOADING DATA FILE ', file, ' *****')
            old_file = os.path.join(self.working_dir, file)
            new_file = os.path.join(self.working_dir, file + '.old')
            print('Using data file: ', os.path.basename(old_file))

            if self.userDefinedKey:
                print('User Defined Key: ', self.dtkey)
            else:
                self.dtkey = Path(old_file).stem
            loadfile_list.append(self.dtkey)
            return loadfile_list

            self.loadScoredataData(old_file)

            print('New File: ', new_file)
            print('***** FILE LOAD COMPLETED - RENAMING TO *.old *****')
            os.rename(old_file, new_file)


    def loadScoredataData(self, datafile):
        dt = time.strftime('%Y%m%d')

        with open(datafile, mode='r') as file:

            # reading the CSV file
            csvFile = csv.reader(file)
            count = 0
            print('USING DTKEY: ', self.dtkey)

            try:
                print('**********************************************************')
                print('Configuration File: ', self.configFile)
                config_source = os.path.join(self.cdir, self.configFile)
                print('Configuration Source: ', config_source)
                self.config.read(config_source)
                print('**********************************************************')

                cnx = mysql.connector.connect(user=self.config['tethys']['user'],
                                              password=self.config['tethys']['passwd'],
                                              host=self.config['tethys']['host'],
                                              database=self.config['tethys']['db'])

                print(cnx)
                mycursor = cnx.cursor()

                sql = ("insert into scorecard"
                       + " (dtkey,"
                       + " rptdate,"
                       + " pluginid,"
                       + " cve,"
                       + " cvss,"
                       + " riskid,"
                       + " host,"
                       + " protocol,"
                       + " port,"
                       + " name,"
                       + " synopsis,"
                       + " description,"
                       + " solution,"
                       + " see_also,"
                       + " plugin_output,"
                       + " hash)"
                       + " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

                print(sql)

                loaded_records = 0

                for lines in csvFile:
                    if count > 0:
                        datakey = lines[0] + lines[4]
                        riskid = self.fetchRiskID(lines[3])
                        if riskid > -1:
                            values = (
                                self.dtkey, dt, lines[0], self.validateData(lines, 1), self.validateData(lines, 2),
                                riskid, lines[4], self.validateData(lines, 5), self.validateData(lines, 6),
                                self.validateData(lines, 7), self.validateData(lines, 8), self.validateData(lines, 9),
                                self.validateData(lines, 10), self.validateData(lines, 11), self.validateData(lines, 12),
                                hashlib.md5((lines[0] + "" + lines[4]).encode()).hexdigest()
                            )

                        mycursor.execute(sql, values)
                        loaded_records += 1
                        if (loaded_records % 1000) == 0:
                            print("committing another 1000 records: ", loaded_records)
                            cnx.commit()
                    count += 1

                cnx.commit()
                print("Total records scanned: ", count)
                print("Total records loaded: ", loaded_records)
            except Error as e:
                print('Error at line: ', count)
                print(e)

    def fetchIndex(self, line, index):
        try:
            return line[index]
        except IndexError:
            return ''

    def main(self, *argv):
        try:
            opts, args = getopt.getopt(argv, "h:c:p:w:")
        except getopt.GetoptError as e:
            print('>>>> ERROR: %s' % str(e))
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('dataloader.py -h \nHelp Message')
                print('dataloader.py -p <date>')
                print('dataloader.py -c{config.file}')
                print('dataloader.py -p date')
                print('dataloader.py -w{working.dir}')
                sys.exit()
            elif opt in "-c":
                self.configFile = arg
                print(self.configFile)
            elif opt in ("-p", "--pkey"):
                self.userDefinedKey = True
                self.dtkey = arg
                print(self.dtkey)
            elif opt in "-w":
                self.working_dir = arg
                print(self.working_dir)

#        self.fetchFileStack()


if __name__ == "__main__":
    my_instance = DataEngine()
    my_instance.main(*sys.argv[1:])

