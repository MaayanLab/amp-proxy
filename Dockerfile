FROM haproxy:latest

RUN apt-get update && apt-get install -y python python-pip python3 python3-pip && apt-get clean all

RUN pip install Flask

COPY . /usr/local/bin
COPY haproxy.cfg /etc/haproxy/
EXPOSE 80
EXPOSE 52496
CMD /usr/local/sbin/haproxy -D -f /etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid && \
    /usr/local/bin/haproxy_reload && \
    /usr/local/bin/marathon-haproxy-webhook
