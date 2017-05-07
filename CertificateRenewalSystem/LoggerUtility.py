#!/usr/bin/env python3

############################################
# MODULE IMPORT SECTION.
############################################
import logging
import config.LoggerConfig

# Import the `OS` module.
import os

############################################

# Get the Logger Instance for the application.
automate_cert_renewal_logger = logging.getLogger(config.LoggerConfig.APP_LOGGER_NAME)
automate_cert_renewal_logger.setLevel(config.LoggerConfig.LOGGER_LEVEL)

# Build the Logfile Location to store the log file(s).
# First check if it exists, if not create it.
if not os.path.exists(config.LoggerConfig.LOG_FILE_LOCATION):
    os.mkdir(config.LoggerConfig.LOG_FILE_LOCATION)

# Create a Handler Instance for handling log messages.
# The Handler takes in a message (a LogRecord) and passes it on
# to the Formatter Object.
# Here we want a Handler Instance that directs the messages
# to a file as well as to the console (i.e, for severe messages).
# Handler Instance for Redirecting messages to File.
log_file_handler = logging.FileHandler(config.LoggerConfig.LOG_FILENAME,
											mode=config.LoggerConfig.LOG_FILE_MODE)
log_file_handler.setLevel(config.LoggerConfig.FILE_HANDLER_LEVEL)
# Handler Instance for emitting messages to console.
# Log Level should have only severe messages printed
# to the console.
log_console_handler = logging.StreamHandler()
log_console_handler.setLevel(config.LoggerConfig.CONSOLE_HANDLER_LEVEL)

# Set up the Formatter Instance for formatting log messages.
# The Formatter will format the messages accordingly, as per
# the format specifier(s) provided as an initialization argument
# during instantiation.
log_file_formatter = logging.Formatter(config.LoggerConfig.FILE_FORMATTER_SETTING)
log_console_formatter = logging.Formatter(config.LoggerConfig.CONSOLE_FORMATTER_SETTING)
# Add the Formatter Object to the Handler Instances.
log_file_handler.setFormatter(log_file_formatter)
log_console_handler.setFormatter(log_console_formatter)

# Now add the Haandler to the logger.
# A logger can have multiple Handlers.
automate_cert_renewal_logger.addHandler(log_file_handler)
automate_cert_renewal_logger.addHandler(log_console_handler)
