from Saturn import Saturn
from datetime import datetime, timedelta
from mysql.connector import connect, Error
import requests, time, json, base64, os
import mysql.connector, configparser

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

dtkey = time.strftime('%m%y')
userDefinedKey = False
configFile = 'tethys.ini'
config = configparser.ConfigParser()
cdir = os.path.dirname(os.path.abspath(__file__))

dateTimeKey = "0423A"

def fetchPriority(risk):
    result = -99;
    jiraPriority = 'NULL'
    ddate = 'NULL'
    if risk == 0:
        result = 'Critical'
        jiraPriority = 'Highest'
        ddate = fifteen_days_later
    elif risk == 1:
        result = 'High'
        jiraPriority = 'High'
        ddate = thirty_days_later
    return result, jiraPriority, ddate

def createTop10JiraTickets(rid, pluginID, title, description, priority, jiraPriority, due_date):
    #print(api_key)
    assignee_accountId = "603d0d5a5290e700697d72fc"

    # Replace these with your own values
    project_key = 'ISS'
    issue_type = 'Task'
    summary = ('%s %s %s' % (priority, pluginID, title))
    #description = 'This task has specific priority, assignee, and start date set using the REST API.'
    labels = [pluginID, priority]

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
                'name': jiraPriority
            },
            'assignee': {
                'accountId': assignee_accountId
            },
            "labels": labels,
            start_date_field_id: today,
            "duedate": due_date
        }
    }

    # Send the request
    response = requests.post(f'{jira_url}/rest/api/3/issue', headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code == 201:
        print(f"Task created successfully: {response.json()['key']}")
    else:
        print(f"Error creating task: {response.status_code} - {response.text}")


def fetchSQLData():
    count = 0
    try:
        print('**********************************************************')
        print('Configuration File: ', configFile)
        config_source = os.path.join(cdir, configFile)
        print('Configuration Source: ', config_source)
        config.read(config_source)
        print('**********************************************************')

        cnx = mysql.connector.connect(user=config['tethys']['user'],
                                      password=config['tethys']['passwd'],
                                      host=config['tethys']['host'],
                                      database=config['tethys']['db'])
        #            cnx.autocommit = True
        print(cnx)

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
        #values_list = [0, 1]
        values_list = [0]
        for rid in values_list:
            print('********************* start section %s ********************' % (rid))
            vValues = (dateTimeKey, rid)
            topCursor = cnx.cursor()
            topCursor.execute(fetchTopVul, vValues)
            vulResult = topCursor.fetchall()
            vCount = 0
            for vrow in vulResult:
                vulnerability = ('Count: %s \r\nPluginID: %s\r\nName: %s\r\n' % (vrow[0], vrow[1], vrow[2]))
                detailCursor = cnx.cursor()
                values = (dateTimeKey, rid, vrow[1])
                detailCursor.execute(fetchDetails, values)
                detailResult = detailCursor.fetchall()
                for drow in detailResult:
                    details = ('Solution: %s \r\n\r\nDescription: %s' % (drow[0], drow[1]))
                    combined_string = vulnerability + '\r\n' + details
#                    print(combined_string)
                    priority, jiraPriority, due_date= fetchPriority(rid)
                    searchForIssue(rid, vrow[1], vrow[2], combined_string, priority, jiraPriority, due_date, vrow[0])
                vCount += 1
                if vCount == 1:
                    print('********************* end section %s ********************' % (rid))
                    break

    except Error as e:
        print('Error at line: ', count)
        print(e)

def searchForIssue(rid, pluginID, title, description, priority, jiraPriority, due_date, vcount):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        'Authorization': f'Basic {base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")}'
    }
    #"Authorization": f"Basic {requests.auth._basic_auth_str(email, api_token)}",
    # Build the JQL query
    labels = [pluginID, priority]
    labels_str = ",".join([f'"{label}"' for label in labels])
    jql_query = f'labels in ({labels_str}) AND statusCategory != Done'

    params = {
        "jql": jql_query,
        "fields": "key,summary,status,labels",  # Add any other fields you want to retrieve
    }

    response = requests.get(
        f"{jira_url}/rest/api/3/search",
        headers=headers,
        params=params,
    )

    if response.status_code == 200:
        issues = response.json()["issues"]
        print(f"Found {len(issues)} issues with the specified labels and not in the 'Done' status category:")
        for issue in issues:
            print(f"{issue['key']}: {issue['fields']['summary']} | Status: {issue['fields']['status']['name']} | Labels: {issue['fields']['labels']}")
            comment = ("Existing issue found on %s by Tethys CyberSecurity Bot\r\nThe new Vulnerability Count is %s" % (today, vcount))
            addIssueComment(issue['key'], comment)
    else:
        print(f"Failed to search for issues. Status code: {response.status_code}")
        print(response.text)
        createTop10JiraTickets(rid, pluginID, title, description, priority, jiraPriority, due_date)

def addIssueComment(issue_key, comment):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        'Authorization': f'Basic {base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")}'
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
        f"{jira_url}/rest/api/3/issue/{issue_key}/comment",
        headers=headers,
        data=json.dumps(data),
    )
    if response.status_code == 201:
        print(f"Comment added successfully to issue {issue_key}.")
    else:
        print(f"Failed to add comment to issue. Status code: {response.status_code}")
        print(response.text)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX CONSTRUCTOR CODE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def main():
    fetchSQLData()


if __name__ == "__main__":
    main()