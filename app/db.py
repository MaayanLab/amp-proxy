"""A tiny "database". We just want to record when HAProxy has been reloaded
for debugging purposes.
"""

import datetime


def record_time():
    t = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    with open('db.txt', 'w+') as db:
        db.write(t)


def get_time():
    with open('db.txt', 'r') as db:
        t = db.read()
    return t
