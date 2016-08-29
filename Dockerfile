FROM haproxy:latest

RUN apt-get update

RUN apt-get -y install python3 \
    python3-dev \
    python3-pip \
    python3-setuptools

RUN apt-get clean all

RUN pip3 install -Iv Flask==0.11 \
    requests==2.6.0

# HAProxy webhook.
EXPOSE 52496
# All other incoming requests.
EXPOSE 80

ADD . /app

CMD /app/boot.sh
