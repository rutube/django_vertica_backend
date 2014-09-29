Django Vertica Backend
======================

A proof-of-concept for connecting Django ORM to HP Vertica database.

[![Build Status](https://travis-ci.org/tumb1er/django_vertica_backend.svg?branch=master)](https://travis-ci.org/tumb1er/django_vertica_backend)

Current status
--------------

* Django ORM SELECT works for some examples
* Django schema dumping works
* Can't run tests on Vertica DB as Vertica doesn't support database creation

Installation
------------

1. install `vertica_python` and `django_vertica_backend`
2. edit `settings.py`
    ```python
    DATABASES = {
      'default': {
        'ENGINE': 'vertica',
        'NAME': 'dash',
        'HOST': 'localhost',
        'PORT': 5433,
        'USER': 'dbadmin',
        'PASSWORD': 'password'
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
