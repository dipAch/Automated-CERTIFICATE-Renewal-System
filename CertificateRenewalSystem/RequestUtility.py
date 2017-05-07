#!/usr/bin/env python3

# This is the utility file, that hosts utility functions
# to traverse the web. The methods, when requesting web resources
# proxy their requests via the below utility functions.

def request_web_resource(method_type, url_to_request, session_obj, post_payload=None, multipart_form=False):
		'''
			 Utility to proxy outbound requests. Proxies both GET & POST requests.
			 The initial Three (3) parameters are mandatory, while invoking this
			 helper function.
			 The *method_type* parameter should be fed only Boolean Values.

			 In the configuration file, the value is set as,
			 *************
			 * GET  -> 0 *
			 * POST -> 1 *
			 *************
		'''
		if method_type:
				if not multipart_form:
						# For POST Requests.
						url_response = session_obj.post(url_to_request, data=post_payload)
				else:
						# For Multipart-Form Data POST Requests.
						url_response = session_obj.post(url_to_request, files=post_payload)
		else:
				# For GET Requests.
				url_response = session_obj.get(url_to_request)
		return url_response
