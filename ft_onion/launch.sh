#!/bin/sh

#sudo nft -f /etc/nftables.conf
echo "hello"
service tor start
onion_hostname=$(cat /var/lib/tor/onion/hostname)
echo "server_name $onion_hostname;" > serverName
sed -i 's/server_name _;/'"$(cat serverName)"'/' /etc/nginx/nginx.conf

echo "PrivateNetwork=yes" > /lib/systemd/system/nginx.service
rm /etc/nginx/sites-available/defaut
rm /etc/nginx/sites-enabled/defaut

nginx -t
echo "****Hostname: $onion_hostname*****\n"
#nginx -g 'daemon off;'
/bin/bash