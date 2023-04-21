from Saturn import Saturn
from datetime import datetime, timedelta
import requests
import json
import base64


'''
Days to mitigate (15) and close (30) critical risks
https://www.cisa.gov/sites/default/files/publications/Reducing_the_Significant_Risk_of_Known_Exploited_Vulnerabilities_211103.pdf

Mandate for Facilities
https://www.cisa.gov/news-events/directives/binding-operational-directive-19-02
Review and Remediate Critical and High Vulnerabilities

Review Cyber Hygiene reports issued by CISA and remediate the critical and high vulnerabilities detected on the agency’s Internet-accessible systems as follows:

Critical vulnerabilities must be remediated within 15 calendar days of initial detection.
High vulnerabilities must be remediated within 30 calendar day of initial detection.

HIPAA data is protected by federal law
https://www.hhs.gov/hipaa/for-individuals/guidance-materials-for-consumers/index.html
'''

saturn = Saturn()
api_token = saturn.get_api_key()
email = saturn.get_user_id()
jira_url = saturn.get_jira_url()
assignee_accountId = saturn.get_assign_to()
raw_today = datetime.now()
today = raw_today.strftime("%Y-%m-%d")
raw_fifteen_days_later = raw_today + timedelta(days=15)
fifteen_days_later = raw_fifteen_days_later.strftime('%Y-%m-%d')
raw_thirty_days_later = raw_today + timedelta(days=30)
thirty_days_later = raw_thirty_days_later.strftime('%Y-%m-%d')
start_date_field_id = "customfield_10015"

def createTop10JiraTickets():
    #print(api_key)

    fetchSQLData()



    # Replace these with your own values
    project_key = 'ISS'
    issue_type = 'Task'
    summary = 'A new task with specific priority, assignee, and start date'
    description = 'This task has specific priority, assignee, and start date set using the REST API.'
    priority_name = 'Highest'
    start_date = '2023-06-01'

    # Set up the request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")}'
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
                'name': priority_name
            },
            'assignee': {
                'accountId': assignee_accountId
            },
            start_date_field_id: today,
            "duedate": fifteen_days_later

        }
    }

    # Send the request
    response = requests.post(f'{jira_url}/rest/api/3/issue', headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code == 201:
        print(f"Task created successfully: {response.json()['key']}")
    else:
        print(f"Error creating task: {response.status_code} - {response.text}")


def fetchSQLData()




'''
set @ dtk = '0423A';
set @ rid = 0;
set @ pid = 22024;

select
solution,
description
from scorecard
where
dtkey =@dtk
and riskid = @rid
and pluginid = @pid
limit 1
'''



def main():
    createTop10JiraTickets()


if __name__ == "__main__":
    main()