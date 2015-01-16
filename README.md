# dueling_decimals
Minimum working example of ORA-12704 errors encountered while bulk-creating
nullable Django Decimal fields.

setup: 
Create a new Oracle schema and add it to DATABASES in `local_settings.py`. Then,

```
$ virtualenv venv  # python2.7
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt  # cx_Oracle requires an Oracle installation :/
(venv) $ ./manage.py test dummy
```
