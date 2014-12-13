try:
    basestring
except NameError:  # Python 3
    basestring = str
from array import array
from base64 import urlsafe_b64encode
import hashlib
import hmac
import sys
try:
    import json
except ImportError:
    import simplejson as json
import calendar
import time
import datetime

__all__ = ['create_token']

TOKEN_VERSION = 0
TOKEN_SEP = '.'

CLAIMS_MAP = {
    'expires': 'exp',
    'notBefore': 'nbf',
    'admin': 'admin',
    'debug': 'debug',
    'simulate': 'simulate'
}

def create_token(secret, data, options=None):
    """
    Generates a secure authentication token.
 
    Our token format follows the JSON Web Token (JWT) standard:
    header.claims.signature
  
    Where:
    1) "header" is a stringified, base64-encoded JSON object containing version and algorithm information.
    2) "claims" is a stringified, base64-encoded JSON object containing a set of claims:
      Library-generated claims:
      "iat" -> The issued at time in seconds since the epoch as a number
      "d" -> The arbitrary JSON object supplied by the user.
      User-supplied claims (these are all optional):
      "exp" (optional) -> The expiration time of this token, as a number of seconds since the epoch.
      "nbf" (optional) -> The "not before" time before which the token should be rejected (seconds since the epoch)
      "admin" (optional) -> If set to true, this client will bypass all security rules (use this to authenticate servers)
      "debug" (optional) -> "set to true to make this client receive debug information about security rule execution.
      "simulate" (optional, internal-only for now) -> Set to true to neuter all API operations (listens / puts
                 will run security rules but not actually write or return data).
    3) A signature that proves the validity of this token (see: http://tools.ietf.org/html/draft-ietf-jose-json-web-signature-07)
  
    For base64-encoding we use URL-safe base64 encoding. This ensures that the entire token is URL-safe
    and could, for instance, be placed as a query argument without any encoding (and this is what the JWT spec requires).
  
    Args:
        secret - the Firebase Application secret
        data - a json serializable object of data to be included in the token
        options - An optional dictionary of additional claims for the token. Possible keys include:
            a) "expires" -- A datetime or timestamp (as a number of seconds since the epoch) denoting a time after
                            which this token should no longer be valid.
            b) "notBefore" -- A datetime or timestamp (as a number of seconds since the epoch) denoting a time before
                            which this token should be rejected by the server.
            c) "admin" -- Set to true to bypass all security rules (use this for your trusted servers).
            d) "debug" -- Set to true to enable debug mode (so you can see the results of Rules API operations)
            e) "simulate" -- (internal-only for now) Set to true to neuter all API operations (listens / puts
                            will run security rules but not actually write or return data)
    Returns:
        A signed Firebase Authentication Token
    Raises:
        ValueError: if an invalid key is specified in options

    """
    if not isinstance(secret, basestring):
        raise ValueError("firebase_token_generator.create_token: secret must be a string.")
    if not options and not data:
        raise ValueError("firebase_token_generator.create_token: data is empty and no options are set.  This token will have no effect on Firebase.");
    if not options:
        options = {}
    is_admin_token = ('admin' in options and options['admin'] == True)
    _validate_data(data, is_admin_token)
    claims = _create_options_claims(options)
    claims['v'] = TOKEN_VERSION
    claims['iat'] = int(time.time())
    claims['d'] = data

    token = _encode_token(secret, claims)
    if len(token) > 1024:
        raise RuntimeError("firebase_token_generator.create_token: generated token is too long.")
    return token

def _validate_data(data, is_admin_token):
    if data is not None and not isinstance(data, dict):
        raise ValueError("firebase_token_generator.create_token: data must be a dictionary")
    contains_uid = (data is not None and 'uid' in data)
    if ((not contains_uid and not is_admin_token) or (contains_uid and not isinstance(data['uid'], basestring))):
        raise ValueError("firebase_token_generator.create_token: data must contain a \"uid\" key that must be a string.")
    if (contains_uid and (len(data['uid']) > 256)):
        raise ValueError("firebase_token_generator.create_token: data must contain a \"uid\" key that must not be longer than 256 bytes.")

def _create_options_claims(opts):
    claims = {}
    for k in opts:
        if (isinstance(opts[k], datetime.datetime)):
            opts[k] = int(calendar.timegm(opts[k].utctimetuple()))
        if k in CLAIMS_MAP:
            claims[CLAIMS_MAP[k]] = opts[k]
        else:
            raise ValueError('Unrecognized Option: %s' % k)
    return claims

if sys.version_info < (2, 7):
    def _encode(bytes_data):
        # Python 2.6 has problems with bytearrays in b64
        encoded = urlsafe_b64encode(bytes(bytes_data))
        return encoded.decode('utf-8').replace('=', '')
else:
    def _encode(bytes):
        encoded = urlsafe_b64encode(bytes)
        return encoded.decode('utf-8').replace('=', '')


def _encode_json(obj):
    return _encode(bytearray(json.dumps(obj, separators=(',',':')), 'utf-8'))

def _sign(secret, to_sign):
    def portable_bytes(s):
        try:
            return bytes(s, 'utf-8')
        except TypeError:
            return bytes(s)
    return _encode(hmac.new(portable_bytes(secret), portable_bytes(to_sign), hashlib.sha256).digest())

def _encode_token(secret, claims):
    encoded_header = _encode_json({'typ': 'JWT', 'alg': 'HS256'})
    encoded_claims = _encode_json(claims)
    secure_bits = '%s%s%s' % (encoded_header, TOKEN_SEP, encoded_claims)
    sig = _sign(secret, secure_bits)
    return '%s%s%s' % (secure_bits, TOKEN_SEP, sig)
