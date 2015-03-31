Restartlet
========

What?
-----
::

.. _gevent: http://www.gevent.org/

	An extension of gevent greenlet and pool that allow a greenlet that exits exceptionally to restart with the same function and arguments it initially started with.

Usage
----------
.. code-block:: python

	from restartlet import RestartableGreenlet

.. code-block:: python
	
	from restartlet import RestartPool


Installing
----------

Through Pypi:

	$ easy_install restartlet

Or the latest development branch from Github:

	$ git clone git@github.com:fiebiga/restartlet.git

	$ cd restartlet

	$ [From virtualenv] python setup.py install 
	$ [No virtualenv] sudo python setup.py install

Support
-------

You may email myself at fiebig.adam@gmail.com
