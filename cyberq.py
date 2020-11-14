#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import json
import time

import requests
from prometheus_client import start_http_server, Gauge

def get_status(url = 'http://192.168.220.18/status.xml'):
    """get XML and convert to dict"""
    r = requests.get(url)
    r.raise_for_status
    d = ET.fromstring(r.text)

    o = {}
    assert d.tag == 'nutcstatus'
    for e in d:
        o[e.tag] = e.text
    return o

def convert_temp(tstr):
    try:
        return int(tstr)/10
    except Exception as e:
        return -1

if __name__ == '__main__':
    start_http_server(8000)

    output = Gauge('cyberq_output_percent', 'percentage of output')
    cook_temp = Gauge('cyberq_cook_temp', 'pit temperature')
    food_temp = Gauge('cyberq_food_temp', 'food temperature degrees F', ['probe_number'])

    while True:
        s = get_status()
        print(json.dumps(s))
        output.set(float(s['OUTPUT_PERCENT']))
        cook_temp.set(convert_temp(s['COOK_TEMP']))
        for probe in ['1','2','3']:
            food_temp.labels(probe_number=probe).set(convert_temp(s['FOOD%s_TEMP'%probe]))
        time.sleep(10)
    

