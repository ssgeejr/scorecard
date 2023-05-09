#!/usr/bin/env python3

import configparser, time, os, sys, getopt
from AutomateJiraTicketing import JiraEngine
from TethysCore import DataEngine
from TethysConfig import Config


class Tethys:

    def __init__(self):
        self.config = Config()

    def runTethys(self):
        print(self.config.configFile)
        print(self.config.user_id)
        print(self.config.dtkey)
        print(self.config.working_dir)

        data_engine = DataEngine(self.config)
        files = data_engine.fetchFileStack()
        #       files = ['0423A']
        engine = JiraEngine(self.config)
        for dates in files:
            engine.fetchSQLData(dates)

    def main(self, *argv):
        try:
            opts, args = getopt.getopt(argv, "h:c:p:w:a:")
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
                self.config.configFile = arg
            elif opt in "-a":
                self.config.user_id = arg

            elif opt in ("-p", "--pkey"):
                self.config.userDefinedKey = True
                self.config.dtkey = arg
            elif opt in "-w":
                self.config.working_dir = arg

        self.runTethys()


if __name__ == "__main__":
    tethys = Tethys()
    tethys.main(*sys.argv[1:])
