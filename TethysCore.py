import csv, time, sys, getopt, glob, os, datetime, logging
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path
from TethysConfig import Config
from logging.handlers import RotatingFileHandler

class DataEngine:


    def __init__(self, config: Config):
        self.config = configparser.ConfigParser()
        #Shared Configuration Settings
        self.dtkey = config.dtkey
        self.userDefinedKey = config.userDefinedKey
        self.configFile = config.configFile
        self.cdir = config.cdir
        self.working_dir = config.working_dir
        log_file = 'tethys.TethysCore.log'
        max_file_size = 5 * 1024 * 1024  # 5 MB
        backup_count = 5
        if os.path.exists(log_file):
            os.remove(log_file)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        file_handler = RotatingFileHandler(filename=log_file, maxBytes=max_file_size, backupCount=backup_count)
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(log_format)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

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
        self.logger.info(f'Switching to working directory: {self.working_dir}')
        os.chdir(self.working_dir)
        loadfile_list = []
        self.logger.info(f'Using User Defined Key: {self.userDefinedKey}')
        if self.userDefinedKey:
            self.logger.info('User Defined Key: %s', self.dtkey)
            old_file = os.path.join(self.working_dir, self.dtkey + '.csv')
            self.logger.info(f'USER_DEFINED_LOAD_FILE: {old_file} WITH DTKEY {self.dtkey}')
            self.loadScoredataData(old_file)
            loadfile_list.append(self.dtkey)
            new_file = os.path.join(self.working_dir, old_file + '.old')
            os.rename(old_file, new_file)
            return loadfile_list

        self.logger.info('***** ATTEMPTING TO LOAD GLOB.GLOB.DATA *****')
        for file in glob.glob("*.csv"):
            try:
                self.logger.info(f'***** LOADING DATA FILE {file} *****')
                old_file = os.path.join(self.working_dir, file)
                new_file = os.path.join(self.working_dir, file + '.old')
                self.dtkey = Path(old_file).stem
                self.logger.info(f'Using data file: {old_file} and dtkey {self.dtkey}')
                self.loadScoredataData(old_file)
                loadfile_list.append(self.dtkey)
                self.logger.info(f'Successfully loaded {old_file} attempting to rename to {new_file}')
                self.logger.info('***** FILE LOAD COMPLETED *****')
                os.rename(old_file, new_file)
            except Exception as e:
                self.logger.error("An error occurred in the data loading process ...")
                self.logger.error(e)


        return loadfile_list

    def loadScoredataData(self, datafile):
        dt = time.strftime('%Y%m%d')
        self.logger.info(f'Attempting to open data in readonly mode {datafile}')
        with open(datafile, mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            count = 0
            self.logger.info(f'USING DTKEY: {self.dtkey}')
            try:
                self.logger.info('**********************************************************')
                self.logger.info('Configuration File: %s', self.configFile)
                config_source = os.path.join(self.cdir, self.configFile)
                self.logger.info('Configuration Source: %s', config_source)
                self.config.read(config_source)
                self.logger.info('**********************************************************')

                cnx = mysql.connector.connect(user=self.config['tethys']['user'],
                                              password=self.config['tethys']['passwd'],
                                              host=self.config['tethys']['host'],
                                              database=self.config['tethys']['db'])

#                logger.info(cnx)
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

                self.logger.info(sql)

                self.logger.info('**********************************************************')

                loaded_records = 0
                for lines in csvFile:
                    if count > 0:
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
                                self.logger.info(f"   committing 1000 records: {loaded_records}")
                                cnx.commit()
                                break
                    count += 1

                cnx.commit()
                self.logger.info("Total records scanned: " + str(count))
                self.logger.info("Total records committed: " + str(loaded_records))
            except Error as e:
                self.logger.error('TethysCore::Error at line: ' + str(count))
                self.logger.error('===========================================')
                self.logger.error(values)
                self.logger.error('===========================================')
                self.logger.error(e)
                raise ValueError("Database Failure: attempting to stop all processing")

    def fetchIndex(self, line, index):
        try:
            return line[index]
        except IndexError:
            return ''
