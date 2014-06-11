#!/usr/bin/python
from naptan import download_naptan_data
import bustrackerDb
import bustrackerApi
import log

key = bustrackerApi.getKey()
api_topo_id = bustrackerApi.getTopoID()

def check_topo_id_new():
    current_topo_id = bustrackerDb.getCurrentTopoID()
    log.log_info("Checking bustracker topology: \tNew=%s, \tCurrent=%s" % (api_topo_id, current_topo_id))
    return (api_topo_id != current_topo_id)

def update():
    # Download new NaPTAN data
    download_naptan_data()

    # Download new json data
    bustrackerApi.scrapeStopsFromServer()
    bustrackerApi.scrapeDestsFromServer()
    bustrackerApi.scrapeServicesFromServer()

    # Clear the database
    bustrackerDb.clear_database()

    # Update services
    services = bustrackerApi.getServices()
    bustrackerDb.populateServices(services)

    # Update stops
    apiStops = bustrackerApi.getStops()
    bustrackerDb.populateStops(apiStops)

    # Update destinations
    dests = bustrackerApi.getDests()
    bustrackerDb.populateDests(dests)

    # Updating database topology id
    bustrackerDb.setCurrentTopoID(api_topo_id)

    log.log_info("Update complete: \tExiting")
    log.email_log()

if __name__ == "__main__":
    log.log_info("\n\nBeginning update")
    if check_topo_id_new():
        log.log_info("Bustracker has updated: \tUpdating DB")
        update()
    else:
        log.log_info("Bustracker has not updated: \tExiting")
