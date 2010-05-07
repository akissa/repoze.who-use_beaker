#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_beaker import TestBaseUseBeakerPlugin

class TestUseBeakerPluginStringImplementation(TestBaseUseBeakerPlugin):

    def test_usual_workflow(self):
        plugin = self._make_one(delete_on_logout=True)
        identity = {'repoze.who.userid': 'chiwawa'}
        environ = self.session_app.request.environ

        r = plugin.identify(environ)
        self.assertEqual(r, None)

        plugin.remember(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, identity)
        # the following is implementation dependant
        user_in_session = environ['beaker.session'].get('repoze.who.tkt')
        self.assertEqual(user_in_session, 'chiwawa')

        plugin.forget(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, None)
        # Session is completely empty (new)
        self.assertEquals(str(environ['beaker.session']), '{}')

    def test_call_twice(self):
        plugin = self._make_one()
        identity = {'repoze.who.userid': 'chiwawa'}
        environ = self.session_app.request.environ

        plugin.forget(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, None)
        self.assert_(not environ['beaker.session'].has_key('repoze.who.tkt'))

        plugin.remember(environ, identity)
        plugin.remember(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, identity)
        # the following is implementation dependant
        user_in_session = environ['beaker.session'].get('repoze.who.tkt')
        self.assertEqual(user_in_session, 'chiwawa')
