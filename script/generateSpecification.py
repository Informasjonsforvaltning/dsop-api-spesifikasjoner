import yaml
import json
import sys
import csv
import copy

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', help="the path to the input csv-file", required=True)
args = parser.parse_args()

print("Reading organizations from: %s"%args.inputfile)

def generateSpec(template, bank):
    # Need to do a deepcopy to actually copy the template into a new object.
    specification = copy.deepcopy(template)
    # Then put the bank-specific values into the specification:
    specification['info']['title'] = template['info']['title'] + ' ' + bank[1]
    # We must recreate the Server object
    specification['servers'] = []
    # Prod url
    if (len(bank[3]) > 0):
        server = {}
        server['url'] = bank[3]
        server['description'] = 'production'
        specification['servers'].append(server)
    # Test url
    if (len(bank[4]) > 0):
        server = {}
        server['url'] = bank[4]
        server['description'] = 'test'
        specification['servers'].append(server)
    return specification

templateFilePath = './script/'
templateFileName = 'Accounts API openapi v1.0.0-RC2.yaml'
with open(templateFilePath + templateFileName) as t:
    template = yaml.safe_load(t)
    with open(args.inputfile, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        # extracting field names through first row
        next(reader, None)
        for bank in reader:
            orgNummer = bank[0]
            orgName = bank[1].replace(' ', '-')
            templateFileName = templateFileName.replace(' ', '_')
            specificationPath = "./specs/"
            specificationFileName = specificationPath + bank[2]
            print('writing specifcation to file', specificationFileName)
            # Validate Prod url:
            if (bank[3].endswith('/')):
                sys.exit('ERROR: Trailing slash in url is not allowed >' + bank[3] + '<')
            # Validate Test url:
            if (bank[4].endswith('/')):
                sys.exit('ERROR: Trailing slash in url is not allowed >' + bank[4] + '<')
            with open(specificationFileName, 'w', encoding="utf-8") as outfile:
                json.dump(generateSpec(template, bank), outfile, ensure_ascii=False, indent=2)
