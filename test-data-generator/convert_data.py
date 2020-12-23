import csv
import json

model = "basic.ZipCode"

result = []


input_file = csv.DictReader(open('input/PLZ.csv'), fieldnames=['zipCode', 'city', 'lon', 'lat'], delimiter=";")

for i, event in enumerate(input_file, start=1):
    result.append({
        "model": model,
        "pk": i,
        "fields": {}
    })

    result[i-1]['fields']['zip_code'] = event['zipCode'].zfill(5)
    result[i-1]['fields']['city'] = event['city']
    result[i-1]['fields']['lon'] = event['lon']
    result[i-1]['fields']['lat'] = event['lat']

with open('output/0_zipCodes.json', 'w') as outfile:
    json.dump(result, outfile)
