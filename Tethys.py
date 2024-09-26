#!/usr/bin/env python3

import configparser, time, os, sys, getopt
from AutomateJiraTicketing import JiraEngine
from TethysCore import DataEngine
from TethysConfig import Config


class Tethys:

    def __init__(self):
        self.config = Config()
        self.runJira = True

    def runTethys(self):
        print(f'Config File: {self.config.configFile}')
        print(f'User ID {self.config.user_id}')
        print(f'DTKEY {self.config.dtkey}')
        print(f'Working Directory {self.config.working_dir}')

        data_engine = DataEngine(self.config)
        files = data_engine.fetchFileStack()

        #       files = ['0423A']

        #print('==== THIS IS WHERE YOU CAN SKIP JIRA LOADING IF YOU HAVE AN ISSUE ====')
        if self.runJira:
            engine = JiraEngine(self.config)
            for dates in files:
                print(f'ATTEMPTING TO LOAD TOP 10 JIRA TICKET DATA FOR {dates}')
                engine.fetchSQLData(dates)
        else:
            print('SKIPPING JIRA TICKETING')

    def main(self, *argv):
        try:
            opts, args = getopt.getopt(argv, "h:c:p:w:a:jx")
        except getopt.GetoptError as e:
            print('>>>> ERROR: %s' % str(e))
            sys.exit(2)
        jiraonly = False
        for opt, arg in opts:
            if opt == '-h':
                print('dataloader.py -h \nHelp Message')
                print('dataloader.py -x \nSkip the Jira Section and only do the data load')
                print('dataloader.py -p <date>')
                print('dataloader.py -c{config.file}')
                print('dataloader.py -p date')
                print('dataloader.py -w{working.dir}')
                sys.exit()
            elif opt in "-x":
                self.runJira = False
            elif opt in "-c":
                self.config.configFile = arg
            elif opt in "-a":
                self.config.user_id = arg
            elif opt in ("-p", "--pkey"):
                self.config.userDefinedKey = True
                self.config.dtkey = arg
            elif opt in "-w":
                self.config.working_dir = arg
            elif opt in "-j":
                jiraonly = True

        if jiraonly:
            engine = JiraEngine(self.config)
            engine.fetchSQLData(self.config.dtkey)
        else:
            self.runTethys()


if __name__ == "__main__":
    tethys = Tethys()
    tethys.main(*sys.argv[1:])
