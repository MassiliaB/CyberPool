#!/bin/sh

service tor start
onion_hostname=$(cat /var/lib/tor/onion/hostname)
echo "server_name $onion_hostname;" > serverName
sed -i 's/server_name _;/'"$(cat serverName)"'/' /etc/nginx/sites-available/onion.conf
ln -sf /etc/nginx/sites-available/onion.conf /etc/nginx/sites-enabled/onion.conf
mkdir /var/run/sshd

sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

nginx -t
echo "Hostname: $onion_hostname\n"
/usr/sbin/sshd -D
nginx -g 'daemon off;'