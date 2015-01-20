# dueling_decimals
Minimum working example of ORA-12704 errors encountered while bulk-creating
nullable Django Decimal fields.

## Failing Tests:
The problem that spawned this repo is that the following tests fails under
Django 1.7.1 and cx_Oracle 5.1.3:
* `test_one_field_set`
* `test_different_fields_set_with_batch_size_35`
* `test_different_fields_set_with_batch_size_2`
* `test_different_fields_set`

### Test failures by Django version
Number of passing tests by version of Django, all with cx_Oracle==5.1.3, since
that's the only one available from PyPI.

| python | Django  | tests |
| ------ | ------  | ----- |
| 2.7.9  | 1.4.12  | 8/8   |
| 2.7.9  | 1.4.18  | 8/8   |
| 2.7.9  | 1.5.0   | 4/8   |
| 2.7.9  | 1.5.12  | 4/8   |
| 2.7.9  | 1.6.10  | 4/8   |
| 2.7.9  | 1.7.1   | 4/8   |
| 3.4.2  | 1.7.1   | 8/8   |

So, it looks like the problem lies in a change made between 1.4 and 1.5...

### Related Django Issues
* https://code.djangoproject.com/ticket/19606

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
You need an Oracle installation on your code-executing machine to make
connections to your Oracle database. I'm going to use
[Oracle Instant Client](http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html).
Note that this requires creating an account on oracle.com and agreeing to their
license terms.

Choose your host architecture on the page linked above, agree to the license
terms if you dare, and download the "Basic" and "SDK" zip files that correspond
to the version of Oracle you're connecting to. If you need to know what version
of Oracle you're connecting to, try running this SQL statement:
```
SELECT * FROM V$VERSION;
```
Follow the installation instructions at the bottom of listing page, including
creating symlinks and setting up `ORACLE_HOME` and `LD_LIBRARY_PATH`.

This might also help: https://gist.github.com/hangtwenty/5547377, though I
didn't need it, other than to know that the "Basic" and "SDK" downloads are
both needed.

Now, you should be able to install `cx_Oracle` as part of the overall
installation:
```
$ git clone github.com/UT-Austin-FIS/dueling_decimals.git
$ cp dueling_decimals/{_local_settings_template.py,local_settings.py}
$ nano dueling_decimals/local_settings.py  # update DATABASES
$ virtualenv venv  # python2.7
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ ./manage.py test dummy
```
