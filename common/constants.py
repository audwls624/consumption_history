# API STATUS MESSAGE
API_STATUS_MESSAGE_EXPIRED_TOKEN = "EXPIRED_TOKEN"
API_STATUS_MESSAGE_INVALID_SIGNATURE = "INVALID_SIGNATURE"
API_STATUS_MESSAGE_COMMON_TOKEN_ERROR = "COMMON_TOKEN_ERROR"
API_STATUS_MESSAGE_TOKEN_TYPE_ERROR = "TOKEN_TYPE_ERROR"
API_STATUS_MESSAGE_TOKEN_PAYLOAD_DATA_ERROR = "TOKEN_PAYLOAD_DATA_ERROR"
API_STATUS_MESSAGE_TOKEN_USER_NOT_EXISTS = "TOKEN_USER_NOT_EXISTS"
API_STATUS_MESSAGE_BAD_REQUEST = "BAD_REQUEST"
API_STATUS_MESSAGE_EMAIL_VALIDATION_FALSE = "EMAIL_VALIDATION_FALSE"
API_STATUS_MESSAGE_UNAUTHORIZED = "UNAUTHORIZED"
API_STATUS_MESSAGE_NOT_FOUND = "PAGE_NOT_FOUND"
API_STATUS_MESSAGE_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
API_STATUS_MESSAGE_OK = "OK"

# API STATUS CODE
API_STATUS_CODE_BAD_REQUEST = 400
API_STATUS_CODE_UNAUTHORIZED = 401
API_STATUS_CODE_FORBIDDEN = 403
API_STATUS_CODE_NOT_FOUND = 404
API_STATUS_CODE_SERVER_ERROR = 500
API_STATUS_CODE_OK = 200
API_STATUS_CODE_CREATED = 201

# TOKEN_DURATION
ACCESS_TOKEN_DURAION = 60 * 60
REFRESH_TOKEN_DURAION = 60 * 60 * 24 * 7

# CACHE_KEY
CACHE_KEY_REFRESH_TOKEN_MAPPING = 'refresh_token:{random_string}'

# CACHE_DURATION
CACHE_DURATION_REFRESH_TOKEN_MAPPING = 60 * 60 * 24 * 7

# TOKEN_TYPE
TOKEN_TYPE_ACCESS = 'access'
TOKEN_TYPE_REFRESH = 'refresh'

