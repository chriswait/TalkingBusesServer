#!/usr/bin/python
import logging
from datetime import datetime
from subprocess import call
from os import chmod

setup = 0
logs_path = "/home/ubuntu/project/server/logs/"
datestring = datetime.now().date().isoformat()
update_log_file_path = "%supdate_%s.log" % (logs_path, datestring)

def setup_log():
    logging.basicConfig(filename=update_log_file_path, level=logging.DEBUG, format='%(asctime)s %(message)s')

def log_info(info):
    print info
    if not setup:
        setup_log()
    logging.info(info)

def log_error(error):
    print error
    if not setup:
        setup_log()
    logging.error(error)

def email_log():
    command = "sendemail -v -f talkingbuses@gmail.com -t chriswait91@gmail.com -u Bustracker Update -o message-file=%s tls=yes -s smtp.gmail.com -xu talkingbuses -xp bustracker" % update_log_file_path
    call(command.split())
