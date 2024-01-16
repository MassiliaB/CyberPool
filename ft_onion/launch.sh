#!/bin/sh

sudo nft -f /etc/nftables.conf
service tor start
onion_hostname=$(cat /var/lib/tor/onion/hostname)
echo "server_name $onion_hostname;" > serverName
sed -i 's/server_name _;/'"$(cat serverName)"'/' /etc/nginx/nginx.conf

service nginx reload

#nginx -g 'daemon off;'
/bin/sh