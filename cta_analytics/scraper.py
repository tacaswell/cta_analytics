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

def parse_date(date_str):
    if 'fstr' in config_dict:
        fstr = config_dict['fstr']
    else:
        fstr = '%Y%m%d %H:%M'

    return datetime.strptime(date_str, fstr)


def get_buses_on_route(route_nums):
    """
    Returns the result of the api call for all busses on the routes specified.

    Only the first 10 route numbers are queried
    """
    url = '%s/getvehicles' % config_dict['url']

    route_nums = route_nums[:10]

    params = {'key': config_dict['key'],
              'rt': ','.join([str(int(r)) for r in route_nums])
              }

    r = requests.get(url, params=params, timeout=1.0)

    if r.status_code != 200:
        print "ERROR"
        return None

    r_xml = ET.fromstring(r.text)

    busses = []
    for vehicle in r_xml:
        if vehicle.tag != 'vehicle':
            continue

        local_dict = {}
        for data in vehicle:
            local_dict[data.tag] = data.text

        if 'tmstmp' in local_dict:
            local_dict['timestamp'] = parse_date(local_dict['tmstmp'])
        else:
            print local_dict
        busses.append(local_dict)

    return busses


def get_time_offset():
    url = '%s/gettime' % config_dict['url']
    params = {'key': config_dict['key']}

    cta_time = requests.get(url, params=params, timeout=1.0)
    sys_time = datetime.now()

    fmt_str = '%Y%m%d %H:%M:%S'
    time_xml = ET.fromstring(cta_time.text)
    cta_time_ = datetime.strptime(time_xml[0].text, fmt_str)

    return cta_time_ - sys_time


def get_stop_distance(route):
    url = '%s/getpatterns' % config_dict['url']

    params = {'key': config_dict['key'],
              'rt': str(int(route))}

    r = requests.get(url, params=params, timeout=1.0)

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


def get_pattern_by_route(route):
    url = '%s/getpatterns' % config_dict['url']

    params = {'key': config_dict['key'],
              'rt': route}

    r = requests.get(url, params=params, timeout=1.0)

    route_xml = ET.fromstring(r.text)

    res = {}

    for ptr in route_xml:
        local_dict = {}
        for data in ptr[:3]:
            local_dict[data.tag] = data.text
        pts = []
        for pt in ptr[3:]:
            pt_dict = {}
            for d in pt:
                pt_dict[d.tag] = d.text
            pts.append(pt_dict)
        local_dict['pts'] = pts
        res[ptr[0].text] = local_dict

    return res


def get_pattern_by_pid(pid):
    url = '%s/getpatterns' % config_dict['url']

    params = {'key': config_dict['key'],
              'pid': str(pid)}

    r = requests.get(url, params=params, timeout=1.0)

    route_xml = ET.fromstring(r.text)
    res = {}
    for ptr in route_xml:
        local_dict = {}
        for data in ptr[:3]:
            local_dict[data.tag] = data.text
        pts = []
        for pt in ptr[3:]:
            pt_dict = {}
            for d in pt:
                pt_dict[d.tag] = d.text
            pts.append(pt_dict)
        local_dict['pts'] = pts
        res[ptr[0].text] = local_dict

    return res


def get_routes():

    url = '%s/getroutes' % config_dict['url']

    params = {'key': config_dict['key'], }

    r = requests.get(url, params=params, timeout=1.0)

    route_xml = ET.fromstring(r.text)

    routes = []
    for route in route_xml:
        print route[0].text, route[1].text


def get_directions(rt_num):

    url = '%s/getdirections' % config_dict['url']

    params = {'key': config_dict['key'],
              'rt': str(int(rt_num))}

    r = requests.get(url, params=params, timeout=1.0)

    directions_xml = ET.fromstring(r.text)

    return [dr.text for dr in directions_xml]


def get_stops(rt_num, direction):

    url = '%s/getstops' % config_dict['url']

    params = {'key': config_dict['key'],
              'rt': str(int(rt_num)),
              'dir': direction}

    r = requests.get(url, params=params, timeout=1.0)
    stop_xml = ET.fromstring(r.text)

    stops = []
    for stop in stop_xml:
        local_dict = {}
        for data in stop:
            local_dict[data.tag] = data.text
        stops.append(local_dict)
    return stops


def get_predictions(stops):

    url = '%s/getpredictions' % config_dict['url']

    stops = stops[:10]

    params = {'key': config_dict['key'],
              'stpid': ','.join([str(int(s)) for s in stops])
              }

    r = requests.get(url, params=params, timeout=1.0)

    if r.status_code != 200:
        print "ERROR"
        return None

    r_xml = ET.fromstring(r.text)
    busses = []
    for prd in r_xml:
        if prd.tag != 'prd':
            continue

        local_dict = {}
        for data in prd:
            local_dict[data.tag] = data.text

        if 'tmstmp' in local_dict:
            local_dict['timestamp'] = parse_date(local_dict['tmstmp'])
        if 'prdtm' in local_dict:
            local_dict['prd_time'] = parse_date(local_dict['prdtm'])

        else:
            print local_dict
        busses.append(local_dict)

    return busses
