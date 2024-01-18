FROM ubuntu:23.10

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y curl gnupg nginx apt-transport-https &&\
    echo 'deb https://deb.torproject.org/torproject.org mantic main' >> /etc/apt/sources.list && \
    curl https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --import && \
    gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add - && \
    apt-get update && apt-get install -y tor deb.torproject.org-keyring  openssh-server && \
    rm /etc/nginx/sites-enabled/default && rm /etc/nginx/sites-available/default

RUN useradd -rm -d /home/sshuser -s /bin/bash -g root -G sudo -u 1001 sshuser
RUN echo 'sshuser:passwd' | chpasswd && echo 'root:root' | chpasswd
COPY index.html /usr/share/nginx/html
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/onion.conf /etc/nginx/sites-available/
COPY config/torrc /etc/tor/torrc
COPY config/sshd_config /etc/ssh/sshd_config
COPY launch.sh /usr/local/bin/launch

RUN chmod +x /usr/local/bin/launch
EXPOSE 80 22
CMD ["/bin/bash", "-c", "launch"]
