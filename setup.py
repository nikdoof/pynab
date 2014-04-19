from __future__ import print_function
from setuptools import setup
import io
import os

import pynab

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')


setup(
    name='pynab',
    version=pynab.__version__,
    url='http://github.com/nikdoof/pynab/',
    license='BSD',
    author='Andrew Williams',
    author_email='andy@tensixtyone.com',
    description='YNAB4 budget parser for Python',
    long_description=long_description,
    packages=['pynab'],
    platforms='any',
    classifiers = [
        'Programming Language :: Python',
        'rogramming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'icense :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    test_suite='pynab.tests',
)