import yaml
import json
import sys
import csv
import copy

def generateSpec(template, bank):
    # Need to do a deepcopy to actually copy the template into a new object.
    specification = copy.deepcopy(template)
    # Then put the bank-specific values into the specification:
    specification['info']['title'] = template['info']['title'] + ' ' + bank[1]
    specification['servers'][0]['url'] = bank[3]
    specification['servers'][1]['url'] = bank[4]
    return specification

templateFilePath = './specs/'
templateFileName = 'Accounts API openapi v1.0.0-RC2.yaml'
with open(templateFilePath + templateFileName) as t:
    template = yaml.safe_load(t)
    with open("./banker.csv", encoding='utf-8') as f:
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
            with open(specificationFileName, 'w', encoding="utf-8") as outfile:
                json.dump(generateSpec(template, bank), outfile, ensure_ascii=False, indent=2)
