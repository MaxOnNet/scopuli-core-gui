#!/usr/bin/env bash
cd ../
../scopuli-environment/bin/pip uninstall scopuli-core-gui  -y
../scopuli-environment/bin/python3.7 setup.py install
