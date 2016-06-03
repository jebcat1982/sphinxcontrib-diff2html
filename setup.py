# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='sphinxcontrib-diff2html',
    description='Diff2html for Sphinx',
    version='0.0.1',
    author='tsgkadot',
    author_email='tsgkadot@gmail.com',
    install_requires=['sphinx'],
    platforms='any',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url="https://github.com/tsgkdt/sphinx-git",
    namespace_packages=['sphinxcontrib'],
)
