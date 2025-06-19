import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

################################
#                              #
#            Logger            #
#                              #
################################

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()  # also print to console
    ]
)

# public functions for logging
def log_error(msg):
    logger.error(msg)
    
def log_info(msg):
    logger.info(msg)

logger = logging.getLogger(__name__)