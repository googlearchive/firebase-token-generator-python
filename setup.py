from distutils.core import setup

setup(
    name='firebase-token-generator',
    version='1.3',
    author='Greg Soltis',
    author_email='greg@firebase.com',
    zip_safe=False,
    py_modules=['firebase_token_generator'],
    license='LICENSE',
    url='https://github.com/firebase/firebase-token-generator-python',
    description='A utility to generate signed Firebase Authentication Tokens',
    long_description=open('README.md').read()
)