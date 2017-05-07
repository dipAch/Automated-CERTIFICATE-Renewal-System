#!/usr/bin/env python3

# This module deals with the part where we need to submit the generated
# CSR to the Certificate Issuing Authority. The CSR needs to be uploaded
# with other relevant information to the Authorities' Renewal portal.

#########################################################################
# Module Import Section.
# Please import all the necessary modules in this section only.
# Do not pollute the entire file with imports here and there.
#########################################################################

import requests
import logging
import RequestUtility
import config.PortalConfig
import sys
import config.CSRConfig
from bs4 import BeautifulSoup

# To be used when performing time manipulation operations.
import time

# Below module helps getting user details.
import getpass

# Below module captures the system information.
import platform

#########################################################################

#########################################################################
# Setting up the logger Instance.

import LoggerUtility
import config.LoggerConfig

UPLOAD_CSR_LOGGER_NAME = '.CSRPortalUploader'

# Instantiate the module level Logger Object.
csr_uploader_logger = logging.getLogger(config.LoggerConfig.APP_LOGGER_NAME + UPLOAD_CSR_LOGGER_NAME)

#########################################################################

# Below is the class definition that makes the CSR submission
# for the desired certificate renewal procedure.
class SubmitCSRToPortal(object):
	'''
	   The Class Definition which performs the Automated Online CSR Submission.
	'''

	def __init__(self):
		'''
		   Capture environment information and other relevant information
		   for auditing purposes. These information must be captured before
		   the CSR submision.
		'''
		self.time                 = time.ctime()
		self.user                 = getpass.getuser()
		self.host                 = platform.node()
		self.os_info              = platform.system()
		# Instantiate a session object, before transaction begins.
		self.cert_renewal_session = requests.Session()
		# Execution Status Flag.
		self.failure              = False
		# Log a comment.
		csr_uploader_logger.info('[Time: %s, User: %s, Host: %s, OS_INFO: %s]', self.time, self.user, self.host, self.os_info)

	def get_cert_details(self, url_cert_details_page):
		'''
		   Requests the Certificate details page, which contains the options
		   to Renew / Replace / Download that particular Certificate.
		'''
		try:
			resp_cert_details_page = RequestUtility.request_web_resource(config.PortalConfig.REQUEST_METHOD['GET'], url_cert_details_page, self.cert_renewal_session)
			csrf_token = None
			if resp_cert_details_page.status_code == requests.codes.ok:
				# Get the CSRF token.
				# This token should be passed to all the subsequent requests.
				# This token prevents Cross-Site Scripting and is used as a
				# preventive measure by site developers.
				csrf_token = resp_cert_details_page.text[1182:1246]
				csr_uploader_logger.info('Response Code [DETAILS_PAGE]: %s', resp_cert_details_page.status_code)
				csr_uploader_logger.info('CSRF Token: %s', csrf_token)
			else:
				# Log a comment stating the returned Response code.
				csr_uploader_logger.error('Response Code [DETAILS_PAGE]: %s', resp_cert_details_page.status_code)
				csr_uploader_logger.error('CSRF Token: %s', csrf_token)
				self.failure = True
			return (csrf_token, resp_cert_details_page.status_code)
		except requests.exceptions.RequestException as request_err:
			# Log Error and turn on evasive mode.
			csr_uploader_logger.critical('EXCEPTION_OCCURED::[DETAILS_PAGE]::ABORTING::' + str(request_err))
			self.failure = True
			# We are returning the below tuple because when exception occurs,
			# the caller expects a Tuple and because of Exception, as this is
			# a function, the return type defaults to None. This cannot be
			# assigned to the multiple assignment statement. Hence, to
			# overcome that issue, we are returning a None sequence Tuple.
			return (None, None)

	def select_renew_option(self, url_renew_page):
		'''
		   Choose the Renew option from the Certificate Details Page.
		'''
		try:
			# This page contains two options.
			# Either proceed via previously set Challenge Phrase or bypass it. 
			resp_renew_page = RequestUtility.request_web_resource(config.PortalConfig.REQUEST_METHOD['GET'], url_renew_page, self.cert_renewal_session)
			if resp_renew_page.status_code == requests.codes.ok:
				# Return the Response code.
				csr_uploader_logger.info('Response Code [RENEW_PAGE]: %s', resp_renew_page.status_code)
			else:
				# Log a comment stating the returned Response code.
				csr_uploader_logger.error('Response Code [RENEW_PAGE]: %s', resp_renew_page.status_code)
				self.failure = True
			return resp_renew_page.status_code
		except requests.exceptions.RequestException as request_err:
			# Log Error and turn on evasive mode.
			csr_uploader_logger.critical('EXCEPTION_OCCURED::[RENEW_PAGE]::ABORTING::' + str(request_err))
			self.failure = True

	def bypass_challenge_phrase(self, url_enroll_page, csrf_token):
		'''
		   Choose to proceed with Challenge Phrase or try bypassing it.
		'''
		# If return code was successful, then proceed to enroll page.
		# Prepare the POST payload.
		# This payload remains constant and does not vary across requests.
		data_payload = {'challengePhrase'   : '',
						'withChallenge'     : 'false',
						'opCode'            : 'renew',
						'newCertProductType': '',
						'csrfToken'         : csrf_token,}
		try:
			resp_enroll_page = RequestUtility.request_web_resource(config.PortalConfig.REQUEST_METHOD['POST'], url_enroll_page, self.cert_renewal_session, data_payload)
			if resp_enroll_page.status_code == requests.codes.ok:
				# Return the Response code.
				csr_uploader_logger.info('Response Code [ENROLL_PAGE]: %s', resp_enroll_page.status_code)
				
				# Below logging statement should not be run in production.
				csr_uploader_logger.debug(str(resp_enroll_page.text))
				
				# Also in the process, check the enrollment page if any Subject
				# Alternative Name (SAN) already exists.
				CURRENT_SAN_SEPERATOR = ','
				souped_up_enrollment = BeautifulSoup(resp_enroll_page.text, 'html.parser')
				# Gather the `TEXTAREA` tags, based on the `ID` value supplied.
				# Should return one entity only, as `ID` attribute is used.
				# Get the `SAN` text present within the previously parsed HTML
				# entity.
				san_names = souped_up_enrollment.select('#subject_alt_names')[0].string
				# The `TEXT` is comma seperated, hence we need to split it based on tha
				san_list = san_names.split(CURRENT_SAN_SEPERATOR)

				# Log a comment.
				csr_uploader_logger.debug('SAN Values [Enrollment Page]: ' + str(san_list))
			else:
				# Log a comment stating the returned Response code.
				csr_uploader_logger.error('Response Code [ENROLL_PAGE]: %s', resp_enroll_page.status_code)
				self.failure = True
			return resp_enroll_page.status_code, san_list
		except requests.exceptions.RequestException as request_err:
			# Log Error and turn on evasive mode.
			csr_uploader_logger.critical('EXCEPTION_OCCURED::[ENROLL_PAGE]::ABORTING::' + str(request_err))
			self.failure = True

	def submit_csr_details(self, url_csr_submit_page, csr_content, csrf_token, san_list):
		'''
		   The final step in the process. Submit the CSR details to the
		   Certificate Authority.
		'''
		# Prepare the POST payload.
		# Getting the Service Agreement Notes
		AGREEMENT_FILE_NAME = './extras/SymantecServiceAgreement.txt' 
		try:
			with open(AGREEMENT_FILE_NAME, 'r') as agreement_file_obj:
				SERVICE_AGREEMENT_NOTES = agreement_file_obj.read()
		except (IOError, OSError) as agreement_file_err:
			# Log a comment and abort.
			csr_uploader_logger.error('EXCEPTION_OCCURED::[AGREEMENT_FILE_ACCESS]::ABORTING::' + str(agreement_file_err))
			sys.exit(1)

		# Curate the SANs to be included in the request.
		if config.PortalConfig.SAN_LIST:
			curated_san_list = '\n'.join(san_list + config.PortalConfig.SAN_LIST)
		else:
			curated_san_list = '\n'.join(san_list)

		# Log a comment.
		csr_uploader_logger.debug('CURATED_SAN_LIST <FINALIZED> => ' + curated_san_list)
		
		# This payload should come from a configuration file,
		# as the data might change from one requester to another.
		# The most important item in the payload is the CSR_content field.
		# NOTE: Values for *subAgreementID* & *subAgreementVersion* can be
		# found in the source code hosted at location, 
		# URI: https://www.symantec.com/scripts/agreement/subscriber_us.js
		multipart_form_payload = {
								 'contactInfo.firstName': (None, config.PortalConfig.FIRST_NAME),
								 'contactInfo.lastName': (None, config.PortalConfig.LAST_NAME),
								 'contactInfo.email': (None, config.PortalConfig.GROUP_EMAIL),
								 'contactInfo.additional_field10': (None, config.PortalConfig.SERVER_IP),
								 'contactInfo.additional_field4': (None, config.PortalConfig.PURPOSE),
								 'contactInfo.additional_field5': (None, config.PortalConfig.GROUP_MANAGER),
								 'CheckWeakKey': (None, 'yes'),
								 'contactInfo.additional_field9': (None, config.PortalConfig.SERVER_CATEGORY),
								 'wildcardType': (None, 'N'),
								 'application': (None, config.PortalConfig.SERVER_APPLICATION_TYPE),
								 'csrChoice': (None, 'text'),
								 'csrInfo.csrText': (None, csr_content[:-1]),
								 'csrGeneratedFromApplet': (None, 'N'),
								 'csrInfo.subjectAltNames': (None, curated_san_list),
								 'signatureAlgorithm': (None, config.PortalConfig.SIGNATURE_ALGORITHM),
								 'numLicense': (None, config.PortalConfig.NUMBER_OF_LICENSES),
								 'validity': (None, config.PortalConfig.CERTIFICATE_VALIDITY),
								 'ctLogOptionChecked': (None, 'true'),
								 'challenge': (None, config.PortalConfig.CHALLENGE_PHRASE),
								 'confirmChallenge': (None, config.PortalConfig.CHALLENGE_PHRASE),
								 'subAgreementID': (None, 'SSL Certificate Subscriber Agreement Version 10.0 (April 2014)'),
								 'subAgreementVersion': (None, '10.0'),
								 'subAgreement': (None, SERVICE_AGREEMENT_NOTES[:-1]),
								 'csrfToken': (None, csrf_token),
								 }
		try:
			# This is the Final page where we submit the CSR,
			# via the web form.
			resp_csr_submit_page = RequestUtility.request_web_resource(config.PortalConfig.REQUEST_METHOD['POST'], url_csr_submit_page, self.cert_renewal_session, multipart_form_payload, multipart_form=True)
			if resp_csr_submit_page.status_code == requests.codes.ok:
				# Log success comment and return success code.
				csr_uploader_logger.info('Response Code [SUBMIT_PAGE]: %s', resp_csr_submit_page.status_code) 
			else:
				# Log a comment stating the returned Response code.
				csr_uploader_logger.error('Response Code [SUBMIT_PAGE]: %s', resp_csr_submit_page.status_code)
				self.failure = True
			return resp_csr_submit_page.status_code
		except requests.exceptions.RequestException as request_err:
			# Log Error and turn on evasive mode.
			csr_uploader_logger.critical('EXCEPTION_OCCURED::[SUBMIT_PAGE]::ABORTING::' + str(request_err))
			self.failure = True

if __name__ == '__main__':
	# Instantiate a CSR Submission Bot.
	csr_submission_bot = SubmitCSRToPortal()

	# Let's get CSR data ready for submission.
	# We will read it to a variable.
	# For the sake of testing out the code, I'll be using a DUMMY CSR file.
	DUMMY_CSR_FILE_NAME = config.CSRConfig.CSR_NAME

	# Use the `with as` context management protocol.
	# This handles the proper closing of open files and spares us from
	# doing it manually.
	try:
		with open(DUMMY_CSR_FILE_NAME, 'r') as dummy_csr_file_obj:
			DUMMY_CSR_CONTENT = dummy_csr_file_obj.read()
	except (IOError, OSError) as dummy_csr_file_err:
		# Log a comment and abort.
		csr_uploader_logger.error('EXCEPTION_OCCURED::[DUMMY_CSR_FILE_ACCESS]::ABORTING::' + str(dummy_csr_file_err))
		sys.exit(1)

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
		csr_uploader_logger.error('Failed to Retrieve Details Page')
		sys.exit(1)

	# Check for response to fetching the Renew Option.
	if renew_resp_code == requests.codes.ok and not csr_submission_bot.failure:
		# Make a POST request to the enrollment page.
		enroll_resp_code, san_list = csr_submission_bot.bypass_challenge_phrase(config.PortalConfig.URL_ENROLL_PAGE, csrf_token)
	else:
		# Log a comment and abort.
		csr_uploader_logger.error('Failed to Retrieve Renew Page')
		sys.exit(1)

	# Check for response to retrieving the Certificate Enrollment Form.
	if enroll_resp_code == requests.codes.ok and not csr_submission_bot.failure:
		# Make a Final POST request, posting the relevant information
		# about the certificate.

		# Log a comment.
		csr_uploader_logger.debug('Going Strong: Should Submit CSR now')
		
		# Perform the CSR Submit action.
		csr_submit_resp_code = csr_submission_bot.submit_csr_details(config.PortalConfig.URL_CSR_SUBMIT_PAGE, DUMMY_CSR_CONTENT, csrf_token, san_list)
	else:
		# Log a comment and abort.
		csr_uploader_logger.error('Failed to Retrieve Enrollment Page')
		sys.exit(1)

	# Check for the response to having successfully submitted the CSR.
	if csr_submit_resp_code == requests.codes.ok and not csr_submission_bot.failure:
		# Log a Successful Process Completion Entry.
		csr_uploader_logger.info('CSR Submission Procedure Successfully Completed')
	else:
		# Log a comment.
		# Also Abort.
		csr_uploader_logger.error('CSR Submission Process Failed. Check Log File Traceback')
		sys.exit(1)