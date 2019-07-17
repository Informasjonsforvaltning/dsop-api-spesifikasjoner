import csv
import json

def transformToPublisher(data):
    transformed = data
    # TODO Do the actual transformation
    return transformed


with open("../banker.csv", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[1]
        inputfileName = "../01_extract_organizations/" + orgNummer + "_enhetsregisteret.json"
        outputfileName = "../03_load_publishers/" + orgNummer + "_Publisher.json"
        with open(inputfileName) as json_file:
            data = json.load(json_file)
            # Transform the organization object to publihser format:
            with open(outputfileName, 'w', encoding="utf-8") as outfile:
                json.dump(transformToPublisher(data), outfile, ensure_ascii=False)
