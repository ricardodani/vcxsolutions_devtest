Vcxsolutiosn - Dev TEST
=======================

A python django solution for the Vcx development test.

Installing
----------

Install the python dependencies in a clean python 3 environment:

    $ pip install -r requirements.txt

Open on the project:

    $ cd vcxsolutions_devtest

Then, run the migrations:

    $ ./manage.py migrate

After it, import the "Tarifas" data sheet::

    $ ./manage.py import_tarifas


Running
-------

To run, type::

    $ ./manage.py runserver


To open the application on the browser, open:

    http://localhost:8000/


Admin
-----

To access the admin to manage imported data open:


    http://localhost:8000/admin/
