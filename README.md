Tango with Django
=================

This is the repo for my work with following along with the
tutorial [Tango with Django](http://www.tangowithdjango.com/)

As I go along I'll update this README with my progress.

To setup and populate the database for this run

```bash
python manage.py syncdb
python populate_rango.py
```

*  Completed Chapter 3 + Exercises (no problems here)
*  Completed Chapter 4 + Exercises
  * What is the best way of structuring templates? c.f. this
    tutorial and the official one?
*  Completed Chapter 5 + Exercises
*  Completed Chapter 6 + Exercises
  * The URL encoding method seems wrong, perhaps I should see
    how urllib could be used here.
*  Completed Chapter 7 + Exercises
  * I've improved on the example code to always reuturn a HttpRedirect
    when responding to a POST request.
* Completed Chapter 8 + Exercises
  * I've extended the system so that if you attempt to view a restricted
    page and are forced to login when you login you are then redirected to
    the page that you originally requested.
