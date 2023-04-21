from Saturn import Saturn
import requests
import json
import base64
import requests
from requests.auth import HTTPBasicAuth

saturn = Saturn()
api_token = saturn.get_api_key()
email = saturn.get_user_id()
jira_url = saturn.get_jira_url()


def fetchCustomFields():
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(
        f"{jira_url}/rest/api/3/field",
        headers=headers,
        auth=HTTPBasicAuth(email, api_token)
    )

    if response.status_code == 200:
        fields = response.json()
        for field in fields:
            print(f"{field['name']} ({field['id']})")
    else:
        print(f"Error fetching custom fields: {response.status_code} - {response.text}")


def main():
    fetchCustomFields()


if __name__ == "__main__":
    main()