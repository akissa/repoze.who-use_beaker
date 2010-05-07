#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from beaker.middleware import SessionMiddleware
from webob import Request, Response
from webtest import TestApp
from repoze.who.tests.test_middleware import DummyIdentifier
from test_beaker import TestBaseUseBeakerPlugin

class TestUseBeakerPluginDictionaryImplementation(TestBaseUseBeakerPlugin):

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
        identity_in_session = environ['beaker.session'].get('repoze.who.tkt')
        self.assertEqual(identity_in_session, identity)

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
        identity_in_session = environ['beaker.session'].get('repoze.who.tkt')
        self.assertEqual(identity_in_session, identity)
