# XRDP

## Install
```sh
sudo apt install xrdp
```

## Multiple Connection
In Deban based distribution, you could not connect to xRDP if the same user is logged in to the machine's graphical console ([_Error "Could not acquire name on session bus"_); cause is that dbus-user-session surrently doesn't support multiple graphical sessions per user.
You can fix it in this way:
```sh
sudo apt remove dbus-user-session
sudo apt install dbus-x11
``` 
More details [here](https://github.com/neutrinolabs/xrdp/wiki/Debian-dbus-user-session-package)

## NetworkManager 
To avoid polkit asking admin password for every action:

in file 
```sh
/etc/NetworkManager/NetworkManager.conf
``` 
add line
```sh
auth-polkit=false 
```
restart NetworkManager
```sh
sudo systemctl restart NetworkManager
```
