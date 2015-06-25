#!/usr/bin/env python3
__author__ = 'mmcdermott'

from urllib.request import Request, urlopen
import json
import argparse
import base64

parser = argparse.ArgumentParser(description='Generate an HAProxy config file '
                                             'for Marathon given its URL.')
parser.add_argument('baseUrl',
                    help='The baseURL of the Marathon master with the proper '
                         'port. (example: http://localhost:8080)')
parser.add_argument('-u', '--username', type=str,
                    help='The username to login to Marathon.')
parser.add_argument('-p', '--password', type=str,
                    help='The password to login to Marathon.')

args = parser.parse_args()
baseUrl = args.baseUrl
username = args.username
password = args.password

userPass = username + ':' + password

base64string = base64.b64encode(bytes(userPass, 'utf-8'))
if 'http://:8080' in baseUrl:
    print('Please make sure that your MARATHON_MASTER env is set properly '
          'or that you\'re baseURL is properly formatted')
    appUrl = 'THIS IS AN IMPROPER URL'
    baseUrl = 'THIS IS AN IMPROPER URL'
else:
    appUrl = baseUrl + '/v2/apps'
    taskUrl = baseUrl + '/v2/tasks'
appReq = Request(appUrl)
appReq.add_header('Accept', 'application/json')
appReq.add_header('Authorization', 'Basic ' + base64string.decode('utf-8'))
apps = json.loads(urlopen(appReq).read().decode('utf-8'))['apps']

taskReq = Request(taskUrl)
taskReq.add_header('Accept', 'application/json')
taskReq.add_header('Authorization', 'Basic bWFheWFubGFiOnN5c3RlbXNiaW9sb2d5')
tasks = json.loads(urlopen(taskReq).read().decode('utf-8'))['tasks']

config = '''
global
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
'''

config += '''
frontend http-in
  bind *:80
  mode http
  option httplog
  option dontlognull
  option forwardfor
  stats enable
  stats uri /haproxy
  stats auth admin:admin

'''

serverDict = {}
for i, task in enumerate(tasks):
    name = task['appId'][1:]
    h = task['host']
    ports = task['ports']
    if 'servicePorts' not in task:
        continue
    servicePorts = task['servicePorts']

    for j, port in enumerate(servicePorts):
        key = name + '-' + str(port)
        servStr = 'server ' + name + '-' + str(i) + ' ' + h + ':' \
            + str(ports[j])
        if key in serverDict:
            serverDict[key].append(servStr)
        else:
            serverDict[key] = [servStr]

frontend = ''
backend = ''
listen = ''
finishedApps = []
for task in tasks:
    name = task['appId'][1:]

    # Find the app with the same id as the current task
    app = [app for app in apps if app['id'] == task['appId']][0]
    # Do not expose any apps without a public label set to true
    if 'public' not in app['labels'] or app['labels']['public'] != "true":
        continue

    if 'servicePorts' not in task:
        continue
    servicePorts = task['servicePorts']

    for port in servicePorts:
        namePort = name + '-' + str(port)
        # Prevent duplicates
        if namePort in finishedApps:
            continue
        else:
            finishedApps.append(namePort)

        frontend += '  acl host_' + name + ' path_reg -i ^/' + name \
            + '($|/)\n' + '  use_backend ' + namePort + '_cluster if host_' \
            + name + '\n\n'

        backend += 'backend ' + namePort + '_cluster' + '\n' \
            + '  option forwardfor\n  mode http\n  balance leastconn\n'

        listen += 'listen ' + namePort + '\n' + '  bind 0.0.0.0:' + str(port) \
            + '\n  mode tcp\n  option tcplog\n  balance leastconn\n'

        for string in serverDict[namePort]:
            backend += '  ' + string + '\n'
            listen += '  ' + string + '\n'

        backend += '\n'
        listen += '\n'

config += frontend
config += backend
config += listen

print(config)
