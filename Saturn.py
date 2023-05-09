import os

class Saturn:
    def __init__(self):
        # Get the path to the .openai directory in the user's home directory
        home_directory = os.path.expanduser('~')
        file_path = os.path.join(home_directory, '.tethys', 'tethys.api')
        with open(file_path, 'r') as f:
            contents = f.read()
        for line in contents.splitlines():
            key, value = line.split('~')
            if key == 'APIKEY':
                self.tethys_api_key = value.strip()
            if key == 'USERID':
                self.tethys_user_id = value.strip()
            if key == 'COMPANYID':
                self.company_id = value.strip()
            if key == 'ASSIGN_TO':
                self.assign_to = value.strip()


    def get_api_key(self):
        return self.tethys_api_key

    def get_user_id(self):
        return self.tethys_user_id

    def get_assign_to(self):
        return self.assign_to

    def get_company_id(self):
        return self.company_id

    def get_jira_url(self):
        return 'https://' + self.company_id + '.atlassian.net'
