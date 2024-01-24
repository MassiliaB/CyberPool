#!/bin/bash

ipsrc=$1
macsrc=$2
iptarg=$3
mactarg=$4

# Enable ip forwarding 
echo "1" /proc/sys/net/ipv4/ip_forward

tail -f /dev/null
#python3 inquisitor.py $ipsrc $macsrc $iptarg $mactarg