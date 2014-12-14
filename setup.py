from distutils.core import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='firebase-token-generator',
    version='2.0.1',
    author='Firebase',
    author_email='support@firebase.com',
    zip_safe=False,
    py_modules=['firebase_token_generator'],
    license='LICENSE',
    url='https://github.com/firebase/firebase-token-generator-python',
    description='A utility to generate signed Firebase Authentication Tokens',
    classifiers=[
       'Programming Language :: Python',
       'Programming Language :: Python :: 2',
       'Programming Language :: Python :: 3',
    ],
    long_description=read('README')
)
