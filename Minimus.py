import configparser
import os


class APIConfig:
    def __init__(self, config_path=None):
        # Set default configuration path
        self.default_config_path = os.path.expanduser("~/.tethys/emailengine.api")
        self.config_path = config_path if config_path else self.default_config_path

        self.config = configparser.ConfigParser()
        self.load_configuration()

    def load_configuration(self):
        """Load configuration from a file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"No configuration file found at {self.config_path}")

        self.config.read(self.config_path)

    @property
    def client_id(self):
        """Get the client_id from the configuration file."""
        return self.config.get('Credentials', 'client_id', fallback="DefaultClientId")

    @property
    def client_secret(self):
        """Get the client_secret from the configuration file."""
        return self.config.get('Credentials', 'client_secret', fallback="DefaultClientSecret")

    @property
    def tenant_id(self):
        """Get the tenant_id from the configuration file."""
        return self.config.get('Credentials', 'tenant_id', fallback="DefaultTenantId")


# Usage
if __name__ == "__main__":
    try:
        # Instantiate with default path
        api_config = APIConfig("./emailengine.api")

        # Instantiate with a custom path
        # api_config = ApiConfig("/custom/path/to/emailengine.api")

        print("Client ID:", api_config.client_id)
        print("Client Secret:", api_config.client_secret)
        print("Tenant ID:", api_config.tenant_id)
    except FileNotFoundError as e:
        print(e)
