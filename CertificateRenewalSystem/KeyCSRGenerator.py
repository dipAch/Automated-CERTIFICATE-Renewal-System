#!/usr/bin/env python3

# Author: Dipankar Achinta, 2017 [dipankar.achinta@supervalu.com]
# Date  : 23/03/2017

'''
   This module holds the Class Definition to generate the CSR (Certificate
   Signing Request) and the server's Private Key for furthering the Certificate
   Generation procedure. This Utility makes use of the OpenSSL Tool to perform
   the various operations related to CSR and Private-Key generation.
   The various methods/interfaces exposed by the below Class(s), only act as a
   wrapper for the OpenSSL Tool.
'''

##################################################################
# Module Import Section.
# Make all the necessary imports within this section.
# Don't Pollute the entire file, with imports here and there.
##################################################################

# The below import deals with system user information.
import getpass
# The below import is a time manipulation utility library.
import time
# The below library utility provides the system's information.
import platform
# Below module handles subprocesses and their interaction.
import subprocess, io
# Below module holds the configuration options for the CSR
# generation.
import config.CSRConfig
# Logging Module to enable this application to log its events.
import logging
# To help out with OS level interactions.
import os

##################################################################

##################################################################
# Setting up the logger Instance.

import LoggerUtility
import config.LoggerConfig

GENERATE_CSR_PKEY_LOGGER_NAME = '.CertificateGenerator'

# Instantiate the module level Logger object.
csr_pkey_gen_logger = logging.getLogger(config.LoggerConfig.APP_LOGGER_NAME + GENERATE_CSR_PKEY_LOGGER_NAME)

##################################################################

class CSRKeyGenerator(object):
	'''
	   Generate the *CSR* and the *Private Key*.
	'''

	def __init__(self):
		'''
		   Perform certain Environment Information Initialization.
		   Below information can be logged, for auditing purposes.
		'''
		self.time      = time.ctime()
		self.user      = getpass.getuser()
		self.host      = platform.node()
		self.os_info   = platform.system()
		# Log a comment.
		csr_pkey_gen_logger.info('[Time: %s, User: %s, Host: %s, OS_INFO: %s]', self.time, self.user, self.host, self.os_info)

	def generate_csr_pkey(self, use_existing_pkey=None):
		'''
		   Wrapper for calling OpenSSL Tool. This is a sub-part
		   into the entire process. In this part, the utility issues
		   a CSR generation command via OpenSSL.
		'''

		# Build the CSR store and Private Key store directory locations.
		# First check if it exists, if not create it.
		# Check for the CSR output directory location.
		if not os.path.exists(config.CSRConfig.CSR_DIRECTORY_LOCATION):
			os.mkdir(config.CSRConfig.CSR_DIRECTORY_LOCATION)

		# Check for the PRIVATE KEY output directory location as well.
		if not os.path.exists(config.CSRConfig.PKEY_DIRECTORY_LOCATION):
			os.mkdir(config.CSRConfig.PKEY_DIRECTORY_LOCATION)

		if use_existing_pkey:
			# We only create a new CSR. We will be
			# using the existing PKEY, when installing
			# the `CERTIFICATE`.
			openssl_command = 'openssl req -out ' + \
							  config.CSRConfig.CSR_NAME + \
							  ' -key ' + use_existing_pkey + ' -new'
		else:
			# Generate a new CSR and PKEY pair.
			openssl_command = 'openssl req -out ' + \
							  config.CSRConfig.CSR_NAME + \
							  ' -new -newkey rsa:2048 -nodes -keyout ' + \
							  config.CSRConfig.PRIVATE_KEY_NAME

		# Create a PIPED OpenSSL Sub-Process.
		proc = subprocess.Popen(openssl_command, shell=True,
												 stdin=subprocess.PIPE,
												 stdout=subprocess.PIPE,)
		
		# Log a comment
		csr_pkey_gen_logger.info('Subprocess and PIPE Instantiated.')
		
		# Instantiate the STDIN stream for the PIPED Process.
		stdin = io.TextIOWrapper(proc.stdin, encoding='utf-8',
											 line_buffering=True,)
		# Perform the same as well for the STDOUT stream.
		stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8',)
		
		# Log a comment
		csr_pkey_gen_logger.info('STDIN and STDOUT have been Instantiated.')

		# Output Start Marker.
		print('\n********************** SUBPROCESS OUTPUT *********************\n')

		# Start sending the certificate information to the subprocess
		# prompt. This data should be kept seperate in a configuration
		# file, as it is subject to change based on the CSR requirement.
		for info in config.CSRConfig.CSR_INFO:
			# Append the new-line to the input to seperate out
			# the passed in data.
			info_line = '{}\n'.format(info)
			# Write the data to the OpenSSL process.
			stdin.write(info_line)
			
			# Log a comment
			csr_pkey_gen_logger.debug('Passing in value: %s', info_line)

		# Get the remaining output from the child process and
		# display it on screen.
		remaining_proc_out = proc.communicate()[0].decode('utf-8')
		print(remaining_proc_out)

		# Output End Marker.
		print('\n********************** SUBPROCESS OUTPUT *********************\n')

# Execute Module Code.
# Just load the Module, in case it's not run as a stand-alone program.
if __name__ == '__main__':
	# Go for CSR creation, iff you do not have the old existing CSR and its
	# corresponding P_KEY.
	if not os.path.isfile(config.CSRConfig.USE_EXISTING_CSR) and not os.path.isfile((config.CSRConfig.CSR_NAME)):
		# Instantiating the CSR and Key Generator Class.
		csr_pkey_generator = CSRKeyGenerator()
		# Log a comment.
		csr_pkey_gen_logger.info('Instantiated Certificate Generator Object.')
		
		# Now time to check whether we have an existing PKEY.
		if not os.path.isfile(config.CSRConfig.USE_EXISTING_PKEY) and not os.path.isfile(config.CSRConfig.PRIVATE_KEY_NAME):
			# This will generate a brand new CSR and PKEY pair.
			# Initiate Generation.
			csr_pkey_gen_logger.info('Generating CSR and Private Key.')
			csr_pkey_generator.generate_csr_pkey()
		else:
			# This will generate a CSR based on the existing PKEY.
			# The PKEY to use might be in some other directory location or it
			# might be in the program's home directory's PKEY store.
			pkey_file_location = config.CSRConfig.USE_EXISTING_PKEY or config.CSRConfig.PRIVATE_KEY_NAME
			# Initiate Generation.
			csr_pkey_gen_logger.info('Generating CSR from Existing Private Key.')
			csr_pkey_generator.generate_csr_pkey(use_existing_pkey=pkey_file_location)
		csr_pkey_gen_logger.info('CSR and Private Key have been generated in the presently configured directory.')
	else:
		csr_pkey_gen_logger.info('Using Existing CSR: %s', (config.CSRConfig.USE_EXISTING_CSR or config.CSRConfig.CSR_NAME))
