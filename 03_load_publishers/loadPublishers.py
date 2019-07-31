import csv
import json
import requests


with open("./banker.csv", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        inputfileName = "./tmp/" + orgNummer + "_Publisher.json"
        with open(inputfileName) as json_file:
            data = json.load(json_file)
            # Load the publisher by posting the data:
            url = "https://" + "dittogdatt" + "/dcat/publisher/" + orgNummer
            headers = {'Content-Type' : 'application/json'}
            print("Posting to the following url: ", url)
            print("Posting to publisher index the following data:\n", data)
            r = requests.post(url, json=data, headers)
            print (orgNummer + ": " + str(r.status_code))
