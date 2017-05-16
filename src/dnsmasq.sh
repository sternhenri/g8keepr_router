#! /bin/sh
Debug=/root/g8keepr/log/debug.log
Log=/root/g8keepr/log/dnsmasq.log
Script=/root/g8keepr/src/detect_connection.py
date >> $Log
echo $* >> $Log
$Script $* &
echo 'ok' >> $Debug
cat $Script >> $Debug
#
