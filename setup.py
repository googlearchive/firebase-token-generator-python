from distutils.core import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='firebase-token-generator',
    version='1.3.2',
    author='Greg Soltis',
    author_email='greg@firebase.com',
    zip_safe=False,
    py_modules=['firebase_token_generator'],
    license='LICENSE',
    url='https://github.com/firebase/firebase-token-generator-python',
    description='A utility to generate signed Firebase Authentication Tokens',
    long_description=read('README')
)
