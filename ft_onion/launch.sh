#!/bin/sh

echo "PrivateNetwork=yes" >> /etc/init.d/nginx.service
tor -f /etc/tor/torrc
/bin/bash