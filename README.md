wefarm-django
=============
Welcome to WeFarm!

WeFarm was created with Django 1.5.

WeFarm is an online marketplace that processes payments using the WePay API. WeFarm utilizes the WePay API Python SDK to simplify making API calls through WePay.

Full documentation on the WePay API can be found at https://www.wepay.com/developer.

The WePay API Python SDK is open source and can be found at https://github.com/wepay/Python-SDK.

Installation steps:
-------------------
You will need to create a WePAY app. Go to stage.wepay.com or wepay.com to create an application. Add client_id and client_secret settings to wefarm_django/settings.py. Make sure to change the WEPAY.in_production parameter to either True (if your app is in production) or False (if your app is on stage).

Make sure to edit DATABASES setting in settings.py with your correct database information. We use Postgresql.

Install pip if you already don't have it:  
`easy_install pip`

Install virtualenv:  
`pip install virtualenv`

Run the following commands from the root of this project (where manage.py is located):

Create virtualenv:  
`virtualenv venv --no-site-packages`

Activate virtualenv:  
`source venv/bin/activate`

Install all requirements:  
`pip install -r requirements.txt`

Sync database tables:  
`python manage.py syncdb`

Run server:  
`python manage.py runserver`

