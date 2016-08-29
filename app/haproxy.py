"""Handles configuring and restarting HAPRoxy.
"""

import requests
from requests.auth import HTTPBasicAuth
import os

from .config import MARATHON_URL, MARATHON_USER, MARATHON_PASSWORD


HA_CONFIG_PATH = '/usr/local/etc/haproxy/haproxy.cfg'
INDENT = '    '
ERROR_MSG = 'haproxy.cfg does not exist. Are you developing locally?'


def reload():
    """Rebuilds HAProxy configuration file and restarts HAProxy.
    """
    config = _build_config()
    _write_config(config)
    _restart()


def config():
    """Returns HAProxy's configuration file. Throws a FileNotFoundError if the
    file does not exist.
    """
    try:
        f = open(HA_CONFIG_PATH, 'r')
        s = f.read()
        f.close()
    except FileNotFoundError:
        raise FileNotFoundError(ERROR_MSG)
    return s


def _restart():
    """Restarts HAPRoxy.
    """
    CMD = '/usr/local/sbin/haproxy -D ' \
          '-f %s ' \
          '-p /var/run/haproxy.pid ' \
          '-sf $(cat /var/run/haproxy.pid)' % HA_CONFIG_PATH
    os.system(CMD)


def _write_config(config_contents):
    """Writes contents to HAPRoxy configuration file.
    """
    try:
        with open(HA_CONFIG_PATH, 'w+') as f:
            f.write(config_contents)
    except FileNotFoundError:
        raise FileNotFoundError(ERROR_MSG)


def _build_config():
    """Builds the contents for the HAPRoxy configuration file.
    """
    apps_url = '%s/v2/apps' % MARATHON_URL
    auth = HTTPBasicAuth(MARATHON_USER, MARATHON_PASSWORD)
    apps = requests.get(apps_url, auth=auth).json()['apps']

    tasks_url = '%s/v2/tasks' % MARATHON_URL
    auth = HTTPBasicAuth(MARATHON_USER, MARATHON_PASSWORD)
    tasks = requests.get(tasks_url, auth=auth).json()['tasks']

    servers = {}
    for i, task in enumerate(tasks):
        if task['state'] != 'TASK_RUNNING':
            continue

        name = task['appId'][1:]
        h = task['host']
        ports = task['ports']
        if 'servicePorts' not in task:
            continue
        service_ports = task['servicePorts']

        if not len(ports):
            continue

        for j, port in enumerate(service_ports):
            key = name + '-' + str(port)
            server = 'server ' + name + '-' + str(i) + ' ' + h + ':' \
                + str(ports[j])
            if key in servers:
                servers[key].append(server)
            else:
                servers[key] = [server]

    frontend = ''
    backend = ''
    listen = ''
    finished_apps = []
    legacy_backend = ''
    for task in tasks:
        if task['state'] != 'TASK_RUNNING':
            continue

        name = task['appId'][1:]

        # Find the app with the same id as the current task
        app = [app for app in apps if app['id'] == task['appId']][0]
        # Do not expose any apps without a public label set to true
        if 'public' not in app['labels'] or app['labels']['public'] != "true":
            continue

        if 'servicePorts' not in task:
            continue
        service_ports = task['servicePorts']

        for port in service_ports:
            name_port = '%s-%s' % (name, port)
            if name_port in finished_apps:
                continue
            else:
                finished_apps.append(name_port)

            if name == 'legacy-proxy':
                legacy_backend = name_port

            frontend += _frontend(name_port, name)
            backend += _backend(name_port)
            listen += _listen(name_port, port)

            for server in servers[name_port]:
                backend += '%s%s\n' % (INDENT, server)
                listen += '%s%s\n' % (INDENT, server)

            backend += '\n'
            listen += '\n'

    if legacy_backend:
        frontend += '%sdefault_backend %s_cluster\n\n' % (
            INDENT, legacy_backend)

    ha_config = '''global
    daemon
    log 127.0.0.1 local0
    log 127.0.0.1 local1 notice
    maxconn 4096

defaults
    log         global
    retries     3
    maxconn     2000
    timeout connect  5000
    timeout client  500000
    timeout server  500000

frontend http-in
    bind *:80
    mode http
    option httplog
    option dontlognull
    option forwardfor
    stats enable
    stats uri /haproxy
    stats auth admin:admin

    acl invalid_src src 176.9.5.71 80.237.193.116
    tcp-request connection reject if invalid_src
    http-request deny if invalid_src\n\n'''

    ha_config += frontend
    ha_config += backend
    ha_config += listen

    return ha_config


def _frontend(name_port, name):
    """Builds "frontend" sections. From the documentation:

        "A 'frontend' section describes a set of listening sockets accepting
        client connections."

    Example:

        acl host_<APP_NAME> path_reg -i ^/<APP_NAME> ($|/)
        use_backend <APP_SERVER> if host_<APP_NAME>
    """
    s = '%sacl host_%s path_reg -i ^/%s($|/)\n' \
        '%suse_backend %s_cluster if host_%s\n\n' % (
            INDENT, name, name, INDENT, name_port, name)
    return s


def _backend(name_port):
    """Builds "backend" sections. From the documentation:

        "A 'backend' section describes a set of servers to which the proxy
        will connect to forward incoming connections."

    Example:

        backend <APP_SERVER>
            option forwardfor
            mode http
            balance leastconn
            server <APP_NAME>-<INDEX> <MACHINE>:<PORT>
    """
    s = 'backend %s_cluster\n' \
        '%soption forwardfor\n' \
        '%smode http\n' \
        '%sbalance leastconn\n' % (
            name_port, INDENT, INDENT, INDENT)
    return s


def _listen(name_port, port):
    """Builds "backend" sections. From the documentation:

        "A 'listen' section defines a complete proxy with its frontend and
        backend parts combined in one section. It is generally useful
        for TCP-only traffic."

    Example:

        listen <APP_NAME>-<PORT>
            bind 0.0.0.0:<PORT>
            mode tcp
            option tcplog
            balance leastconn
            server baylor-0 <MACHINE>:<PORT>
    """
    s = 'listen %s\n' \
        '%sbind 0.0.0.0:%s\n' \
        '%smode tcp\n' \
        '%soption tcplog\n' \
        '%sbalance leastconn\n' % (
            name_port, INDENT, port, INDENT, INDENT, INDENT)
    return s
