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
from pymongo import MongoClient


class mongo_wrapper(object):
    def __init__(self, server='localhost', port=27017):
        self.connection = MongoClient(server, port)
        self.db = self.connection.cta_analytics

    def add_bus_locations(self, bus_locs):
        coll = self.db.bus_location
        coll.insert(bus_locs)

    def add_stop_prediction(self, predictions):
        coll = self.db.arrrival_prediction
        coll.insert(predictions)
