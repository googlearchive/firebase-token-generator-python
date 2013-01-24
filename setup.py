from distutils.core import setup

setup(
    name='FirebaseAuthTokenGenerator',
    version='1.0',
    author='Greg Soltis',
    author_email='greg@firebase.com',
    packages=['firebase_token_generator'],
    license='LICENSE',
    description='A utility to generate signed Firebase Authentication Tokens',
    long_description=open('README.md').read()
)