"""Manages initialization code and application endpoints.
"""

from flask import Flask, request, render_template
from . import haproxy
from .config import ROOT_DIR
import logging


PATH = 'marathon-haproxy-webhook'
templates_dir = '%s/templates' % ROOT_DIR
app = Flask(PATH, static_url_path='', template_folder=templates_dir)


# logging.basicConfig(filename='%s/production.log' % ROOT_DIR,
#                     filemode='a',
#                     level=logging.DEBUG)
# logger = logging.getLogger()

# CRITICAL: When HAProxy first starts, we need it to build its config.
haproxy.reload()


@app.route('/%s' % PATH, methods=['GET', 'POST'])
def index():
    """Updates the HAProxy config and reloads HAProxy if needed.
    """
    if request.method == 'POST':
        #logger.info('Marathon callback URL to update haproxy.cfg.')
        json = request.get_json(force=True)
        if _task_has_updated(json):
            haproxy.reload()
        return 'Success'
    else:
        haproxy.reload()
        ha_config = haproxy.config()
        return render_template('ha-config.html', ha_config=ha_config)


def _task_has_updated(json):
    """Returns true if Marathon's API indicates a task has changed, False
    otherwise.
    """
    is_status_update = json.get('eventType') == 'status_update_event'
    STATUSES = ['TASK_RUNNING', 'TASK_FAILED', 'TASK_KILLED', 'TASK_LOST']
    is_task_update = json.get('taskStatus') in STATUSES
    return is_status_update and is_task_update
