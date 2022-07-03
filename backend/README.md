# go to backend folder
`cd backend/`

# create venv
`virtualenv venv`

# activate venv
`source venv/bin/activate`

Mac, Linux: ( `pipenv install` )
             `pipenv shell`

# install
`pip install -r requirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py add_users`

Mac, Linux:
`python manage.py loaddata data/main/*.json`
`python manage.py loaddata data/test/*.json`

Inspi Mac, Linux:
`python manage.py loaddata data/inspi/master-data/*.json`
`python manage.py loaddata data/inspi/test-data/*.json`

Windows: `python manage.py add_fixtures test-data`

`python manage.py runserver`

# deactivate venv
`deactivate`

# PostGres for MacOS
`brew install postgresql`

# Dumpdata
Contenttypes: `python -Xutf8 manage.py dumpdata contenttypes.contenttype -o data\main\0_contenTypes.json`

Descriptions: `python -Xutf8 manage.py dumpdata basic.description -o data\main\0_contenTypes.json`

Basic: `python -Xutf8 manage.py dumpdata basic --exclude=basic.ZipCode --exclude=basic.description --exclude=basic.ScoutOrgaLevel --exclude=basic.ScoutHierarchy -o data\test\1_completeBasic.json`

Email: `python -Xutf8 manage.py dumpdata email_services -o data\test\2_completeEmail.json`

Event: `python -Xutf8 manage.py dumpdata event -o data\test\3_completeEvent.json`


# Test mails
`send_mail('Subject here', 'Here is the message.', 'test@anmelde-tool.de', ['robert@hratuga.de'], fail_silently=False)`

# save new packages
`pip freeze > requirements.txt`
