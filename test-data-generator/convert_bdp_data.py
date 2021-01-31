import csv
import json

model = "basic.scoutHierarchy"

result = []

with open('output/0_zip_codes.json') as json_file:
    zipCodes = json.load(json_file)


def findIdByCity(plz):
    print(plz)
    for i, event in enumerate(zipCodes, start=0):
        if (zipCodes[i]['fields']['zip_code'] == plz):
            return zipCodes[i]['fields']['id']
    return 1


input_file = csv.DictReader(open('input/bdp_stammesliste.csv'), fieldnames=[
                            'id', 'bezirk', 'ring_name', 'stamm', 'city'], delimiter=";")

for i, event in enumerate(input_file, start=1):
    ii = i + 41
    result.append({
        "model": model,
        "pk": ii,
        "fields": {}
    })

    result[i-1]['fields']['id'] = ii
    result[i-1]['fields']['name'] = event['stamm']
    result[i-1]['fields']['zip_code'] = findIdByCity(event['plz'])
    result[i-1]['fields']['parent_id'] = 1
    result[i-1]['fields']['level_id'] = 5

with open('output/0_bdp.json', 'w') as outfile:
    json.dump(result, outfile)
