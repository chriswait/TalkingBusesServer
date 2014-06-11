#!/usr/bin/python
from csv import reader, writer
from urllib2 import urlopen
from subprocess import call
from os import chdir
from log import log_info


stop_id_index = 1
name_index = 4
street_index = 10
naptan_areas = [620, 627, 628, 629]
naptan_rows = []
csv_path = "/home/ubuntu/project/server/csv/"

def storeUrlContentsAtPath(url, path):
    response = urlopen(url).read()
    outputFile = open(path,"w")
    outputFile.write(response)

def download_naptan_data():
    # Download the NaPTAN archive
    log_info("Downloading NaPTAN data")
    naptan_url = "http://www.dft.gov.uk/NaPTAN/snapshot/NaPTANcsv.zip"
    naptan_archive_path = "%sNaPTANcsv.zip" % csv_path
    storeUrlContentsAtPath(naptan_url, naptan_archive_path)

    # Extract the Stops.csv file
    log_info("Extracting NaPTAN Stops data")
    stops_filename = 'Stops.csv'
    command = "unzip %s %s -d %s" % (naptan_archive_path, stops_filename, csv_path)
    call(command.split())

    # Find rows corresponding to stops we're interested in
    log_info("Extracting useful rows")
    stops_path = "%s%s" % (csv_path,stops_filename)
    stops_file = open(stops_path,'r')
    stops_csv_reader = reader(stops_file)
    useful_rows = []
    for row in stops_csv_reader:
        # add if the ACTOcode starts with one of our areas
        for area in naptan_areas:
            if row[0].startswith(str(area)):
                useful_rows.append(row)

    # Write useful rows to file
    log_info("Storing useful rows")
    naptan_path = '%sNaPTAN.csv' % csv_path
    naptan_file = open(naptan_path,'w')
    naptan_csv_writer = writer(naptan_file)
    naptan_csv_writer.writerows(useful_rows)

    # Remove the zip archive and Stops csv file
    call(['rm',naptan_archive_path,stops_path])

def load_naptan_rows():
    rows = []
    path = '%sNaPTAN.csv' % csv_path
    naptan_stops_file = open(path,"r")
    rows = list(reader(naptan_stops_file))
    return rows

# QUERY NAPTAN DATABASE FOR BETTER STOP NAMES
def addNaptanDataToStop(stop):
    # Ensure NaPTAN rows are loaded
    global naptan_rows
    if not naptan_rows:
        naptan_rows = load_naptan_rows()

    # Find the corresponding row
    for row in naptan_rows:
        if str(row[stop_id_index]) == stop['stopId']:
            name = row[name_index]
            if name: stop['name'] = name

            street = row[street_index]
            if street: stop['street'] = street

            return stop
    return stop
