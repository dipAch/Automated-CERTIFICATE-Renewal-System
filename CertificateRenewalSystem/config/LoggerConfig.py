# Configuration Options for the Application's Logging Facility.
# Make changes to the behaviour of the Logger by changing
# the specified options present below.

import logging

# Configure the Application wide Logger name.
APP_LOGGER_NAME = 'LoggerUtility::AUTO_CERT_RENEWAL'

# Set the Log Level for the Logger components.
LOGGER_LEVEL = logging.INFO
FILE_HANDLER_LEVEL = logging.DEBUG
CONSOLE_HANDLER_LEVEL = logging.INFO

# File Handler Settings
LOG_FILE_LOCATION = '/home/vagrant/python_progs/cert_issuer/log/'
LOG_FILENAME = LOG_FILE_LOCATION + 'AutoCertRenewal.log'

# We chose mode `w` (Write-Mode), as we need a new file to be created
# for each build. This is not a rolling application log.
# If the file already exists, the contents will be clobbered.
LOG_FILE_MODE = 'w'

# Set the Formatter settings and options.
FILE_FORMATTER_SETTING = '[%(asctime)s] :: [%(levelname)s] :: [%(threadName)s] :: [%(name)s] >> %(message)s'
CONSOLE_FORMATTER_SETTING = '[%(asctime)s] :: [%(levelname)s] :: [%(name)s] >> %(message)s'
