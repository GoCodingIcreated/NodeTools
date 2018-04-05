#!/bin/bash

source $1

function package_exists {
    dpkg -l "$1" &> /dev/null
    return $?
}

if  ! package_exists dante-server ; then
    echo "Abort : dante-server isn't installed"
    exit 1
fi



rm /etc/danted.conf

echo "internal: $IP_INTERNAL port = 1080
external:$IP_EXTERNAL method: username none
user.privileged: root
user.notprivileged: nobody
client pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: error
}
pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        command: connect
        log: error
        method: none
}

" > /etc/danted.conf
service danted restart

