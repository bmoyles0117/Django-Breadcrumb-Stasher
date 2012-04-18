#!/usr/bin/env python

from setuptools import setup

setup(
    name='Breadcrumb Stasher',
    version='1.0',
    description='A helpful django plugin to store server-side breadcrumbs to redirect back to later.',
    author='Bryan Moyles',
    author_email='bmoy117@gmail.com',
    url='http://www.bryanmoyles.com/',
    packages=['breadcrumb_stasher'],
    install_requires=['django']
)