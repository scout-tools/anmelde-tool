# go to backend folder
`cd backend/`

# create venv
`virtualenv venv`

# activate venv
`source venv/bin/activate`

# install
`pip install -r requirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py add_users`

`python manage.py loaddata test-data/*.json`

`python manage.py runserver`

# deactivate venv
`deactivate`

# PostGres for MacOS
`brew install postgresql`