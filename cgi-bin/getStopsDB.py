#!/usr/bin/python
from bustrackerDb import getStopsDB
from bson.json_util import dumps

stops = getStopsDB()
print "Content-type: text/html\n\n"
print dumps(stops)
