#!/usr/bin/python
import json
import dbus
import subprocess
import sys

# dbus stuff
bus = dbus.SessionBus()

browser_tabs_object = bus.get_object(
        'org.cubimon.BrowserTabs', '/org/cubimon/BrowserTabs')
browser_tabs_interface = dbus.Interface(
        browser_tabs_object, dbus_interface='org.cubimon.BrowserTabs')

get_active_tab_id = browser_tabs_interface.get_dbus_method('activeTabId')
rename = browser_tabs_interface.get_dbus_method('rename')

# get new name from rofi
p = subprocess.Popen(['rofi', '-dmenu'],
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
new_name = stdout.decode('utf-8')

# rename
rename(int(get_active_tab_id()), new_name.split('\n')[0])

