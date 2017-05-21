#!/usr/bin/env sh
echo "export PATH=$PATH:/tmp/usr/bin/" >> /etc/profile
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp/usr/lib/" >> /etc/profile

opkg update
opkg install git
opkg install nodogsplash
