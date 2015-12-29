from setuptools import setup, find_packages
import os


packagename = 'zenodio'
description = 'I/O with Zenodo.'
author = 'Jonathan Sick'
author_email = 'jsick@lsst.org'
license = 'MIT'
url = 'https://github.com/lsst-sqre/zenodio'
version = '0.1.1.dev0'


def read(filename):
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return open(full_filename, mode='r', encoding='utf8').read()

long_description = read('README.rst')


setup(
    name=packagename,
    version=version,
    description=description,
    long_description=long_description,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='aas',
    packages=find_packages(exclude=['docs', 'tests*', 'data', 'notebooks']),
    install_requires=['future', 'requests', 'xmltodict'],
    tests_require=['pytest'],
    # package_data={},
)
