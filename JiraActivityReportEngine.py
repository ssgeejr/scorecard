from Saturn import Saturn
import requests,sys, base64, getopt, logging, os
from logging.handlers import RotatingFileHandler
from requests.auth import HTTPBasicAuth
from datetime import datetime,timedelta
import pandas as pd

saturn = Saturn()
api_token = saturn.get_api_key()
email = saturn.get_user_id()
jira_url = saturn.get_jira_url()
today = datetime.now()
yesterday = today - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%m/%d/%y')

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

        self.run_daily_report = True
        self.run_weekly_report = today.weekday() == 0
        self.run_monthly_report = today.day == 1
        self.send_report_email = True
        self.email_list = []

    def determineReportParameters(self):
        dailyjql = {
            "validation": {
                "title": "Validated Yesterday",
                "sql": "status = Validation AND statuscategorychangeddate >= startOfDay(-1) and statusCategoryChangedDate <= endOfDay(-1) order by priority desc"
            },
            "done": {
                "title": "Done Yesterday",
                "sql": "status = Done AND statuscategorychangeddate >= startOfDay(-1) and statusCategoryChangedDate <= endOfDay(-1) order by priority desc"
            },
            "open": {
                "title": "Created Yesterday",
                "sql": "createdDate >= startOfDay(-1) and createdDate <= endOfDay(-1) order by priority desc"
            }
        }
        weeklyjql = {
            "validation": {
                "title": "Validated Last Week",
                "sql": "status = Validation AND statuscategorychangeddate >= startOfWeek(-1) and statusCategoryChangedDate <= endOfWeek(-1) order by priority desc"
            },
            "done": {
                "title": "Done Last Week",
                "sql": "status = Done AND statuscategorychangeddate >= startOfWeek(-1) and statusCategoryChangedDate <= endOfWeek(-1) order by priority desc"
            },
            "open": {
                "title": "Created Last Week",
                "sql": "createdDate >= startOfWeek(-1) and createdDate <= endOfWeek(-1) order by priority desc"
            }
        }
        monthlyjql = {
            "validation": {
                "title": "Validated Last Month",
                "sql": "status = Validation AND statuscategorychangeddate >= startOfMonth(-1) and statusCategoryChangedDate <= endOfMonth(-1) order by priority desc"
            },
            "done": {
                "title": "Done Last Month",
                "sql": "status = Done AND statuscategorychangeddate >= startOfMonth(-1) and statusCategoryChangedDate <= endOfMonth(-1) order by priority desc"
            },
            "open": {
                "title": "Created Last Month",
                "sql": "createdDate >= startOfMonth(-1) and createdDate <= endOfMonth(-1) order by priority desc"
            }
        }

        try:
            #print('determining date to run')

            if self.run_daily_report:
                self.logger.info(f'Run Daily Report (RUN_DAILY_REPORT {self.run_daily_report})')
                self.runReport(dailyjql)

            if self.run_weekly_report:
                self.logger.info(f'Run Weekly Report (RUN_WEEKLY_REPORT {self.run_weekly_report})')
                self.runReport(weeklyjql)

            if self.run_monthly_report:
                self.logger.info(f'Run Monthly Report (RUN_MONTHLY_REPORT {self.run_monthly_report})')
                self.runReport(monthlyjql)

        except Exception as e:
            self.logger.error("An error occurred in determining runtime ...")
            self.logger.error(e)

    def runReport(self, datadict):
        headers = ["Issue", "Level", "Created", "Description"]
        result_header = f"{headers[0]:<12} {headers[1]:<10} {headers[2]:<12} {headers[3]:<256}\n"
        #result = result_header + "-" * 50 + "\n"
        result = ''

        try:
            for query_name, query_data in datadict.items():
                result += "-" * 50 + "\n"
                result += f"{query_data['title']:<30}\n"

                url = f"{jira_url}/rest/api/3/search"
                params = {
                    "jql": query_data['sql'],
                    "maxResults": 250,  # Optional: Change if you want to limit the results
                }
                auth = HTTPBasicAuth(email, api_token)
                headers = {
                    "Accept": "application/json"
                }
                response = requests.get(url, headers=headers, auth=auth, params=params)
                #print(f"Reporting criteria: {query_data['title']}")
                if response.status_code == 200:
                    #print('RESPONSE_CODE_200')
                    data = response.json()
                    #print(f">>>>>>>>>>>>>>>>>> {data['total']}")
                    if data['total'] == 0:

                        result += 'No issues found for given period ... \n'
                    else:
                        result += result_header + "-" * 50 + "\n"
                        for issue in data['issues']:
                            date_object = datetime.strptime(f"{issue['fields']['created']}", '%Y-%m-%dT%H:%M:%S.%f%z')
                            result += f"{issue['key']:<12} {issue['fields']['priority']['name']:<10} {date_object.strftime('%m/%d/%y'):<12} {issue['fields']['summary']:<256}\n"
                        #result += "-" * 50 + "\n"
                else:
                    self.logger.error(f"Error fetching issue: {response.status_code} - {response.text}")
            #print('-----------------------------------------------------------------------------')
            result += "-" * 50 + "\n"
            print(result)


        except Exception as e:
            self.logger.error("An error occurred in data processing ...")
            self.logger.error(e)

    def main(self, *argv):
        try:
            opts, args = getopt.getopt(argv, "d:hewmabcx", ["emails="])
        except getopt.GetoptError as e:
            print('>>>> ERROR: %s' % str(e))
            sys.exit(2)

        only_key = 0
        key_count = 0
        for opt, arg in opts:
            if opt == '-h':
                print('---RUNTIME PARAMETERS---')
                print('python JiraActivityReportEngine.py -h #Help Message')
                print('python JiraActivityReportEngine.py -d date  #set the runtime date')
                print('python JiraActivityReportEngine.py -e #run the daily report')
                print('python JiraActivityReportEngine.py -w #run the weekly report')
                print('python JiraActivityReportEngine.py -m #run the monthly report')
                print('python JiraActivityReportEngine.py -a #run ONLY the daily report')
                print('python JiraActivityReportEngine.py -b #run ONLY the monthly report')
                print('python JiraActivityReportEngine.py -c #run ONLY the monthly report')
                print('python JiraActivityReportEngine.py -x #do not send the email')
                print('python JiraActivityReportEngine.py --emails "one@mail.com, two@mail.com, three@mail.com"')
                print('------------------------')
                sys.exit()
            elif opt in "-x":
                self.sendEmail = False
                print('Report will [NOT] send email')
            elif opt in "-e":
                self.run_daily_report = True
                print('forcing daily report')
            elif opt in "-w":
                self.run_weekly_report = True
                print('forcing weekly report')
            elif opt in "-m":
                print('forcing monthly report')
            elif opt in "-a":
                key_count += 1
                only_key = 1
            elif opt in "-b":
                key_count += 1
                only_key = 2
            elif opt in "-c":
                key_count += 1
                only_key = 3
            elif opt == '--emails':
                # Split the comma-separated email addresses and strip any whitespace
                self.email_list = [email.strip() for email in arg.split(',')]

        if key_count > 1:
            self.logger.info("Exactly one of the argument -a, -b, or -c must be provided.")
            exit(-1)

        if only_key == 1:
            self.logger.info('ONLY running DAILY report')
            self.run_daily_report = True
            self.run_weekly_report = False
            self.run_monthly_report = False
        elif only_key == 2:
            self.logger.info('ONLY running WEEKLY report')
            self.run_daily_report = False
            self.run_weekly_report = True
            self.run_monthly_report = False
        elif only_key == 3:
            self.logger.info('ONLY running MONTHLY report')
            self.run_daily_report = False
            self.run_weekly_report = False
            self.run_monthly_report = True

        self.logger.info(f'DAILY:  {self.run_daily_report}')
        self.logger.info(f'WEEKLY:  {self.run_weekly_report}')
        self.logger.info(f'MONTHLY:  {self.run_monthly_report}')

        if self.email_list:
            self.logger.info("User provided Email addresses:", self.email_list)
        else:
            self.logger.info("Using default mailing list")

        self.determineReportParameters()

if __name__ == "__main__":
    tethys = ReportEngine()
    tethys.main(*sys.argv[1:])