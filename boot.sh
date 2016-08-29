#!/usr/bin/env bash

root=/app
log=$root/error.log

echo "Creating hosts file..."
cat $root/hosts >> /etc/hosts
rm $root/hosts

echo "Starting webhook server..."
python3 $root/run.py

# HAProxy is started by the Python application.

if [ -f $log ]; then
    rm $log;
fi

echo "Booting..." > $log
tail -f $log
