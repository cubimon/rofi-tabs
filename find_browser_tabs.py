#!/usr/bin/python
import json
import subprocess
import sys

import dbus
import i3ipc

# i3
i3 = i3ipc.Connection()
root = i3.get_tree()

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
tabs.values()
tab_descriptions = [
        str(tab_id) + ' - ' + tab_name 
        for tab_id, tab_name in tabs.items()]

# get selected tab from rofi
p = subprocess.Popen(['rofi', '-dmenu'],
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate(
        input='\n'.join(tab_descriptions).encode('utf-8'))
selection = stdout.decode('utf-8')
if '-' not in selection:
    sys.exit(1)
tabId = selection[:selection.index('-') - 1]
if not tabId.isdigit():
    sys.exit(2)
tabId = int(tabId)

# active tab
activate(tabId)

# focus window
# TODO: find right firefox window for firefox browser tab
root.find_named('Firefox')[0].command('focus')

