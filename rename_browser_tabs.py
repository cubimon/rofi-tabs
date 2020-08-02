#!/usr/bin/python
import dbus
import rofi

# dbus stuff
bus = dbus.SessionBus()

browser_tabs_object = bus.get_object(
        'org.cubimon.BrowserTabs', '/org/cubimon/BrowserTabs')
browser_tabs_interface = dbus.Interface(
        browser_tabs_object, dbus_interface='org.cubimon.BrowserTabs')

get_active_tab_id = browser_tabs_interface.get_dbus_method('activeTabId')
rename = browser_tabs_interface.get_dbus_method('rename')

# get new name from rofi
r = rofi.Rofi()
new_name = r.text_entry('Enter new Browser tab name')

# rename
rename(int(get_active_tab_id()), new_name)

