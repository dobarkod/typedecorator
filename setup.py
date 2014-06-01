#!/usr/bin/env python
# Copyright (C) 2014. Senko Rasic <senko.rasic@goodcode.io>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys

from setuptools import setup, find_packages, Command

from typedecorator import __version__


class BaseCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class TestCommand(BaseCommand):

    description = "run self-tests"

    def run(self):
        ret = os.system('%s tests.py' % sys.executable)
        if ret != 0:
            sys.exit(-1)


class CoverageCommand(BaseCommand):
    description = "run self-tests and report coverage (requires coverage.py)"

    def run(self):
        r = os.system('coverage run --source=typedecorator tests.py')
        if r != 0:
            sys.exit(-1)
        os.system('coverage html')


setup(
    name='typedecorator',
    version=__version__,
    author='Senko Rasic',
    author_email='senko.rasic@goodcode.io',
    description='Decorator-based type checking library for Python 2 and 3',
    license='MIT',
    url='https://github.com/dobarkod/typedecorator/',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    cmdclass={
        'test': TestCommand,
        'coverage': CoverageCommand
    }
)
