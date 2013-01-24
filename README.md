# PyFirebaseTokenGenerator

A Python library for generating JWT that can be used for authentication in a Firebase app.

## Installation

pip install firebase-token-generator

## Usage

Using the library to generate a valid, signed token:

    from firebase_token_generator import create_token

    SECRET = '<YOUR FIREBASE APP SECRET>'
    custom_data = {'auth_data': 'foo', 'other_auth_data': 'bar'}
    options = {'admin': True}

    token = create_token(SECRET, custom_data, options)

The options argument is an optional dictionary of additional properties for the token. The list of possible options is:

* expires - epoch time after which the token will be considered invalid
* notBefore - epoch time before which the token will be considered invalid
* admin - if set to True, this client will bypass security rules
* debug - if set to True, the client will receive information about security rule execution
* simulate - (internal-only for now) if True, Firebase will run security rules but not actually make any data changes

See the [Firebase Authentication Docs](https://www.firebase.com/docs/security/authentication.html) for more information about authentication tokens.
