#!/usr/bin/python
import json
import sys

import dbus
import rofi

from general import *

# dbus
bus = dbus.SessionBus()

browser_tabs_object = bus.get_object(
        'org.cubimon.BrowserTabs', '/org/cubimon/BrowserTabs')
browser_tabs_interface = dbus.Interface(
        browser_tabs_object, dbus_interface='org.cubimon.BrowserTabs')

get_tabs = browser_tabs_interface.get_dbus_method('tabs')
activate = browser_tabs_interface.get_dbus_method('activate')

# get tabs
tabs = get_tabs()
tabs = json.loads(tabs)
tab_ids = list(tabs.keys())
tab_descriptions = [
        str(tab_id) + ' - ' + tab_name 
        for tab_id, tab_name in tabs.items()]

# get selected tab from rofi
r = rofi.Rofi()
index, _ = r.select('Select tab to focus', tab_descriptions)
if index < 0:
    sys.exit(0)
tab_id = tab_ids[index]

# active tab
activate(tab_id)

# focus window
# TODO: find right firefox window for firefox browser tab
windows = find_windows_by_name('Firefox')
for window in windows:
    if window.get_wm_class():
        focus_window(window)

