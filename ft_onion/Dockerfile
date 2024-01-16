FROM nginx:alpine
RUN apk update && apk upgrade && apk --no-cache add tor bash 

COPY index.html /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY torrc /etc/tor/torrc
COPY launch.sh /usr/local/bin/launch

RUN rm /etc/tor/torrc.sample && chown -R root /var/lib/tor && chmod -R 700 /var/lib/tor; \
    chmod +x /usr/local/bin/launch

EXPOSE 80
CMD ["bash", "-c", "launch"]
