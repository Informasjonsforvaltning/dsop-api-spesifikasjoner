import csv
import requests
import json

headers={"Accept":"application/json"}

with open("../banker.csv", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[1]
        url = "https://data.brreg.no/enhetsregisteret/api/enheter/" + orgNummer
        r = requests.get(url=url, headers=headers)
        print (orgNummer + ": " + str(r.status_code))
        with open(orgNummer + '_enhetsregisteret.json', 'w') as outfile:
            json.dump(r.json(), outfile)

    # get total number of rows
    print("Total no. of organizations from enhetsregisteret: %d"%(reader.line_num - 1))
