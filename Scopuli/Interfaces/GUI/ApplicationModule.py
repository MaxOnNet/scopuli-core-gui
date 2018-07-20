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
import sys
import os
import threading
import logging
import logging.handlers
import time


gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
log = logging.getLogger(__name__)


from gi.repository import GObject, Gdk, Gtk, Gio

from Scopuli.Interfaces.Config import Config

import Scopuli.Interfaces.GUI as IGUI


class Application(Gtk.Application):
    __gsignals__ = {
        'login'        : (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'logout'       : (GObject.SIGNAL_RUN_FIRST, None, ()),
        
        'log'          : (GObject.SIGNAL_RUN_FIRST, None, (str,))
    }
    
    
    def __init__(self):
        Gtk.Application.__init__(self, flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        
        self.config = Config(path="./config.xml")
        self.database = None
        self.session = None
        
        self.windowMain = None
        self.windowSplash = None
        
        self._logging_init()
        self._check_gui()
    
    
    def _logging_init(self):
        threading.current_thread().name = 'main'
        
        logging.basicConfig(level=int(self.config.get("logging", "console", "level", "10")), stream=sys.stdout,
                            format='%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s')
        
        log_handler_gui = IGUI.LogHandler(self)
        log_handler_gui.setLevel(int(self.config.get("logging", "splash", "level", "20")))
        
        log_handler_console = logging.StreamHandler()
        log_handler_console.setLevel(int(self.config.get("logging", "console", "level", "10")))
        log_handler_console.setFormatter(
            logging.Formatter('%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s'))
        
        if bool(int(self.config.get("logging", "", "use_file", "0"))):
            log_handler_file = logging.handlers.TimedRotatingFileHandler(self.config.get("logging", "file", "path", "4gain.log"),
                                                                         when=self.config.get("logging", "file", "when", "d"),
                                                                         interval=int(self.config.get("logging", "file", "interval", "1")),
                                                                         backupCount=int(self.config.get("logging", "file", "count", "1")))
            log_handler_file.setLevel(int(self.config.get("logging", "file", "level", "10")))
            log_handler_file.setFormatter(logging.Formatter(
                '%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s'))
            
            logging.getLogger('').addHandler(log_handler_file)
        
        if bool(int(self.config.get("logging", "", "use_syslog", "0"))):
            log_handler_syslog = logging.handlers.SysLogHandler(address=(self.config.get("logging", "syslog", "address_ip", "127.0.0.1"),
                                                                         int(self.config.get("logging", "syslog", "address_port", "514"))))
            log_handler_syslog.setLevel(int(self.config.get("logging", "file", "level", "10")))
            log_handler_syslog.setFormatter(logging.Formatter(
                    '%(asctime)s [%(module)15s] [%(funcName)19s] [%(lineno)4d] [%(levelname)7s] [%(threadName)4s] %(message)s'))
            
            logging.getLogger('').addHandler(log_handler_syslog)
        
        logging.getLogger('').addHandler(log_handler_gui)
        # logging.getLogger('').addHandler(log_handler_console)
    
    
    def _check_gui(self):
        if int(self.config.get("gui", "", "gtk-major", "0")) == int(Gtk.get_major_version()) \
                and int(self.config.get("gui", "", "gtk-minor", "0")) == int(Gtk.get_minor_version()) \
                and int(self.config.get("gui", "", "gtk-micro", "0")) == int(Gtk.get_micro_version()):
            log.debug("Рабочая версия GTK.")
            
            IGUI.ResourceChecker(self)
            
            return
        
        log.critical("Warning: GTK version mistmatch!")
        log.critical(
            "Current GTK version is: {0}.{1}.{2}".format(Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))
        log.critical("Need GTK version is: {0}.{1}.{2}".format(self.config.get("gui", "", "gtk-major", "0"),
                                                               self.config.get("gui", "", "gtk-minor", "0"),
                                                               self.config.get("gui", "", "gtk-micro", "0")))
        
        self.quit()
    
    
    def _database_init(self):
        raise Exception("Не реализовано")
    
    
    def _database_close(self):
        raise Exception("Не реализовано")
    

    def _splash_load(self, application_onload=True):
        if bool(int(self.config.get("gui", "", "use_splash", "0"))):
            if self.windowSplash is not None:
                self.add_window(self.windowSplash.window)
    
    
    def _splash_unload(self):
        if bool(int(self.config.get("gui", "", "use_splash", "0"))):
            if self.windowSplash is not None:
                self.windowSplash.window.hide()
                self.remove_window(self.windowSplash.window)
    
    
    def _session_init(self):
        raise Exception("Не реализовано")
    
    
    def _session_close(self):
        raise Exception("Не реализовано")
    
    def _synchronizers_init(self):
        raise Exception("Не реализовано")
    
    def _synchronizers_run(self):
        raise Exception("Не реализовано")
    
    def _synchronizers_stop(self):
        raise Exception("Не реализовано")
    
    def _main_prepare(self):
        self._database_init()
        self._session_init()
        self._synchronizers_init()
        self._synchronizers_run()
    
    
    def _main_load(self):
        log.info("Загрузка основного окна")
        if self.windowMain is not None:
            self.windowMain.window.connect('delete-event', self._main_destroy)
            
            self.add_window(self.windowMain.window)
            self.windowMain.window.present()
        else:
            log.critical("Main Window не предопределен")
            self._main_unload()
    
    def _main_destroy(self, widget, args):
        log.info("Выгрузка основного окна")

        if self.windowMain is not None:
            self.windowMain.window.hide()
            self.remove_window(self.windowMain.window)
        
        if bool(int(self.config.get("gui", "", "use_splash", "0"))):
            self._splash_load(application_onload=False)
        else:
            self._main_unload()
    
    
    def _main_unload(self):
        self._synchronizers_stop()
        self._session_close()
        self._database_close()
        
        self.quit()
    
    
    def do_startup(self):
        log.debug("Application do_startup")
        Gtk.Application.do_startup(self)
    
    
    def do_activate(self):
        log.debug("Application do_activete")
        
        Gtk.Application.do_activate(self)
        
        if bool(int(self.config.get("gui", "", "use_splash", "0"))):
            self._splash_load()
        else:
            self._main_prepare()
            self._main_load()
    
    
    def do_run_mainloop(self):
        Gtk.Application.do_run_mainloop(self)
    
    
    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        
        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")
        
        self.activate()
        
        return 0
    
    
    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()
    
    
    def on_quit(self, action, param):
        log.info("Завершение приложения")
        
        self.quit()
