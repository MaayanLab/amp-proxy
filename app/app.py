#!/usr/bin/env python

from flask import Flask, request, render_template
import logging
from . import haproxy


logging.basicConfig(filename='/app/production.log',
                    filemode='a',
                    level=logging.DEBUG)

logger = logging.getLogger()

PATH = 'marathon-haproxy-webhook'

app = Flask(PATH, static_url_path='')


@app.route('/%s' % PATH, methods=['GET', 'POST'])
def index():
    """
    """
    if request.method == 'POST':
        logger.info('Marathon callback URL to update haproxy.cfg.')
        json = request.get_json(force=True)
        if _task_has_updated(json):
            haproxy.reload()
        return 'Success'
    else:
        logger.info('GET request')
        haproxy.reload()
        ha_config = haproxy.config()
        return render_template('ha-config.html', ha_config=ha_config)


def _task_has_updated(json):
    """
    """
    is_status_update = json['eventType'] == 'status_update_event'
    STATUSES = ['TASK_RUNNING', 'TASK_FAILED', 'TASK_KILLED', 'TASK_LOST']
    is_task_update = json['taskStatus'] in STATUSES
    return is_status_update and is_task_update
