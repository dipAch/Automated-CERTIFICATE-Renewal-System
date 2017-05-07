#!/usr/bin/env python3

# Author: Dipankar Achinta, 2017 [dipankar.achinta@supervalu.com]
# Date  : 23/03/2017

'''
   This is the Supervisor Script that calls the various components
   of the workflow. We are importing the individual functionalities
   and stitching them together in this module.
'''

####################################################################
# Module Import Section.
# Make all necessary imports in this and this section only.
# Don't Pollute the entire file with unecessary imports here and
# there.
####################################################################

import KeyCSRGenerator
import SubmitCSR
import config.PortalConfig
import requests
import sys
import os
import config.CSRConfig

####################################################################

# Start the Certificate Renewal Process.
# The process needs the CSR and Private Key to be generated,
# before submitting off the request to the Certificate Issuers'
# portal.

# Go for CSR creation, iff you do not have the old existing CSR and its
# corresponding P_KEY.
# Also do check that the CSR is not present in the CSR store, within the
# program's home directory.
if not os.path.isfile(config.CSRConfig.USE_EXISTING_CSR) and not os.path.isfile((config.CSRConfig.CSR_NAME)):
	# Instantiating the CSR and Key Generator Class.
	csr_pkey_generator = KeyCSRGenerator.CSRKeyGenerator()
	# Log a comment.
	KeyCSRGenerator.csr_pkey_gen_logger.info('Instantiated Certificate Generator Object.')
	
	# Now time to check whether we have an existing PKEY.
	if not os.path.isfile(config.CSRConfig.USE_EXISTING_PKEY) and not os.path.isfile(config.CSRConfig.PRIVATE_KEY_NAME):
		# This will generate a brand new CSR and PKEY pair.
		# Initiate Generation.
		KeyCSRGenerator.csr_pkey_gen_logger.info('Generating CSR and Private Key.')
		csr_pkey_generator.generate_csr_pkey()
	else:
		# This will generate a CSR based on the existing PKEY.
		# The PKEY to use might be in some other directory location or it
		# might be in the program's home directory's PKEY store.
		pkey_file_location = config.CSRConfig.USE_EXISTING_PKEY or config.CSRConfig.PRIVATE_KEY_NAME
		# Initiate Generation.
		KeyCSRGenerator.csr_pkey_gen_logger.info('Generating CSR from Existing Private Key.')
		csr_pkey_generator.generate_csr_pkey(use_existing_pkey=pkey_file_location)
	KeyCSRGenerator.csr_pkey_gen_logger.info('CSR and Private Key have been generated in the presently configured directory.')
else:
	KeyCSRGenerator.csr_pkey_gen_logger.info('Using Existing CSR: %s', (config.CSRConfig.USE_EXISTING_CSR or config.CSRConfig.CSR_NAME))

# Let's get CSR data ready for submission.
# We will read it to a variable.
# First lets determine the CSR file and prepare the content for submission.
csr_file_name = config.CSRConfig.USE_EXISTING_CSR or config.CSRConfig.CSR_NAME

# Use the `with as` context management protocol.
# This handles the proper closing of open files and spares us from
# doing it manually.
try:
	with open(csr_file_name, 'r') as csr_file_obj:
		csr_content = csr_file_obj.read()
except (IOError, OSError) as csr_file_err:
	# Log a comment and abort.
	SubmitCSR.csr_uploader_logger.error('EXCEPTION_OCCURED::[CSR_FILE_ACCESS]::ABORTING::' + str(csr_file_err))
	sys.exit(1)

# Now handing over the charge to the Online CSR submission Process.
# This process performs the task of uploading the software generated
# CSR to the Certificate Authority via the portal.
# Instantiate a CSR Submission Bot.
csr_submission_bot = SubmitCSR.SubmitCSRToPortal()

# Request the Certificate Details Page.
# This is the initial page in the entire flow.
csrf_token, details_resp_code = csr_submission_bot.get_cert_details(config.PortalConfig.URL_CERT_DETAILS_PAGE)

# Check the response to fetching the Details Page.
if details_resp_code == requests.codes.ok and not csr_submission_bot.failure:
	# Imitate clicking on the Renew Option.
	renew_url = config.PortalConfig.URL_RENEW_PAGE.format(csrf_token)
	renew_resp_code = csr_submission_bot.select_renew_option(renew_url)
else:
	# Log a comment and abort.
	SubmitCSR.csr_uploader_logger.error('Failed to Retrieve Details Page')
	sys.exit(1)

# Check for response to fetching the Renew Option.
if renew_resp_code == requests.codes.ok and not csr_submission_bot.failure:
	# Make a POST request to the enrollment page.
	enroll_resp_code, san_list = csr_submission_bot.bypass_challenge_phrase(config.PortalConfig.URL_ENROLL_PAGE, csrf_token)
else:
	# Log a comment and abort.
	SubmitCSR.csr_uploader_logger.error('Failed to Retrieve Renew Page')
	sys.exit(1)

# Check for response to retrieving the Certificate Enrollment Form.
if enroll_resp_code == requests.codes.ok and not csr_submission_bot.failure:
	# Make a Final POST request, posting the relevant information
	# about the certificate.

	# Log a comment.
	SubmitCSR.csr_uploader_logger.debug('Going Strong: Should Submit CSR now')

	csr_submit_resp_code = csr_submission_bot.submit_csr_details(config.PortalConfig.URL_CSR_SUBMIT_PAGE, csr_content, csrf_token, san_list)
else:
	# Log a comment and abort.
	SubmitCSR.csr_uploader_logger.error('Failed to Retrieve Enrollment Page')
	sys.exit(1)

# Check for the response to having successfully submitted the CSR.
if csr_submit_resp_code == requests.codes.ok and not csr_submission_bot.failure:
	# Log a Successful Process Completion Entry.
	SubmitCSR.csr_uploader_logger.info('CSR Submission Procedure Successfully Completed')
else:
	# Log a comment.
	# Also Abort.
	SubmitCSR.csr_uploader_logger.error('CSR Submission Process Failed. Check Log File Traceback')
	sys.exit(1)
