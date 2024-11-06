from O365 import Account, FileSystemTokenBackend


class DeliverEngine:
    def __init__(self, client_id, client_secret, tenant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.account = None
        self.setup_account()

    def setup_account(self):
        """Setup the O365 account connection."""
        token_backend = FileSystemTokenBackend(token_path='.', token_filename='o365_token.txt')
        credentials = (self.client_id, self.client_secret)
        self.account = Account(credentials, token_backend=token_backend, tenant_id=self.tenant_id)

        if not self.account.is_authenticated:
            self.account.authenticate(scopes=['basic', 'message_all'])

    def send_email(self, to, subject, body, attachment_path, from_address=None):
        """Send an email with an attachment."""
        if not self.account.is_authenticated:
            print("Account is not authenticated. Please authenticate first.")
            return

        mailbox = self.account.mailbox()
        message = mailbox.new_message()

        message.to.add(to)
        message.subject = subject
        message.body = body
        if from_address:
            message.sender.address = from_address  # Set the sender's address if provided and permitted

        message.attachments.add(attachment_path)
        message.send()
        print("Email sent successfully!")


def main():
    client_id = 'your_client_id_here'
    client_secret = 'your_client_secret_here'
    tenant_id = 'your_tenant_id_here'

    # Create an instance of the DeliverEngine
    engine = DeliverEngine(client_id, client_secret, tenant_id)

    # Test case: Send an email with attachment
    engine.send_email(
        to='recipient@example.com',
        subject="Today's Results",
        body='Please find attached the results for today.',
        attachment_path='path_to_your_file/results.xlsx'
    )


if __name__ == "__main__":
    main()
