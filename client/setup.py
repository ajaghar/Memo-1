#!/usr/bin/env python
import os

from setuptools import setup


__doc__ = 'see https://github.com/amirouche/Memo'


setup(
    name='memo-client',
    version='0.1',
    url='https://github.com/amirouche/Memo',
    license='LGPL',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    description='Memo is a Redis clone wanna be in Python',
    long_description=__doc__,
    packages=['memo_client'],
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
)
