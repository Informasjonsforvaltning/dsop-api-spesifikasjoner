import csv
import json
import requests
import sys


with open("./banker.csv", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        inputfileName = "./tmp/" + orgNummer + "_Publisher.json"
        with open(inputfileName) as json_file:
            data = json.load(json_file)
            # PUT THE CORRECT URL IN HERE:
            host = ''
            if len(host) == 0:
                sys.exit('You must provide the url to the server!')
            url = host + "/dcat/publisher/" + orgNummer
            headers = {'Content-Type' : 'application/json'}
            # PUT THE COOKIE NAME:VALUE IN HERE
            cookieName = 'devshell-proxy-session'
            cookieValue = ''
            if len(cookieValue) == 0:
                sys.exit('You must provide the cookieValue!')
            cookies={'':''}
            print("Posting to the following url: ", url)
            print("Posting to publisher index the following data:\n", data)
            # Load the publisher by posting the data:
            r = requests.post(url, cookies=cookies, json=data, headers=headers)
            print (orgNummer + ": " + str(r.status_code))
