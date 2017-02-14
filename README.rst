What is repoze.who-use_beaker
=============================

.. image:: https://travis-ci.org/akissa/repoze.who-use_beaker.svg?branch=master
    :target: https://travis-ci.org/akissa/repoze.who-use_beaker
.. image:: https://codeclimate.com/github/akissa/repoze.who-use_beaker/badges/gpa.svg
   :target: https://codeclimate.com/github/akissa/repoze.who-use_beaker
   :alt: Code Climate

`repoze.who-use_beaker` is a repoze.who_ identifier_ plugin. It is aimed at
replacing repoze.who.plugins.auth_tkt_ in order to store the user data in
`beaker session`_.

The plugin stores a dictionary containing at least `{'repoze.who.userid': userid}`
under key `repoze.who.tkt`.

``UseBeakerPlugin`` takes the following parameters:

- `key_name` (default: `repoze.who.tkt`) - the key name to store the userid
  under::

  >>> userid = session['repoze.who.tkt']

- `session_name` (default: `beaker.session`) - the key name of the beaker
  session in the WSGI environment::

  >>> session = environ['beaker.session']

- `delete_on_logout` (default: `false`) - if `false` then on logout
  ``session['repoze.who.tkt']`` is erased but the other session data stays and
  will be reused during the next session. If you want the session to be
  invalidated pass ``delete_on_logout = True``

- `alsopersist` (default: `['userdata']`) - a sequence of item keys that are
  persisted along to `repoze.who.userid`

Usually you should use `make_plugin` method instead of instantiating
`UseBeakerPlugin` directly::

    >>> from repoze.who.plugins.use_beaker import make_plugin
    >>> plugin = make_plugin(**kw)

In order to properly use the `beaker.session` `repoze.who` (with
`repoze.who-use_beaker`) has to be placed lower in the WSGI stack. Usually this
means that you have to define `repoze.who` in your framework's middleware
configuration higher than beaker session. E.g. (using the factory from
repoze.what-quickstart_)::

    >>> from beaker.middleware import SessionMiddleware
    >>> from repoze.what.plugins.quickstart import setup_sql_auth
    >>> from repoze.who.plugins.use_beaker import make_plugin as make_beaker_plugin

    ... # app definition here

    >>> app = setup_sql_auth(app,
    ...     User, Group, Permission, DBSession,
    ...     # HERE we provide the beaker plugin to be used as the primary identifier
    ...     identifiers=[('use_beaker', make_beaker_plugin())],
    ...     form_plugin=... # The rest of repoze configuration

    ... # more middlewares here

    >>> app = SessionMiddleware(app, config)

Git repository is located at GitHub.com_.

.. _repoze.who: http://docs.repoze.org/who
.. _identifier: http://docs.repoze.org/who/narr.html#identifier-plugins
.. _beaker session: http://beaker.groovie.org/sessions.html
.. _repoze.who.plugins.auth_tkt: http://docs.repoze.org/who/narr.html#repoze.who.plugins.auth_tkt.AuthTktCookiePlugin
.. _repoze.what-quickstart: http://code.gustavonarea.net/repoze.what-quickstart
.. _GitHub.com: http://github.com/kaukas/repoze.who-use_beaker 
