from Xlib import X
from Xlib.display import Display
from Xlib.protocol.event import ClientMessage

# xorg
display = Display()
screen = display.screen()
xorg_root_window = screen.root
NET_WM_PID = display.intern_atom('_NET_WM_PID')
NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')

def find_window_by_pid(pid, window=xorg_root_window):
    todo = window.query_tree()._data['children']
    while len(todo) != 0:
        child_window = todo.pop()
        if NET_WM_PID in child_window.list_properties():
            window_pid = child_window.get_property(NET_WM_PID, 0, 0, 4).value[0]
            if window_pid == pid:
                return child_window
        todo.extend(child_window.query_tree()._data['children'])

def find_windows_by_name(name, window=xorg_root_window):
    todo = window.query_tree()._data['children']
    result = []
    while len(todo) != 0:
        child_window = todo.pop()
        if NET_WM_PID in child_window.list_properties():
            window_pid = child_window.get_property(NET_WM_PID, 0, 0, 4).value[0]
            window_name = child_window.get_wm_name()
            if window_name and name in window_name:
                result.append(child_window)
        todo.extend(child_window.query_tree()._data['children'])
    return result

def focus_window(window):
    message = ClientMessage(
            window=window,
            client_type=NET_ACTIVE_WINDOW,
            data=(32, (2, 0, 0, 0, 0)))
    xorg_root_window.send_event(message,
            event_mask=X.SubstructureNotifyMask | X.SubstructureRedirectMask)
    display.sync()

