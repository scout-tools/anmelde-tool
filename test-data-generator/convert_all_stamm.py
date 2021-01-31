import csv
import json

model = "basic.scoutHierarchy"

result = []

with open('output/0_zip_codes.json') as json_file:
    zipCodes = json.load(json_file)


def findIdByCity(plz):

    for i, event in enumerate(zipCodes, start=0):
        if (zipCodes[i]['fields']['zip_code'] == plz):
            return zipCodes[i]['fields']['id']
    return 1


input_file = csv.DictReader(open('input/stamm_gesamt.csv'), fieldnames=[
                            'stamm', 'parent_id', 'plz'], delimiter=";")

for i, event in enumerate(input_file, start=1):
    ii = i + 81
    result.append({
        "model": model,
        "pk": ii,
        "fields": {}
    })

    result[i-1]['fields']['id'] = ii
    result[i-1]['fields']['name'] = event['stamm']
    result[i-1]['fields']['zip_code'] = findIdByCity(event['plz'])
    result[i-1]['fields']['parent_id'] = int(event['parent_id'], 10)
    result[i-1]['fields']['level_id'] = 5

with open('output/all_stamm.json', 'w') as outfile:
    json.dump(result, outfile)
