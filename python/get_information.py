#!/usr/bin/python3

import os
import json
import socket
import urllib.request


# global paths
projectPath = os.path.abspath(os.path.dirname(__file__))
jsonFile = os.path.join(projectPath, '../information/information.json')

def internet_on(host="duckduckgo.com", port=80, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return ex


def get_response_code(url):
    conn = urllib.request.urlopen(url)
    return conn.getcode()


def get_space_state():
    spaceAPIUrl = "https://spaceapi.sbg.chaostreff.at/status/json"
    httpResponse = get_response_code(spaceAPIUrl)
    if httpResponse == 200:
        jsonReturn = urllib.request.urlopen(spaceAPIUrl).read()
        try:
            tmp = json.loads(jsonReturn)
            tmp = tmp['state']['open']
            if tmp == True:
                return 'Open'
            elif tmp == False:
                return 'Closed'
            else:
                return 'Unknown state'
        except json.decoder.JSONDecodeError:
            return 'JSONError'
    else:
        return f'Err: {httpResponse}'


if __name__ == '__main__':
    connection = internet_on()
    if connection == True:
        information = {}
        information['hackerspace'] = get_space_state()
        jsonResult = json.dumps(information, sort_keys=True)
        with open(jsonFile, 'w') as resultFile:
            resultFile.write(jsonResult)
            print(jsonResult)
    else:
        information = {'error': str(connection)}
        jsonError = json.dumps(information)
        with open(jsonFile, 'w') as resultFile:
            resultFile.write(jsonError)
