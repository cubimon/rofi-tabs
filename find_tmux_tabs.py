#!/usr/bin/python
import json
import subprocess
import sys
import psutil

import i3ipc
import libtmux
from Xlib.display import Display
from operator import attrgetter

def get_tmux_pids():
    result = []
    for procinfo in psutil.process_iter(['pid', 'name']):
        if procinfo.name() == 'tmux: client':
            result.append(procinfo.pid)
    return result

def get_parent_terminal_process(pid):
    process = psutil.Process(pid)
    while process.name() != 'konsole':
        process = psutil.Process(process.ppid())
    return process

def pid_to_window_id(pid, window):
    todo = window.query_tree()._data['children']
    while len(todo) != 0:
        child_window = todo.pop()
        if pid_property in child_window.list_properties():
            window_pid = child_window.get_property(pid_property, 0, 0, 4).value[0]
            if window_pid == pid:
                return child_window.id
        todo.extend(child_window.query_tree()._data['children'])

def window_id_to_i3_node(window_id, node):
    todo = node.nodes
    while len(todo) != 0:
        child_node = todo.pop()
        if child_node.window == window_id:
            return child_node
        todo.extend(child_node.nodes)

# get tmux session pids
p = subprocess.Popen(['tmux', 'list-clients', '-F', '#{session_name};#{client_pid}'],
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
stdout = stdout.decode('utf-8').split('\n')[:-1]
tmux_sessions = {}
for line in stdout:
    session_name, pid = line.split(';')
    tmux_sessions[session_name] = int(pid)

# xorg
display = Display()
screen = display.screen()
xorg_root_window = screen.root
pid_property = display.intern_atom('_NET_WM_PID')

# i3
i3 = i3ipc.Connection()
i3_root_node = i3.get_tree()

# tmux
server = libtmux.Server()

# get tabs
tab_descriptions = []
for session in server.sessions:
    for window in session.windows:
        tab_descriptions.append(session.name + ' - ' + window.name)

# get selected tab from rofi
p = subprocess.Popen(['rofi', '-dmenu'],
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate(
        input='\n'.join(tab_descriptions).encode('utf-8'))
selection = stdout.decode('utf-8').split('\n')[0]

# focus selected tab + window
for session in server.sessions:
    for window in session.windows:
        if selection == session.name + ' - ' + window.name:
            window.select_window()
            tmux_pid = tmux_sessions[session.name]
            terminal_process = get_parent_terminal_process(tmux_pid)
            window_id = pid_to_window_id(terminal_process.pid, xorg_root_window)
            i3_window_node = window_id_to_i3_node(window_id, i3_root_node)
            i3_window_node.command('focus')

