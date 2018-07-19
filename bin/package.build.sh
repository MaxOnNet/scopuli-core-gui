#!/usr/bin/env bash
cd ../
../scopuli-environment/bin/python3.7 setup.py bdist_wheel
../scopuli-environment/bin/python3.7 setup.py sdist
