FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get install python3 \
    python3-pip vim net-tools ca-certificates tcpdump -y

COPY script.sh script.sh
COPY inquisitor.py inquisitor.py
RUN chmod 750 script.sh
#RUN echo "1" > /proc/sys/net/ipv4/ip_forward

CMD ["./script.sh"]