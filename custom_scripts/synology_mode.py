#!/usr/bin/python3

"""
Script for the control of the Synology Surveillance Station Home Mode

This is to allow for the station to be set into home mode so that
recordings can be either disabled when required or disable notifcations

Modes supported

- home
- away
- status

"""

import argparse
import requests
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', action='store', dest='url',
                    help="target DSM URL (e.g https://1.2.3.4:5001)")
parser.add_argument('-a', '--account', action='store', dest='account',
                    help="User account name")
parser.add_argument('-p', '--password', action='store', dest='password',
                    help="User account password")
parser.add_argument('-m', '--mode', action='store', dest='mode',
                    help="Operational mode (home/away/status)")


def login():
    """ Log into the array """
    global session
    data = {'api': 'SYNO.API.Auth',
            'method': 'Login',
            'version': '2',
            'session': 'SurveillanceStation',
            'account': args.account,
            'passwd': args.password,
            'format': 'cookie'}
    url = "{}/webapi/auth.cgi".format(args.url)

    resp = session.get(url, params=data, timeout=5, verify=False)
    if resp.status_code == 200:
        return True
    else:
        return False

def logout():
    """ Log out of the array """
    global session
    data = {'api': 'SYNO.API.Auth',
            'method': 'Logout',
            'version': '2',
            'session': 'SurveillanceStation'}
    url = "{}/webapi/auth.cgi".format(args.url)
    resp = session.get(url, params=data, timeout=5, verify=False)
    if resp.status_code == 200:
        session.close()
        return True
    else:
        return False

def setmode():
    """ Set the requested mode on array """
    global session
    global switchon
    if args.mode == 'home':
        # do home switch
        method = {'method': 'Switch', 'on': 'true'}
    elif args.mode == 'away':
        # do away switch
        method = {'method': 'Switch', 'on': 'false'}
    else:
        # get status
        method = {'method': 'GetInfo'}
    data = {'api': 'SYNO.SurveillanceStation.HomeMode',
            'version': '1',
            'session': 'SurveillanceStation'}
    data.update(method)
    url = "{}/webapi/entry.cgi".format(args.url)
    resp = session.get(url, params=data, timeout=5, verify=False)
    if resp.status_code == 200:
        if args.mode == 'status':
            data = resp.json()
            if data['data']['on']:
                switchon = True
            else:
                switchon = False
        return True
    else:
        return False

def getstatus():
    """ Get the status of the home mode on the array """

args = parser.parse_args()
session = requests.session()
requests.packages.urllib3.disable_warnings() 
if login():
    setmode()
    logout()
    if args.mode == 'status':
        if switchon:
            sys.exit(0)
        else:
            sys.exit(1)
