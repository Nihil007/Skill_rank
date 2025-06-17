# Import Python's built-in logging module
import logging  

# Function to configure global logging settings
def setup_logging():
    logging.basicConfig(
        # Set minimum log level to INFO
        level=logging.INFO,  
        # Log format: timestamp, level, message
        format="%(asctime)s [%(levelname)s] %(message)s",  
    )
