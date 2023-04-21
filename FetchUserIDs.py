from Saturn import Saturn
import requests
import json
import base64

saturn = Saturn()
api_token = saturn.get_api_key()
email = saturn.get_user_id()
jira_url = saturn.get_jira_url()

def fetchUserID():
    jira_url = 'https://wmmc.atlassian.net'
    # Get the email address to search from the user
    search_email = input("Enter the email address of the user you want to find: ")

    # Set up the request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {base64.b64encode(f"{email}:{api_token}".encode("utf-8")).decode("utf-8")}'
    }

    # Send the request
    response = requests.get(f'{jira_url}/rest/api/3/user/search?query={search_email}', headers=headers)

    # Check the response
    if response.status_code == 200:
        users = response.json()
        if users:
            user = users[0]
            print(f"User accountId: {user['accountId']}")
            print(f"User display name: {user['displayName']}")
        else:
            print(f"No users found for email: {search_email}")
    else:
        print(f"Error searching for user: {response.status_code} - {response.text}")



def main():
    fetchUserID()

if __name__ == "__main__":
    main()