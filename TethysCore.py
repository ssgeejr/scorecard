import csv, time, sys, getopt, glob, os, datetime, logging
import mysql.connector, configparser, hashlib
from mysql.connector import connect, Error
from pathlib import Path
from TethysConfig import Config
from logging.handlers import RotatingFileHandler

log_file = 'tethys.TethysCore.log'
max_file_size = 5 * 1024 * 1024  # 5 MB
backup_count = 5
if os.path.exists(log_file):
    os.remove(log_file)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(filename=log_file, maxBytes=max_file_size, backupCount=backup_count)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


class DataEngine:


    def __init__(self, config: Config):
        self.config = configparser.ConfigParser()
        #Shared Configuration Settings
        self.dtkey = config.dtkey
        self.userDefinedKey = config.userDefinedKey
        self.configFile = config.configFile
        self.cdir = config.cdir
        self.working_dir = config.working_dir

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
        logger.info(f'Switching to working directory: {self.working_dir}')
        os.chdir(self.working_dir)
        loadfile_list = []
        logger.info(f'Using User Defined Key: {self.userDefinedKey}')
        if self.userDefinedKey:
            logger.info('User Defined Key: ', self.dtkey)
            old_file = os.path.join(self.working_dir, self.dtkey + '.csv')
            logger.info(f'USER_DEFINED_LOAD_FILE: {old_file} WITH DTKEY {self.dtkey}')
            self.loadScoredataData(old_file)
            loadfile_list.append(self.dtkey)
            new_file = os.path.join(self.working_dir, old_file + '.old')
            os.rename(old_file, new_file)
            return loadfile_list

        logger.info('***** ATTEMPTING TO LOAD GLOB.GLOB.DATA *****')
        for file in glob.glob("*.csv"):
            try:
                logger.info('***** LOADING DATA FILE ', file, ' *****')
                old_file = os.path.join(self.working_dir, file)
                new_file = os.path.join(self.working_dir, file + '.old')
                self.dtkey = Path(old_file).stem
                logger.info(f'Using data file: {old_file} and dtkey {self.dtkey}')
                self.loadScoredataData(old_file)
                loadfile_list.append(self.dtkey)
                logger.info(f'Successfully loaded {old_file} attempting to rename to {new_file}')
                logger.info('***** FILE LOAD COMPLETED *****')
                os.rename(old_file, new_file)
            except Exception as e:
                logger.error("An error occurred in the data loading process ...")
                logger.error(e)


        return loadfile_list

    def loadScoredataData(self, datafile):
        dt = time.strftime('%Y%m%d')
        logger.info(f'Attempting to open data in readonly mode {datafile}')
        with open(datafile, mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            count = 0
            logger.info('USING DTKEY: ', self.dtkey)
            try:
                logger.info('**********************************************************')
                logger.info('Configuration File: ', self.configFile)
                config_source = os.path.join(self.cdir, self.configFile)
                logger.info('Configuration Source: ', config_source)
                self.config.read(config_source)
                logger.info('**********************************************************')

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

                logger.info(sql)

                logger.info('**********************************************************')

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
                                logger.info("   committing 1000 records: ", loaded_records)
                                cnx.commit()
                    count += 1

                cnx.commit()
                logger.info("Total records scanned: ", count)
                logger.info("Total records committed: ", loaded_records)
            except Error as e:
                logger.error('TethysCore::Error at line: ', count)
                logger.error('===========================================')
                logger.error(values)
                logger.error('===========================================')
                logger.error(e)
                raise ValueError("Database Failure: attempting to stop all processing")

    def fetchIndex(self, line, index):
        try:
            return line[index]
        except IndexError:
            return ''
