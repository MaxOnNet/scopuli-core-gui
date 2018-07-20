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

import os
import gi
import logging


gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
log = logging.getLogger(__name__)


from gi.repository import GObject, Gdk, Gtk


class Widget(object):
    _init_widget = True
    
    def __init__(self, application, application_frame):
        self.application = application
        self.application_frame = application_frame
        
        # Ускорители
        self.config = self.application.config
        self.session = self.application.session
        self.database = self.application.database
        
        if self._check_structure():
            self._init_builder()
            self._init_attributes()


    def _check_structure(self):
        for attribute in ["_widget_name", "_widget_attributes", "_widget_functions", "_widget_signals"]:
            if not hasattr(self, attribute):
                log.error("Ошибка загрузки виджета, отсутствует аттрибут: {}, в дочернем инстансе.".format(attribute))
                return False

        return True
    
    def _init_builder(self):
        self.builder_glade = self.config.get("gui", self.__class__.__name__, "glade", "")
    
        if os.path.isfile(self.builder_glade):
            self.builder = Gtk.Builder()
            self.builder.add_from_file(self.builder_glade)
    
            self.widget = self.builder.get_object("widget{0}".format(self.__class__.__name__))
    
            for gui_object in self.builder.get_objects():
                gui_object_name = gui_object.__class__.__name__
                gui_object_element_name = ""
                gui_object_element_id = ""
    
                try:
                    if issubclass(type(gui_object), Gtk.Buildable):
                        gui_object_element_id = Gtk.Buildable.get_name(gui_object)
                except TypeError:
                    pass
                finally:
                    if gui_object_name in ("Entry", "Label", "Button", "TreeView", "Box", "ScrolledWindow", "CheckButton", "TextView", "Image"):
                        if gui_object_element_id != "" and len(gui_object_element_id.split("_")) > 1:
                            setattr(self, gui_object_element_id, gui_object)
                            log.debug("Внедряем в клсасс, элемент {0} с именем {1}".format(gui_object_name, gui_object_element_id))
                    else:
                        log.debug("Пропускаем элемент {0} с именем {1}".format(gui_object_name, gui_object_element_id))
        else:
            log.critical("Фаил интерфейса не найден по пути {0}".format(self.builder_glade))
            self._init_widget = False

    
    def _init_attributes(self):
        for attribute in self._widget_attributes:
            if hasattr(self.application_frame, attribute):
                setattr(self, attribute, getattr(self.application_frame, attribute))
            else:
                log.error("Ошибка загрузки виджета, отсутствует аттрибут: {}, в родительском инстансе.".format(attribute))
                self._init_widget = False
 