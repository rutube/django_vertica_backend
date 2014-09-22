Django Vertica Backend
======================

A proof-of-concept for connecting Django ORM to HP Vertica database.

[![Build Status](https://travis-ci.org/tumb1er/django_vertica_backend.svg?branch=master)](https://travis-ci.org/tumb1er/django_vertica_backend)

ODBC setup
----------

1. configure vertica odbc connector in `/etc/vertica.ini`
    ```ini
    [Driver]
    DriverManagerEncoding=UTF-16
    ODBCInstLib=/usr/lib/x86_64-linux-gnu/libodbcinst.so
    ErrorMessagesPath=/opt/vertica/lib64
    LogLevel=4
    LogPath=/tmp
    
    ```
    
2. configure odbc instances in `/etc/odbcinst.ini`
    ```ini
    [HPVertica]
    Description = HP Vertica ODBC Driver
    Driver = /opt/vertica/lib64/libverticaodbc.so
    
    ```
    
3. configure odbc data source in `/etc/odbc.ini`
    ```ini
    [ODBC Data Sources]
    VerticaDB = db database on HP Vertica
    
    [VerticaDB]
    Description = db database on HP Vertica
    Driver = HPVertica
    Database = db_name
    Servername = 127.0.0.1 
    UID = username 
    PWD = 
    Port = 5433
    Locale = en_GB
    
    [ODBC]
    Threading = 1
    
    ```
    
4. check in console:
    ```bash
    $> isql -v VerticaDB
    +---------------------------------------+
    | Connected!                            |
    |                                       |
    | sql-statement                         |
    | help [tablename]                      |
    | quit                                  |
    |                                       |
    +---------------------------------------+

    ```
    
5. connect with pyodbc:
    ```python
    >>> import pyodbc
    >>> pyodbc.connect("DRIVER=HPVertica;HOST=localhost;PORT=5433;DATABASE=")
    <pyodbc.Connection object at 0x7f98991d02d0>
  
    ```
    
6.  now it works in core python ;)
    
Current status
--------------

* Django ORM SELECT works for some examples
* Django schema dumping works
* Can't run tests on Vertica DB as Vertica doesn't support database creation
from odbc connection

Installation
------------

1. install pyodbc
2. configure ODBC for os user
3. edit `settings.py`
    ```python
    DATABASES = {
      'default': {
        'ENGINE': 'vertica',
        'NAME': 'dash',
        'HOST': 'localhost',
        'PORT': 5433,
        'OPTIONS': {
            'DRIVER': 'HPVertica',
        },
      }
    }
    ```

Example
-------

```python
from django.db.models import Sum
from test_app.models import PlatformReport

qs = PlatformReport.objects.filter(date__gte='2014-09-15')
qs = qs.values('platform_id')
qs = qs.annotate(video_views = Sum('video_views'))
print qs[100:500]
```
