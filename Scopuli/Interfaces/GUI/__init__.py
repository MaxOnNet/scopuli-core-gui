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
"""Module docstring.  """

import os
import sys
import logging

from Scopuli.Interfaces.GUI.WindowModule import Window
from Scopuli.Interfaces.GUI.WidgetModule import Widget


log = logging.getLogger(__name__)


class LogHandler(logging.Handler):
    def __init__(self, application):
        logging.Handler.__init__(self)

        self.applocation = application

    def emit(self, record):
        self.applocation.emit("log", "{} - {}".format(record.module, record.msg))


class ResourceChecker:
    def __init__(self, application):
        self.application = application
        self.configuration = self.application.config.configuration
        
        self._check_gui()

    def _check_gui(self):
        group_name = "gui"
        group_error = False
        
        for group in self.configuration.getElementsByTagName(group_name):
            for item in group.childNodes:
                if item.nodeType == 1:
                    for attr in ["glade", "image-splash", "image-logo"]:
                        if item.hasAttribute(attr):
                            attr_value = self.application.config.get(group_name, item.nodeName, attr, "")
                            
                            if not os.path.isfile(attr_value):
                                group_error = True
                                log.critical("Ошибка конфигурации, файл {} не найден, проблема в группе {}, элемент {}, аттрибут {}".format(attr_value, group_name, item.nodeName, attr))
                                
        if group_error:
            sys.exit(1)
