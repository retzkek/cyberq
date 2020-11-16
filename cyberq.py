#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import json
import time
import re

import requests
from prometheus_client import start_http_server, Gauge
import click

class CyberQ(object):
    def __init__(self, base_url='http://192.168.220.18'):
        self.base_url = base_url

    def get_status(self, path = '/status.xml'):
        """get XML and convert to dict"""
        r = requests.get(self.base_url+path)
        r.raise_for_status
        d = ET.fromstring(r.text)

        o = {}
        assert d.tag == 'nutcstatus'
        for e in d:
            o[e.tag] = e.text
        return o

    def get_setpoints(self, path = '/'):
        """get setpoints from page JS source (why isn't this in status.xml??)"""
        r = requests.get(self.base_url+path)
        r.raise_for_status

        o = {}
        for line in r.iter_lines():
            m=re.search(r'document\.mainForm\._(.+)\.value = TempPICToHTML\((\d+), 0\);',str(line))
            if m:
                o[m[1]] = m[2]
        return o
                

def convert_temp(tstr):
    try:
        return int(tstr)/10
    except Exception as e:
        return -1

@click.command()
@click.option('--url', default='http://192.168.220.18', help='base URL for CyberQ')
@click.option('--port', default=8000, help='listen port for prometheus metrics publisher')
@click.option('--addr', default='', help='listen address for prometheus metrics publisher')
def main(url, port, addr):
    output = Gauge('cyberq_output_percent', 'percentage of output')
    cook_temp = Gauge('cyberq_cook_temp', 'pit temperature')
    cook_set = Gauge('cyberq_cook_set_temp', 'pit set temperature')
    food_temp = Gauge('cyberq_food_temp', 'food temperature degrees F', ['probe_number'])
    food_set = Gauge('cyberq_food_set_temp', 'food temperature setting degrees F', ['probe_number'])
    start_http_server(port, addr=addr)

    c = CyberQ()
    while True:
        try:
            s = c.get_status()
        except Exception as e:
            print('error getting status: %s',e)
        else:
            print(json.dumps(s))
            output.set(float(s['OUTPUT_PERCENT']))
            cook_temp.set(convert_temp(s['COOK_TEMP']))
            for probe in ['1','2','3']:
                food_temp.labels(probe_number=probe).set(convert_temp(s['FOOD%s_TEMP'%probe]))
        try:
            s = c.get_setpoints()
        except Exception as e:
            print('error getting setpoints: %s',e)
        else:
            print(json.dumps(s))
            cook_set.set(convert_temp(s['COOK_SET']))
            for probe in ['1','2','3']:
                food_set.labels(probe_number=probe).set(convert_temp(s['FOOD%s_SET'%probe]))
        time.sleep(10)

if __name__ == '__main__':
    main(auto_envvar_prefix='CYBERQ')

    

