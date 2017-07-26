#!/usr/bin/env python

import hpilo
import json
import argparse
import sys

parser = argparse.ArgumentParser(description='take a psssword')
parser.add_argument('--password', required=True)
args = vars(parser.parse_args())

password = args['password']

with open('environments.json') as data_file:
    environments_obj = json.load(data_file)

for endpoint in environments_obj['endpoints']:
    try:
        ilo = hpilo.Ilo(endpoint['hostname'], endpoint['username'], password, ssl_version=None)
        print(ilo.get_fw_version())
    except hpilo.IloError as e:
        print(e)
        sys.exit(1)


