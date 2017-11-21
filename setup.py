VERSION = '1.1'
DESCRIPTION = 'show module internals and corresponding class internals in tree format'

# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Python Software Foundation License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development',
]

if __name__ == '__main__':
    try:
        from setuptools import setup, find_packages
        from codecs import open
        from os import path
    except ImportError:
        from distutils.core import setup

    with open('README.rst', 'r') as f:
        readme = f.read()

setup(
  name = 'inspectshow',
  packages_dir = {'inspectshow': ' '},
  packages = ['inspectshow'],
  version = VERSION,
  description = DESCRIPTION,
  long_description=readme,
  author = 'Vadivel',
  author_email = 'vadivelmurugank@gmail.com',
  url = 'https://github.com/vadivelmurugank/inspectshow',
  license = 'MIT',
  classifiers=classifiers,
  keywords='inspect show tree',
)
