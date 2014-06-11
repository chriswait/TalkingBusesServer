#!/usr/bin/python
from pymongo import MongoClient
from datetime import datetime
from bson.json_util import dumps, loads
from urllib2 import urlopen, HTTPError
from log import log_info
from naptan import addNaptanDataToStop

# DATABASE
client = MongoClient('localhost', 27017)
db = client.bus

# COLLECTIONS
info = db.info
stops = db.stops
dests = db.dests
services = db.services

# ADMIN
def clear_database():
    log_info("Clearing Database")
    client.drop_database('bus')
    db = client.bus

# TOPOLOGY
def getCurrentTopoID():
    result = info.find_one()
    if result: return result['topoID']
    else: return None

def setCurrentTopoID(new_topo_id):
    log_info("Updating topology id: \t%s" % new_topo_id)
    current = info.find_one()
    if not current: current = {}
    current['topoID'] = new_topo_id
    current['last_updated'] = datetime.utcnow()
    info.save(current)

# SERVICES
def getServicesDB():
    return services.find()


def populateServices(new_services):
    log_info("Populating services \t(%i)" % len(new_services))
    for service in new_services:
        services.save(service)

# STOPS
def getStopsDB():
    return stops.find()

# REVERSE GEOCODING FOR STOPS
def add_street_name_to_stop(stop):
    x,y = stop['x'], stop['y']
    url = """http://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f&sensor=true """ % (x,y)
    try:
        response = urlopen(url).read()
        responseDict = loads(response)
        if (len(responseDict['results'])>0):
            for result in responseDict['results']:
                for component in result['address_components']:
                    if "route" in component['types']:
                        street_name = component['long_name']
                        stop['street'] = street_name
                        return stop
        return stop
    except HTTPError, error:
        log_error(error)

# HEADING FOR STOPS
def getHeadingForStopCap(cap):
    bearings = ["North-East","East","South-East","South","South-West","West","North-West","North"]
    adjust = cap - 22.5
    if adjust<0: adjust += 360.0
    index = int(adjust/45)
    return bearings[index]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def add_service_mnemos_to_stop(stop, services_dict):
    stop_service_ids = stop['services']
    mnemos = []
    for service_id in stop_service_ids:
        if service_id in services_dict:
            mnemos.append(services_dict[service_id]['mnemo'])
    if len(mnemos)>1: stop['service_mnemos'] = ",".join(mnemos[:-1])+" and "+mnemos[-1]
    else: stop['service_mnemos'] = mnemos[0]
    return stop

def populateStops(new_stops):
    services_dict = {service['ref']:service for service in getServicesDB()}
    log_info("Populating stops \t(%i)" % len(new_stops))
    for stop in new_stops:
        stop['heading'] = getHeadingForStopCap(stop['cap'])
        stop = addNaptanDataToStop(stop)
        stop = add_service_mnemos_to_stop(stop, services_dict)
        if not'street' in stop:
            stop = add_street_name_to_stop(stop)
    stops.insert(new_stops)
    incomplete_count = len(list(find_incomplete_stops()))
    log_info("Stops without complete information: \t%i" % incomplete_count)

def find_incomplete_stops():
    incomplete = db.stops.find({'street': {'$exists': False}})
    return incomplete

# DESTINATIONS
def getDestsDB():
    return dests.find()

def populateDests(new_dests):
    log_info("Populating dests \t(%i)" % len(new_dests))
    for dest in new_dests:
        dests.save(dest)

