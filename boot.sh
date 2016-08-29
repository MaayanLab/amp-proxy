#!/usr/bin/env bash

root=/app
log=$root/error.log

echo "Creating hosts file..."
cat $root/hosts >> /etc/hosts
rm $root/hosts

echo "Starting webhook server..."
python3 $root/run.py

echo "Starting HAProxy..."
/usr/local/sbin/haproxy -D -f /etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid)

if [ -f $log ]; then
    rm $log;
fi

echo "Booting..." > $log
tail -f $log
