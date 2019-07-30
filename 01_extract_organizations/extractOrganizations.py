import csv
import requests
import json

headers={"Accept":"application/json"}

with open("./banker.csv", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        url = "https://data.brreg.no/enhetsregisteret/api/enheter/" + orgNummer
        r = requests.get(url=url, headers=headers)
        print (orgNummer + ": " + str(r.status_code))
        print(r.json())
        with open("./tmp/" + orgNummer + '_enhetsregisteret.json', 'w', encoding="utf-8") as outfile:
            json.dump(r.json(), outfile, ensure_ascii=False, indent=4)

    # get total number of rows
    print("Total no. of organizations from enhetsregisteret: %d"%(reader.line_num - 1))
