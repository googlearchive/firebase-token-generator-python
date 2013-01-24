from distutils.core import setup

setup(
    name='firebase-token-generator',
    version='1.2',
    author='Greg Soltis',
    author_email='greg@firebase.com',
    py_modules=['firebase_token_generator'],
    license='LICENSE',
    url='https://github.com/firebase/PyFirebaseTokenGenerator',
    description='A utility to generate signed Firebase Authentication Tokens',
    long_description=open('README.md').read()
)