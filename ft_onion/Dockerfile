FROM nginx:alpine
RUN apk update && apk add tor

COPY index.html /usr/share/nginx/html
COPY nginx.conf .
COPY torrc /etc/tor/torrc
RUN rm /etc/tor/torrc.sample && chown -R root /var/lib/tor
# COPY sshd_config .

EXPOSE 8080
CMD ["sh", "-c", "nginx -g daemon off; tor -f /etc/tor/torrc"]