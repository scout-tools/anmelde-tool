import csv
import json

model = "basic.ZipCode"

result = []


input_file_coord = csv.DictReader(open('input/zip_code_coord_city_mapping.csv'),
                                  fieldnames=['zip_code', 'city', 'lon', 'lat'], delimiter=",")

for i, event in enumerate(input_file_coord, start=1):
    result.append({
        "model": model,
        "pk": i,
        "fields": {}
    })
    result[i-1]['fields']['id'] = i
    result[i-1]['fields']['zip_code'] = event['zip_code'].zfill(5)
    result[i-1]['fields']['city'] = event['city']
    result[i-1]['fields']['lon'] = event['lon']
    result[i-1]['fields']['lat'] = event['lat']

with open('output/0_zip_codes.json', 'w') as outfile:
    json.dump(result, outfile)
