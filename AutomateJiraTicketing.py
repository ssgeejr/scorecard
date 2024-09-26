from Saturn import Saturn
from datetime import datetime, timedelta
from mysql.connector import connect, Error
import requests, time, json, base64, os
import mysql.connector, configparser
import logging, sys
from logging.handlers import RotatingFileHandler
from TethysConfig import Config




class JiraEngine:
    def setAssignTo(self, at):
        self.assignee_accountId=at

    def __init__(self, config: Config):
        self.saturn = Saturn()
        self.api_token = self.saturn.get_api_key()
        self.email = self.saturn.get_user_id()
        self.jira_url = self.saturn.get_jira_url()
        self.assignee_accountId = self.saturn.get_assign_to()
        self.config = configparser.ConfigParser()

        self.raw_today = datetime.now()
        self.today = self.raw_today.strftime("%Y-%m-%d")
        self.raw_critical_high = self.raw_today + timedelta(days=30)
        self.critical_high_date = self.raw_critical_high.strftime('%Y-%m-%d')
        self.raw_medium_criticality = self.raw_today + timedelta(days=90)
        self.medium_date = self.raw_medium_criticality.strftime('%Y-%m-%d')
        self.raw_low_date = self.raw_today + timedelta(days=180)
        self.low_date = self.raw_low_date.strftime('%Y-%m-%d')
        self.start_date_field_id = "customfield_10015"
        #config settings for global definitions
        self.dtkey = config.dtkey
        self.userDefinedKey = config.userDefinedKey
        self.configFile = config.configFile
        self.cdir = config.cdir
        self.dateTimeKey = ''
        current_date = datetime.now()
        self.year = current_date.strftime("%Y")

        log_file = 'tethys.jira-engine.log'
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
        self.logger.info('******* Initializing Tethys Jira Engine *********')

    def fetchPriority(self, risk):
        result = -99;
        jiraPriority = 'NULL'
        ddate = 'NULL'
        if risk == 0:
            result = 'Critical'
            jiraPriority = 'Highest'
            ddate = self.critical_high_date
        elif risk == 1:
            result = 'High'
            jiraPriority = 'High'
            ddate = self.critical_high_date
        elif risk == 2:
            result = 'Medium'
            jiraPriority = 'Medium'
            ddate = self.medium_date
        elif risk == 3:
            result = 'Low'
            jiraPriority = 'Low'
            ddate = self.low_date
        return result, jiraPriority, ddate

    def fetchSQLData(self, dateTimeKey):
        self.dateTimeKey = dateTimeKey
        count = 0
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
            #            cnx.autocommit = True
            #print(cnx)

            fetchTopVul = ("select count(distinct hash) as total, pluginid, name"
                           " from scorecard"
                           " where dtkey = %s and riskid = %s"
                           " group by name, pluginid"
                           " order by total"
                           " desc")
            fetchDetails = ("select solution, description"
                            " from scorecard"
                            " where dtkey = %s and riskid = %s and pluginid = %s"
                            " limit 1")
            values_list = [0, 1]
            #The next version will contain all four items
            #values_list = [0, 1, 2, 3]
            # values_list = [0]
            for rid in values_list:
                print('********************* Initiate Search for Risk ID [%s] ********************' % (rid))
                vValues = (self.dateTimeKey, rid)
                topCursor = cnx.cursor()
                topCursor.execute(fetchTopVul, vValues)
                vulResult = topCursor.fetchall()
                vCount = 0
                for vrow in vulResult:
                    vulnerability = ('Count: %s \r\nPluginID: %s\r\nName: %s\r\n' % (vrow[0], vrow[1], vrow[2]))
                    detailCursor = cnx.cursor()
                    values = (self.dateTimeKey, rid, vrow[1])
                    detailCursor.execute(fetchDetails, values)
                    detailResult = detailCursor.fetchall()
#                    print(f'PluginID {vrow[1]}')
                    for drow in detailResult:
                        details = ('Solution: %s \r\n\r\nDescription: %s' % (drow[0], drow[1]))
                        combined_string = vulnerability + '\r\n' + details
                        #                    print(combined_string)
                        priority, jiraPriority, due_date = self.fetchPriority(rid)
                        logger.info(f"Priority [{priority}] Due Date [{due_date}] Issue PluginID [{vrow[1]}] Server Count [{vrow[0]}] Title [{vrow[2]}]")
                        self.searchForIssue(rid, vrow[1], vrow[2], combined_string, priority, jiraPriority, due_date, vrow[0])
                    vCount += 1
                    print('********************* RID [%s] ROW ID [%s] ********************' % (rid, vCount))
                    if vCount == 10:
                        print('********************* End Top 10 for RID: %s ********************' % (rid))
                        break

        except Error as e:
            print('Error at line: ', count)
            print(e)
            self.logger.error('An exception occurred: %s', e, exc_info=True)

    def searchForIssue(self, rid, pluginID, title, description, priority, jiraPriority, due_date, vcount):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            'Authorization': f'Basic {base64.b64encode(f"{self.email}:{self.api_token}".encode("utf-8")).decode("utf-8")}'
        }
        # "Authorization": f"Basic {requests.auth._basic_auth_str(email, api_token)}",
        # Build the JQL query
        jql_query = f"labels = '{pluginID}' AND labels = '{priority}' AND status != 'Done'"
#        print(f'SEARCHING FOR JIRA TICKETS USING JQL QUERY {jql_query}')

        params = {
            "jql": jql_query,
            "fields": "key,summary,status,labels",  # Add any other fields you want to retrieve
        }

        response = requests.get(
            f"{self.jira_url}/rest/api/3/search",
            headers=headers,
            params=params,
        )

        if response.status_code == 200:
            issues = response.json()["issues"]

            if len(issues) == 0:
                #print(f"Failed to find existing issue. Status code: {priority}, {pluginID} and not 'Done' * Attempting to create new Jira Ticket")
                self.logger.info(f"Failed to find existing issue. Status code: {priority}, {pluginID} and not 'Done' * Attempting to create new Jira Ticket")
                self.createNewJiraTicket(rid, pluginID, title, description, priority, jiraPriority, due_date)
            else:
                #print(f"Found {len(issues)} issues with the specified labels and not in the 'Done' status category:")
                self.logger.info(f"Found {len(issues)} issues with the specified labels and not in the 'Done' status category:")
                for issue in issues:
                    #print(f"[~] {issue['key']}: {issue['fields']['summary']} | Status: {issue['fields']['status']['name']} | Labels: {issue['fields']['labels']}")
                    self.logger.info(f"[~] {issue['key']}: {issue['fields']['summary']} | Status: {issue['fields']['status']['name']} | Labels: {issue['fields']['labels']}")
                    comment = ("Existing issue found on %s by Tethys CyberSecurity Bot\r\nThe Vulnerability Count is %s" % (self.today, vcount))
                    self.addIssueComment(issue['key'], comment)
        else:
            print(f"Failed to find for issues. Status code: {response.status_code}")
            print(response.text)
            self.createNewJiraTicket(rid, pluginID, title, description, priority, jiraPriority, due_date)

    def createNewJiraTicket(self, rid, pluginID, title, description, priority, jiraPriority, due_date):
        # print(api_key)
        #self.assignee_accountId = "603d0d5a5290e700697d72fc"

        # Replace these with your own values
        project_key = 'ISS'
        issue_type = 'Task'
        summary = ('%s %s %s' % (priority, pluginID, title))
        # description = 'This task has specific priority, assignee, and start date set using the REST API.'

        labels = [pluginID, priority, self.dtkey, self.year]

        # Set up the request headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {base64.b64encode(f"{self.email}:{self.api_token}".encode("utf-8")).decode("utf-8")}'
        }

        # Set up the request payload
        payload = {
            'fields': {
                'project': {
                    'key': project_key
                },
                'issuetype': {
                    'name': issue_type
                },
                'summary': summary,
                'description': {
                    'type': 'doc',
                    'version': 1,
                    'content': [
                        {
                            'type': 'paragraph',
                            'content': [
                                {
                                    'text': description,
                                    'type': 'text'
                                }
                            ]
                        }
                    ]
                },
                'priority': {
                    'name': jiraPriority
                },
                'assignee': {
                    'accountId': self.assignee_accountId
                },
                "labels": labels,
                self.start_date_field_id: self.today,
                "duedate": due_date
            }
        }

        # Send the request
        response = requests.post(f'{self.jira_url}/rest/api/3/issue', headers=headers, data=json.dumps(payload))

        # Check the response
        if response.status_code == 201:
            #print(f"Jira Ticket created successfully: {response.json()['key']}")
#            print(f"{response.json()['key']}\t{priority}\t{due_date}\t{pluginID}\t{title}")
            #print(f"[+] {response.json()['key']}: {title} | Status: {jiraPriority} | Labels: {pluginID}, {priority}")
#            logging.info(f"Created new Jira Ticket {response.json()['key']} for PluginID: {pluginID}")
            self.logger.info(f"[+] {response.json()['key']}: {title} | Status: {jiraPriority} | Labels: [{pluginID}, {priority}]")
        else:
            self.logger.error(f"Error creating new ticket!! PluginID: {pluginID} Response Code: {response.status_code} - {response.text}")
            #logging.error(f"Failed to create new Jira Ticket for PluginID: {pluginID}")

    def addIssueComment(self, issue_key, comment):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            'Authorization': f'Basic {base64.b64encode(f"{self.email}:{self.api_token}".encode("utf-8")).decode("utf-8")}'
        }

        #    print('ISSUE %s' % issue_key)
        #    print('COMMENT %s' % comment)
        data = {
            "body": {
                "version": 1,
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment
                            }
                        ]
                    }
                ]
            }
        }

        response = requests.post(
            f"{self.jira_url}/rest/api/3/issue/{issue_key}/comment",
            headers=headers,
            data=json.dumps(data),
        )
        if response.status_code == 201:
            #print(f"Comment added successfully to issue {issue_key}.")
            self.logger.info(f"Successfully added comments to issue {issue_key}.")
        else:
            #print(f"Failed to add comment to issue. Status code: {response.status_code}")
            self.logger.error(f"Failed to update issue {issue_key} for reason {response.text}")
            #print(response.text)
