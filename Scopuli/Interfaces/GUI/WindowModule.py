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

import gi
import os
import sys
import logging


gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
log = logging.getLogger(__name__)


from gi.repository import GObject, Gdk, Gtk, GdkPixbuf
from importlib import import_module


class Window(object):
    def __init__(self, application, application_frame=None):
        self.application = application
        self.application_frame = application_frame
        
        self._init_builder()
    
    
    def _init_builder(self):
        self.builder_python = bool(int(self.application.config.get("gui", "", "gtk_build_python", "0")))
        self.builder_glade = self.application.config.get("gui", self.__class__.__name__, "glade", "")
        
        if os.path.isfile(self.builder_glade):
            self.builder = Gtk.Builder()
            self.builder.add_from_file(self.builder_glade)
            
            self.window = self.builder.get_object("window{0}".format(self.__class__.__name__))
            
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
                            log.debug("Внедряем в класс, элемент {0} с именем {1}.".format(gui_object_name, gui_object_element_id))
                        else:
                            log.debug("Пропускаем элемент {0} с именем {1}.".format(gui_object_name, gui_object_element_id))
    
                    if gui_object_name in ("Image"):
                        self._init_builder_image_stock(gui_object)
                        
                    if gui_object_name in ("Alignment"):
                        if gui_object_element_id != "" and len(gui_object_element_id.split("_")) > 1:
                            if gui_object_element_id.split("_")[0] == "widget":
                                log.debug("Найден виджет {0}.".format(gui_object_element_id.split("_")[1]))
                                self._init_builder_widget(gui_object, gui_object_element_id)

        else:
            log.critical("Фаил интерфейса не найден по пути {0}".format(self.builder_glade))
            log.critical("Замершаем работу.")
            
            sys.exit(1)
            
            
    def _init_builder_events(self):
        pass
    
    
    def _init_builder_widget(self, gui_object, gui_object_element_id):
        widget_name = gui_object_element_id.split("_")[1]
        widget_module = "Scopuli.GUI.Widgets".format(widget_name)
        widget = getattr(import_module(widget_module), widget_name)
        
        if widget:
            try:
                log.debug("Иициализируем виджет {0}".format(widget_name))
                gui_object.add(widget(self.application, self.application_frame).widget)
            except Exception as e:
                log.error("Ошибка инициализации виджета с именем {0}. MSG:{1}".format(widget_name, str(e)))


    def _init_builder_image_stock(self, gui_object):
        if gui_object.__class__.__name__ in ("Image"):
            if gui_object.get_property("storage-type") is Gtk.ImageType.STOCK:
                if gui_object.get_property("stock") != "":
                    gui_object_file = self.application.config.get("gui", self.__class__.__name__,
                                                                  "image_{0}".format(gui_object.get_property("stock")), "None")
                    
                    gui_object_width = gui_object.get_property("width-request")
                    gui_object_height = gui_object.get_property("height-request")
                    
                    if gui_object_width == -1:
                        gui_object_width = 16
                    
                    if gui_object_height == -1:
                        gui_object_height = 16
                    
                    if os.path.isfile(gui_object_file):
                        gui_object_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(gui_object_file, width=gui_object_width, height=gui_object_height, preserve_aspect_ratio=False)
                        gui_object.set_from_pixbuf(gui_object_pixbuf)
    
    
    def move(self, window_parent):
        x, y = window_parent.get_position()
        self.window.move((x + 64), (y + 64))
