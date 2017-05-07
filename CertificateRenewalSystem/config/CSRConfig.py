# The configuration file for the automated CSR and Private Key Generation.
# Please change the below settings, to suit your need.

# Option Initiailizers.
# Use this option whenever not sure of the option value.
VALUE_NOT_SET = False
VALUE_SET     = True

# Directory Locations within the program's home directory.
# They are created by the program at the time of initialization.
CSR_DIRECTORY_LOCATION  = 'csr_store/'
PKEY_DIRECTORY_LOCATION = 'private_key_store/'

# Other initialization settings.
CSR_EXTENSION           = '.csr'
PKEY_EXTENSION          = '.key'

#********************** VARIABLE SECTION ************************

# Generic Information pertaining to CSR and Private-Key name.
# Change the below value(s) to suit your requirements.
APP_NAME         = 'www.example.com'
CSR_NAME         = CSR_DIRECTORY_LOCATION + APP_NAME + CSR_EXTENSION
PRIVATE_KEY_NAME = PKEY_DIRECTORY_LOCATION + APP_NAME + PKEY_EXTENSION

# Select Existing CSR option.
# The Defaullt value is set to `FALSE`.
# If you have an existing CSR. set the below option to the path
# of the existing CSR. If CSR exists in the configured program directory,
# the program will take care of it automatically, nothing needs to be done
# from our end.
USE_EXISTING_CSR  = VALUE_NOT_SET

# If you want to use an existing PKEY to create the CSR then,
# set the below option to point to the path of the PKEY file.
# Again, it's set to `FALSE` by default.
USE_EXISTING_PKEY = VALUE_NOT_SET

# *CSR INFO* [Required Fields].
COUNTRY             = 'US'
STATE               = 'SOME_STATE'
LOCALITY            = 'SOME_CITY'
ORGANIZATION        = 'SOME_ORGANIZATION'
ORGANIZATIONAL_UNIT = 'IT'
COMMON_NAME         = APP_NAME
EMAIL_ADDRESS       = 'it@example.com'
DEFAULT             = ''

#********************** VARIABLE SECTION ************************

# The list of values to be supplied to the OpenSSL Process.
CSR_INFO = [COUNTRY, STATE, LOCALITY, ORGANIZATION, ORGANIZATIONAL_UNIT,
            COMMON_NAME, EMAIL_ADDRESS, DEFAULT, DEFAULT]
