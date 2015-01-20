# dueling_decimals
Minimum working example of ORA-12704 errors encountered while bulk-creating
nullable Django Decimal fields.


## Failing Tests:

* `test_one_field_set`
* `test_different_fields_set_with_batch_size_35`
* `test_different_fields_set_with_batch_size_2`
* `test_different_fields_set`

## Setup: 
Create a new Oracle 11gR2 schema to run tests against. Installing cx_Oracle
requires a local Oracle installation, which the PyPE 27.7.0 VM provides.

Continue on, either with PyPE or virtualenv.

### PyPE (the UT-specific Django environment)
If you're using the 27.7.0 VM...

```
$ cd /pype
$ git clone github.com/UT-Austin-FIS/dueling_decimals.git
$ export PYTHONPATH=$PYTHONPATH:/pype/dueling_decimals
$ cp dueling_decimals/{_local_settings_template.py,local_settings.py}
$ nano dueling_decimals/local_settings.py  # update DATABASES
$ python manage.py test dummy
```

### virtualenv
(This is untested...)

You need an Oracle installation on your code-executing machine to make
connections to your Oracle database. I'm going to use
[Oracle Instant Client](http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html).
Find, download, and install the appropriate version for your host architecture
and database version. Follow the installation instructions, including setting
up `ORACLE_HOME` and `LD_LIBRARY_PATH`. If you need to know what version of
Oracle you're connecting to, try running this SQL statement:
```
SELECT * FROM V$VERSION;
```

```
$ git clone github.com/UT-Austin-FIS/dueling_decimals.git
$ cp dueling_decimals/{_local_settings_template.py,local_settings.py}
$ nano dueling_decimals/local_settings.py  # update DATABASES
$ virtualenv venv  # python2.7
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt  # cx_Oracle requires an Oracle installation :/
(venv) $ ./manage.py test dummy
```
