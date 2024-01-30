#!/bin/bash

pip install scapy 
IPSRC=$(ifconfig eth0 | awk '/inet /{print $2}' | grep -Eo '([0-9]*\.){3}[0-9]*')
MACSRC=$(ifconfig eth0 | awk '/ether /{print $2}')
IPTARG=$(echo $IPSRC | sed 's/\.2$/.3/')
MACTARG=$(echo $MACSRC | sed 's/\.2$/.3/')

tail -f /dev/null
#python3 inquisitor.py $IPSRC $MACSRC $iptarg $mactarg