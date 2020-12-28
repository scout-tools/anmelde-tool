import csv
import json

model = "basic.scoutHierarchy"

result = []

with open('output/0_zip_codes.json') as json_file:
    zipCodes = json.load(json_file)


def findIdByZipCode(zipCode):
    for i, event in enumerate(zipCodes, start=0):
        if (zipCodes[i]['fields']['zip_code'] == zipCode):
            return zipCodes[i]['fields']['id']
    return -1


input_file = csv.DictReader(open(
    'input/dpbm.csv'), fieldnames=['name', 'zip_code', 'ring_name', 'ring_id'], delimiter=";")

for i, event in enumerate(input_file, start=1):
    ii = i + 14
    result.append({
        "model": model,
        "pk": ii,
        "fields": {}
    })

    result[i-1]['fields']['id'] = ii
    result[i-1]['fields']['name'] = event['name']
    result[i -
           1]['fields']['zip_code'] = findIdByZipCode(event['zip_code'].zfill(5))
    result[i-1]['fields']['parent_id'] = int(event['ring_id'])
    result[i-1]['fields']['level_id'] = 5

with open('output/0_dpbm.json', 'w') as outfile:
    json.dump(result, outfile)
