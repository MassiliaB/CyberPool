FROM debian:buster
RUN apt-get update && apt-get upgrade -y && apt-get install tor sudo nftables nginx -y

RUN groupadd -r nginx && useradd -r -g nginx nginx
COPY index.html /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY torrc /etc/tor/torrc
COPY launch.sh /usr/local/bin/launch
COPY nft-rules /etc/nftables.conf

RUN chown -R debian-tor /var/lib/tor; \
    chmod +x /usr/local/bin/launch

EXPOSE 80 22
CMD ["/bin/sh", "-c", "launch"]
