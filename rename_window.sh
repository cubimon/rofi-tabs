#!/usr/bin/zsh

new_name=`echo -e "\c" | rofi -dmenu`
if [ -z "${new_name}" ]; then
	exit
fi
xdotool set_window --name "${new_name}" `xdotool getactivewindow`

