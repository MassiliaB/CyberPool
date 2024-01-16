FROM debian:buster
RUN apt-get update && apt-get upgrade -y && apt-get install tor sudo nftables nginx -y

RUN groupadd -r nginx && useradd -r -g nginx nginx
COPY index.html /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY torrc /etc/tor/torrc
COPY launch.sh /usr/local/bin/launch
COPY nft-rules /etc/nftables.conf

RUN rm /etc/tor/torrc.sample && chown -R root /var/lib/tor && chmod -R 700 /var/lib/tor; \
    chmod +x /usr/local/bin/launch

EXPOSE 80 22
CMD ["bash", "-c", "launch"]
