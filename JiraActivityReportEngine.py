from Saturn import Saturn
import requests,sys, base64, getopt, logging, os
from logging.handlers import RotatingFileHandler

saturn = Saturn()
api_token = saturn.get_api_key()
email = saturn.get_user_id()
jira_url = saturn.get_jira_url()

class ReportEngine:
    def __init__(self):
        log_file = 'tethys.JiraActivityEngine.log'
        if os.path.exists(log_file):
            os.remove(log_file)
        max_file_size = 5 * 1024 * 1024  # 5 MB
        backup_count = 5
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
        self.logger.info('******* Initializing JiraActivityReportEngine!!! *********')


    def loadQueryData(self):
        #/ rest / api / 3 / search?jql = filter = {filter_id}
        filter_id = '10009'
        try:
            # Set up the request headers
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Basic {base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")}'
            }
            url = f'{jira_url}/rest/api/3/search?jql=filter={filter_id}'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print('RESPONSE_CODE_200')
                obj = response.json()
                issues = obj['issues']
                for issue in issues:
                    self.logger.info(f"Issue key: {issue['key']}")
            else:
                print(f"Error fetching issue: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error("An error occurred in data processing ...")
            self.logger.error(e)

    def loadReportData(self):
        issue_key = 'ISS-227'

        # Set up the request headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")}'
        }

        # Send the request
        #response = requests.get(f'{jira_url}/rest/api/2/issue/{issue_key}', headers=headers)

        url = f'{jira_url}/rest/api/3/issue/{issue_key}'
        print(url)
        response = requests.get(url, headers=headers)

        # Check the response
        if response.status_code == 200:
            issue_data = response.json()
            print(f"Issue key: {issue_data['key']}")
            print(f"Summary: {issue_data['fields']['summary']}")
            print(f"Status: {issue_data['fields']['status']['name']}")
            print(
                f"Assignee: {issue_data['fields']['assignee']['displayName'] if issue_data['fields']['assignee'] else 'Unassigned'}")
        else:
            print(f"Error fetching issue: {response.status_code} - {response.text}")

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

        self.loadQueryData()

if __name__ == "__main__":
    tethys = ReportEngine()
    tethys.main(*sys.argv[1:])