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
    db_path = os.environ['HOME'] + '/.pydrcom.json'
    attrs = ('username', 'password', 'serverip')
    conf = {}

    # first read options from command line arguments
    for attr in attrs:
        if getattr(options, attr) != None:
            conf[attr] = getattr(options, attr)

    # complete necessary options using the configuration file
    if len(conf) != 3:
        with open(db_path, 'r') as f:
            db = json.loads(f.read())
            for attr in attrs:
                if attr not in conf and attr in db:
                    conf[attr] = db[attr]

    # incomplete arguments
    if len(conf) != 3:
        print conf
        return False

    # write options to db if specified
    if options.write:
        with open(db_path, 'a') as f:
            db = {}
            for entry in conf:
                db[entry] = conf[entry]
            f.write(json.dumps(db))

    conf['base'] = 'http://' + conf['serverip'] + '/'
    conf['logout_url'] = conf['base'] + 'F.htm'
    return conf

def login(conf):
    parameters = {
        'DDDDD': conf['username'], 
        'upass': conf['password'], 
        '0MKKey': '%B5%C7%C2%BC+Login'}
    return requests.post(conf['base'], params=parameters)

def logout(conf):
    return requests.get(conf['logout_url'])

#-------------------------------------------------------------------------------------------

if __name__ == '__main__':

    parser = build_parser()

    try:
        options, command = parser.parse_args()
    except:
        print 'Invalid or insufficient options'
        parser.print_help()

    conf = build_conf(options)

    action = command[0]
    if action == 'help' or not conf:
        pass
    elif action == 'login':
        print login(conf)
    elif action == 'logout':
        print logout(conf)
    else:
        print 'action is not valid'
        print parser.print_help()

#-------------------------------------------------------------------------------------------
