FROM haproxy:latest

RUN apt-get update

RUN apt-get -y install python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    nginx \
    uwsgi-core

RUN apt-get clean all

RUN pip3 install -Iv Flask==0.11 \
    requests==2.6.0 \
    uwsgi

EXPOSE 80

ADD . /app

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

CMD /app/boot.sh
