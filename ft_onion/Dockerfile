FROM ubuntu:23.10

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y curl gnupg nginx apt-transport-https &&\
    echo 'deb https://deb.torproject.org/torproject.org mantic main' >> /etc/apt/sources.list && \
    curl https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --import && \
    gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add - && \
    apt-get update && apt-get install -y tor deb.torproject.org-keyring

COPY index.html /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY torrc /etc/tor/torrc
COPY launch.sh /usr/local/bin/launch
# COPY nft-rules /etc/nftables.conf

RUN chown -R www-data /var/lib/tor; \
    chmod +x /usr/local/bin/launch

EXPOSE 80 22
CMD ["/bin/bash", "-c", "launch"]
