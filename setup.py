from setuptools import find_packages, setup
from neko import __version__ as version

author = 'Daning Su'
author_email = 'sudaning@sina.com'
description = "A pure Python library designed to make it easy and quick to code for Neko"

long_description = '''
=====
Neko
=====
Introduction
------------
pyNeko is a pure Python library designed to making magic to code for Neko.
You can use pyNeko to making magic beautiful.
In `/scripts <https://github.com/sudaning/PytLab-Neko/tree/master/scripts>`_ , there are some scripts written by me for daily use.
Installation
------------
1. Via pip(recommend)::
	pip install pyNeko
2. Via easy_install::
	easy_install pyNeko
3. From source::
	python setup.py install
'''

install_requires = [
	'python-esl>=1.4.18',
	'pycrypto>=2.6.1',
	'paramiko>=2.1.1',
	'redis>=2.10.5',
]

license = 'LICENSE'

name = 'pyNeko'
packages = [
	'neko',
]
platforms = ['linux']
url = 'https://github.com/sudaning/PytLab-Neko'
download_url = ''
classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Science/Research',
	'Natural Language :: English',
	'Topic :: Text Processing',
	'Operating System :: POSIX :: Linux',
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.7',
]

setup(author=author,
	author_email=author_email,
	description=description,
	license=license,
	long_description=long_description,
	install_requires=install_requires,
	maintainer=author,
	name=name,
	packages=find_packages(),
	platforms=platforms,
	url=url,
	download_url=download_url,
	version=version,
	classifiers=classifiers,
)

