import json
import ssl
from urllib import request

from django.core.management.base import BaseCommand

from basic.choices import StateChoices
from basic.models import ZipCode

choices = dict(StateChoices.choices)
get_abbr = lambda state: [abbrevation for abbrevation, name in choices.items() if name == state]


class Command(BaseCommand):
    help = 'add all fixtures'

    def handle(self, *args, **options):
        zip_codes: ZipCode = ZipCode.objects.all()
        context = ssl._create_unverified_context()

        for zip_code in zip_codes:
            api_url = f'https://public.opendatasoft.com/api/records/1.0/search/?dataset=georef-germany-postleitzahl&q={zip_code.zip_code}&facet=lan_name'
            contents = request.urlopen(api_url, context=context).read()
            result_json = json.loads(contents)
            state = result_json['facet_groups'][0]['facets'][0]['name']

            abbreviation = get_abbr(state)[0]
            zip_code.state = StateChoices[abbreviation]
            zip_code.save()
