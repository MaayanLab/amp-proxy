#!/usr/bin/env bash

root=/app
log=$root/error.log

# If we do not set the TERM variable, the command prompt will not allow us to
# use commands like `clear`. I'm not sure why.
echo "Setting TERM environment variable..."
export TERM=xterm

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
