from O365 import Account, FileSystemTokenBackend

# Define your credentials
CLIENT_ID = 'your_client_id_here'
CLIENT_SECRET = 'your_client_secret_here'
TENANT_ID = 'your_tenant_id_here'

# Set the token backend for caching
token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')

# Initialize the Account
credentials = (CLIENT_ID, CLIENT_SECRET)
account = Account(credentials, token_backend=token_backend, tenant_id=TENANT_ID)

# Authenticate the account (only needed when the token is not available or expired)
if not account.is_authenticated:
    # Will open a browser window for the login flow
    account.authenticate(scopes=['basic', 'message_all'])

# Get the mailbox
mailbox = account.mailbox()

# Create new message
message = mailbox.new_message()

# Set email properties
message.to.add('recipient@example.com')
message.subject = "Today's results"
message.body = "Please find attached the results for today."

# Add an attachment
message.attachments.add('path_to_your_file/results.xlsx')

# Send the email
message.send()

print("Email sent successfully!")
