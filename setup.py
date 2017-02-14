from setuptools import find_packages, setup
from neko import __version__ as version

author = 'Daning Su'
author_email = 'sudaning@sina.com'
description = "A pure Python library designed to make it easy and quick to code for Neko"

with open('README.rst') as f:
    long_description = f.read()

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
url = 'https://github.com/sudaning/PytLab-Neko'
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
	maintainer=author,
	name=name,
	packages=find_packages(),
	platforms=platforms,
	url=url,
	download_url=download_url,
	version=version,
	classifiers=classifiers,
)

