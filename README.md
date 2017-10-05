Vcxsolutiosn - Dev TEST
=======================

A python django solution for the Vcx development test.

Installing
----------

Install the python dependencies in a clean python 3 environment::

    $ pip install -r requirements


Then, run the migrations::

    $ ./vcxsolutions_devtest/manage.py runserver


After it, import the "Tarifas" data sheet::

    $ ./vcxsolutions_devtest/manage.py import_tarifas


Running
-------

To run, type::

    $ ./vcxsolutions_devtest/manage.py runserver


To open the application on the browser, open:

    https://localhost:8000/


Admin
-----

To access the admin to manage imported data open:


    https://localhost:8000/admin/
