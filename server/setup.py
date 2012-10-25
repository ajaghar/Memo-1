#!/usr/bin/env python
import os

from setuptools import setup


def long_description():
    path = os.path.dirname(__file__)
    path = os.path.join(path, 'README.rst')
    try:
        with open(path) as f:
            return f.read()
    except:
        return ''


__doc__ = 'see https://github.com/amirouche/Memo'


setup(
    name='memo',
    version='0.3.1',
    url='https://github.com/amirouche/Memo',
    license='AGPL',
    author='Amirouche Boubekki',
    author_email='amirouche.boubekki@gmail.com',
    description='Memo is a Redis clone wanna be in Python',
    long_description=__doc__,
    packages=['memo', 'memo.structures'],
    install_requires=['setproctitle'],
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
)
