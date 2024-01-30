FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install vsftpd net-tools ftp -y

CMD ["sh", "-c", "service vsftpd start && tail -f /dev/null"]