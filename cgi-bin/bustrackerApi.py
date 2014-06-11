#!/usr/bin/python
from md5 import md5
from datetime import datetime
from urllib2 import urlopen
from json import loads
import log

APIKey = "XILE2BXT513X9D4ESWL39JLNA"
# Generates the key for a bustracker API call
def getKey():
    today = datetime.now() 
    dateString = today.strftime("%Y%m%d%H")
    hashedKey = md5(APIKey + dateString).hexdigest()
    return hashedKey

json_path = "/home/ubuntu/project/server/json/"
stopFile = "%sstops.json" % json_path
stopUrl = "http://ws.mybustracker.co.uk/?module=json&function=getBusStops&key=" + getKey()

servicesFile = "%sservices.json" % json_path
servicesUrl = "http://ws.mybustracker.co.uk/?module=json&function=getServices&key=" + getKey()

destsFile = "%sdests.json" % json_path
destsUrl = "http://ws.mybustracker.co.uk/?module=json&function=getDests&key=" + getKey()

def getTopoID():
    operatorID = "LB"
    url = "http://ws.mybustracker.co.uk/?module=json&function=getTopoId&key=%s&operatorId=%s" % (getKey(), operatorID)
    response = urlopen(url).read()
    topoID = loads(response)['topoId']
    return topoID

def storeUrlContentsAtPath(url, path):
    response = urlopen(url).read()
    outputFile = open(path,"w")
    outputFile.write(response)

# STOPS
def scrapeStopsFromServer():
    log.log_info("Downloading stops")
    storeUrlContentsAtPath(stopUrl,stopFile)

def getStops():
    response = open(stopFile,'r').read()
    stops = loads(response)['busStops']
    return stops

# SERVICES
def scrapeServicesFromServer():
    log.log_info("Downloading services")
    storeUrlContentsAtPath(servicesUrl,servicesFile)

def getServices():
    response = open(servicesFile,'r').read()
    services = loads(response)['services']
    return services

# DESTINATIONS
def scrapeDestsFromServer():
    log.log_info("Downloading dests")
    storeUrlContentsAtPath(destsUrl,destsFile)

def getDests():
    response = open(destsFile,'r').read()
    dests = loads(response)['dests']
    return dests
