#!/usr/bin/python
import json
import subprocess
import sys
import psutil

import libtmux

from general import *

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

# get tmux session pids
p = subprocess.Popen(['tmux', 'list-clients', '-F', '#{session_name};#{client_pid}'],
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
stdout = stdout.decode('utf-8').split('\n')[:-1]
tmux_sessions = {}
for line in stdout:
    session_name, pid = line.split(';')
    tmux_sessions[session_name] = int(pid)

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
            window = find_window_by_pid(terminal_process.pid)
            focus_window(window)

