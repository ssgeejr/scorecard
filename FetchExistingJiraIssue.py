from Saturn import Saturn
import requests
import json
import base64

saturn = Saturn()
api_token = saturn.get_api_key()
email = saturn.get_user_id()
jira_url = saturn.get_jira_url()


def fetchExistingIssue():
    #print(email)

    # Replace these with your own values

    issue_key = 'ISS-11'

    # Set up the request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")}'
    }

    # Send the request
    response = requests.get(f'{jira_url}/rest/api/3/issue/{issue_key}', headers=headers)

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


def main():
    fetchExistingIssue()


if __name__ == "__main__":
    main()