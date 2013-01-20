#Copyright 2013 Thomas A Caswell
#tcaswell@gmail.com
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or (at
#your option) any later version.
#
#This program is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, see <http://www.gnu.org/licenses>.
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

from config import config_dict


def get_buses_on_route(route_num):
    url = '%s/getvehicles' % config_dict['url']

    params = {'key': config_dict['key'],
              'rt': str(int(route_num))
              }

    r = requests.get(url, params=params)
    if r.status_code != 200:
        print "ERROR"
        return None

    r_xml = ET.fromstring(r.text)
    busses = {}
    for vehicle in r_xml:
        local_dict = {}
        for data in vehicle:
            local_dict[data.tag] = data.text
        busses[local_dict['vid']] = local_dict
    return busses


def get_time_offset():
    url = '%s/gettime' % config_dict['url']
    params = {'key': config_dict['key']}

    cta_time = requests.get(url, params=params)
    sys_time = datetime.now()

    fmt_str = '%Y%m%d %H:%M:%S'
    time_xml = ET.fromstring(cta_time.text)
    cta_time_ = datetime.strptime(time_xml[0].text, fmt_str)

    return cta_time_ - sys_time


def get_stop_distance(route):
    url = '%s/getpatterns' % config_dict['url']

    params = {'key': config_dict['key'],
              'rt': str(int(route))}

    r = requests.get(url, params=params)

    route_xml = ET.fromstring(r.text)

    stop_dist = {}
    for ptr in route_xml:
        rtdir = ptr[2].text
        stops = {}
        for pt in ptr[3:]:
            if pt[3].text == 'S':
                stops[int(pt[4].text)] = float(pt[6].text)
        stop_dist[rtdir] = stops

    return stop_dist
