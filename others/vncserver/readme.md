# vncserver
* /usr/lib/systemd/system/vncserver.service

# modify /root/.vnc/xstartup

remove script below
```shell
if [ -e /usr/bin/gnome-session -o -e /usr/bin/startkde ]; then
    vncserver -kill $DISPLAY
fi
```
