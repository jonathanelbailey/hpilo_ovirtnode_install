#!/usr/bin/env python3
# this script requires python3 since python2 can't handle the sslv3 errors that pop
# during handshake

import hpilo
import json
import argparse
import sys

parser = argparse.ArgumentParser(description='take a psssword')
parser.add_argument('--password', required=True)
parser.add_argument('--image-url', required=True)
args = vars(parser.parse_args())

password = args['password']
image_url = args['image-url']

# grabs the ilo information from environments.json.  Currently it's
# only set for one node, so refactoring is required for the script
# to work with more than one machine.
with open('environments.json') as data_file:
    environments_obj = json.load(data_file)

for endpoint in environments_obj['endpoints']:
    try:
        # login to ilo interface and attempt to retrieve fw info
        ilo = hpilo.Ilo(endpoint['hostname'], endpoint['username'], password)
        print(ilo.get_fw_version())
    except hpilo.IloError as e:
        print(e)
        sys.exit(1)
    try:
        # attempt to check cd rom status, insert url based virtual media if able,
        # set one-time boot settings to cdrom, and turn on the machine if it's
        # powered down.  This should start the unattended installation.
        media_status = ilo.get_vm_status(device="CDROM")
        if media_status['image_inserted'] == 'NO':
            ilo.insert_virtual_media(device="CDROM", image_url=image_url)
            ilo.set_vm_status(device="cdrom", boot_option="boot_once")
            if ilo.get_host_power_status() == 'OFF':
                ilo.press_pwr_btn()
    except hpilo.IloError as e:
        print(e)
    sys.exit(1)
