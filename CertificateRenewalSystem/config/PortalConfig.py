# This is the Portal Config file, which stores the configuration options
# to be used when submitting the CSR via the Authorities' Web Portal.
# Make changes below to adapt the application to suit your environment
# requirements.

# Import the CSRConfig module for accessing the APP_NAME entry.
import CSRConfig

BASE_URL = 'https://certmanager.websecurity.symantec.com/mcelp/enroll/'

# The Request Method Dictionary.
# This enables the program to decide whether,
# the request needs to be *GET* or *POST*.
REQUEST_METHOD = {'GET': 0, 'POST': 1}

#*************************** VARIABLE SECTION ******************************

# The below option uniquely identifies the Certificate in question.
# The value varies per certificate.
ISSUER_SERIAL = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Submission Form Entities.
FIRST_NAME              = 'Dipankar'
LAST_NAME               = 'Achinta'
GROUP_EMAIL             = 'it@example.com'
SERVER_IP               = ''
PURPOSE                 = 'Certificate Renewal for ' + CSRConfig.APP_NAME
GROUP_MANAGER           = 'MANAGER_NAME'

#!!!!!!!!!!!!!!!!!!!!!!! CAUTION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# The below configuration, if needs to be altered
# we need to put the appropriate option from the
# enrollment portal's value options. To make changes
# to the below two values, contact the application
# owner or architect. 
SERVER_CATEGORY         = 'Apache'
SERVER_APPLICATION_TYPE = 'ApacheSSLEAYServer'

#!!!!!!!!!!!!!!!!!!!!!!! CAUTION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

SIGNATURE_ALGORITHM  = 'sha256WithRSAEncryption'
NUMBER_OF_LICENSES   = '2'
CERTIFICATE_VALIDITY = '2'
CHALLENGE_PHRASE     = 'FastFerr@ri1'

# List out the SANs required while raising the request.
# Structure: ['san_string_1', 'san_string_2', ...]
SAN_LIST = []

#*************************** VARIABLE SECTION ******************************

# This value is a constant within the organization's certificates.
# This value binds the certificate to the Organization's Certificate Domain.
JUR_HASH = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# URL METHOD - GET
URL_CERT_DETAILS_PAGE = BASE_URL + \
                        'searchCertDetails?issuerSerial=' + \
                        ISSUER_SERIAL + \
                        '&jur_hash=' + JUR_HASH

# URL METHOD - GET
URL_RENEW_PAGE = BASE_URL + 'startLcOp?issuerSerial=' + \
                 ISSUER_SERIAL + '&opCode=renew&csrfToken={0}&csrfToken={0}'

# URL METHOD - POST
# The below content-type is posted to the server.
# ::> Content-Type -> application/x-www-form-urlencoded
URL_ENROLL_PAGE = BASE_URL + 'processChallenge'

# URL METHOD - POST
URL_CSR_SUBMIT_PAGE = BASE_URL + 'enroll'
