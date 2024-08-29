import logging
from logging.handlers import RotatingFileHandler

# Configure Logger
logger = logging.getLogger('MyApp')
logger.setLevel(logging.DEBUG)  # Set to the least severe events you want to track

# Create Handlers
# RotatingFileHandler to rotate logs after reaching a certain file size
file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024*5, backupCount=5)  # 5 MB per file, with 5 backup files
file_handler.setLevel(logging.DEBUG)  # Set to the level you want for the file

# StreamHandler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set to the level you want for the console

# Create a Formatter and add to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example usage
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")