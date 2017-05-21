#!/bin/sh
Debug=/root/g8keepr/log/debug.log
Log=/root/g8keepr/log/dnsmasq.log
Script=/root/g8keepr/src/detect_connection.py
# env not set here (check env >> $debug, so need to remediate that)
# need to export /tmp/usr/lib to get access to python
export PATH=$PATH:/tmp/usr/bin/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp/usr/lib/
date >> $Log
echo $* >> $Log
$Script $* 
echo 'ok' >> $Debug
#
