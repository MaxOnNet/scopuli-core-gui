#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright [2018] Tatarnikov Viktor [viktor@tatarnikov.org]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" """

from setuptools import setup, find_packages
from os.path import join, dirname
from datetime import datetime

now = datetime.now()

setup(
    name='scopuli_core_gui',
    author='Viktor Tatarnikov',
    author_email='viktor@tatarnikov.org',
    namespace_packages=['Scopuli'],
    platforms='any',
    zip_safe=False,
    version='0.1.{0}.{1}.{2}.{3}.{4}'.format(now.year, now.month, now.day, now.hour, now.minute),
    license="Apache",
    url="https://scopuli.tatarnikov.org",
    packages=find_packages(exclude=["tests"]),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True
)