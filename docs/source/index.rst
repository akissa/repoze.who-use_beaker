.. repoze.who.plugins.beaker_tkt documentation master file, created by
   sphinx-quickstart on Sun Apr 19 16:53:44 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`repoze.who.plugins.beaker_tkt` -- Store identity information in Beaker session
####################################################################################

.. module:: repoze.who.plugins.beaker_tkt
.. moduleauthor:: Domen Kožar <domen@dev.si>

:Author: Domen Kožar <domen[ATNOSPAM]dev.si>
:Version: |release|
:Source: http://bitbucket.org/iElectric/repozewhopluginsbeaker_tkt/
:Bug tracker: http://bitbucket.org/iElectric/repozewhopluginsbeaker_tkt/issues/

.. topic:: Overview
	 
    `BeakerAuthTktPlugin` shares the same idea as `CookieAuthTktPlugin` from ``repoze.who.plugins.auth_tkt``. 

		Identifier plugins should call **.remember()** and **.forget()** methods,
		which will force `BeakerAuthTktPlugin` to save/delete identity dictionary to/from Beaker session. 

		After .remember() has been called, `BeakerAuthTktPlugin` will return cached identity
		(on **.identity()** call) from configured Beaker session.

.. note::

	 You have to configure SessionMiddleware if your framework does not use it already.
	
.. warning::

	 This plugin is fresh new and thus should NOT be used in production.

API
***

.. autoclass:: BeakerAuthTktPlugin
	 :members:
	 :undoc-members:

.. autofunction:: make_plugin


Changes
*******
0.1 (12.04.2009)
==================
- initial release

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

