FROM ubuntu:latest

RUN apt-get update && apt-get upgrade && apt-get install python3 python

COPY script.sh script.sh
COPY inquisitor.py inquisitor.py
RUN chmod 750 script.sh

CMD [ "./script.sh", "ipsrc", "macsrc", "iptarg", "mactarg"]