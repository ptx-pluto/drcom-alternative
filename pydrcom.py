#!/usr/bin/env python
# -*- utf-8 -*-
#-------------------------------------------------------------------------------------------
# PyDrCom HTTP login script
#
# Author : sheep9275@gmail.com
# Version: 1.0
#-------------------------------------------------------------------------------------------
# check usage: pydrcom help
#-------------------------------------------------------------------------------------------

import requests, os, sys, json
from optparse import OptionParser

#-------------------------------------------------------------------------------------------

DB_PATH = os.environ['HOME'] + '/.pydrcom.json'

#-------------------------------------------------------------------------------------------

def build_parser():
    usage = 'Usage: pydrcom [login|logout|help] options'
    parser = OptionParser(usage)
    parser.add_option('-u', '--username',
                      action='store', type='string', dest='username', metavar='USERNAME')
    parser.add_option('-p', '--password',
                      action='store', type='string', dest='password', metavar='PASSWORD')
    parser.add_option('-s', '--server-ip',
                      action='store', type='string', dest='serverip', metavar='SERVER-IP',
                      help='ip address of the authentication server')
    parser.add_option('-w', '--write',
                      action='store_true', dest='write',
                      help='write options to file (~/.pydrcom.json)')
    return parser

def build_conf(options):
    attrs = ('username', 'password', 'serverip')
    conf = {}

    for attr in attrs:
        if getattr(options, attr) != None:
            conf[attr] = getattr(options, attr)

    try:
        with open(DB_PATH, 'r') as f:
            db = json.loads(f.read())
            for attr in [ clause for clause in attrs if clause not in conf ]:
                conf[attr] = db[attr]
    except: 
        pass

    if len(conf) != 3:
        print('insufficient parameter, %s are needed' \
              % ','.join([ clause for clause in attrs if clause not in conf ]))
        sys.exit(1)
    elif options.write:
        with open(DB_PATH, 'w') as f:
            f.write(json.dumps(conf))

    conf['base'] = 'http://' + conf['serverip'] + '/'

    return conf


def login(conf):
    parameters = {
        'DDDDD': conf['username'], 
        'upass': conf['password'], 
        '0MKKey': '%B5%C7%C2%BC+Login'}
    return requests.post(conf['base'], params=parameters)


def logout(conf):
    return requests.get(conf['base'] + 'F.htm')

#-------------------------------------------------------------------------------------------

if __name__ == '__main__':

    parser = build_parser()

    try:
        options, command = parser.parse_args()
    except:
        print('Invalid or insufficient options')

    conf = build_conf(options)
    action = command[0]

    if action == 'help' or not conf:
        pass
    elif action == 'login':
        print(login(conf))
    elif action == 'logout':
        print(logout(conf))
    else:
        print('action is not valid')

#-------------------------------------------------------------------------------------------
