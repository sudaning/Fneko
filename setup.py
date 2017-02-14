from setuptools import setup, find_packages

from neko import __version__ as version

maintainer = 'Daning Su'
maintainer_email = 'sudaning@sina.com'
author = maintainer
author_email = maintainer_email
description = "A pure Python library designed to make it easy and quick to code for Neko"

long_description = """
=====
Neko
=====
.. image:: https://travis-ci.org/PytLab/VASPy.svg?branch=master
    :target: https://travis-ci.org/PytLab/VASPy
    :alt: Build Status
.. image:: https://img.shields.io/badge/python-3.5-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform
.. image:: https://img.shields.io/badge/python-2.7-green.svg
    :target: https://www.python.org/downloads/release/python-2710
    :alt: platform
.. image:: https://img.shields.io/github/stars/PytLab/VASPy.svg
    :target: https://github.com/PytLab/VASPy/stargazers
.. image:: https://img.shields.io/github/forks/PytLab/VASPy.svg
    :target: https://github.com/PytLab/VASPy/network
Introduction
------------
pyNeko is a pure Python library designed to making magic to code for Neko.
You can use pyNeko to making magic beautiful.
In `/scripts <https://github.com/PytLab/VASPy/tree/master/scripts>`_ , there are some scripts written by me for daily use.
Installation
------------
1. Via pip(recommend)::
    pip install pyNeko
2. Via easy_install::
    easy_install pyNeko
3. From source::
    python setup.py install
"""

install_requires = [
    #'numpy>=1.11.1',
    #'matplotlib>=1.5.2',
    #'scipy>=0.18.0',
]

license = 'LICENSE'

name = 'pyNeko'
packages = [
    'neko',
]
platforms = ['linux']
url = 'https://github.com/PytLab/VASPy'
download_url = ''
classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

setup(author=author,
      author_email=author_email,
      description=description,
      license=license,
      long_description=long_description,
      install_requires=install_requires,
      maintainer=maintainer,
      name=name,
      packages=find_packages(),
      platforms=platforms,
      url=url,
      download_url=download_url,
      version=version,
#      test_suite="tests",
      classifiers=classifiers)

