#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beaker.middleware import SessionMiddleware

from webob import Request, Response
from webtest import TestApp
from repoze.who.tests import Base, DummyIdentifier

class DummyLogger(object):

    def __init__(self):
        self.messages = []

    def debug(self, msg):
        self.messages.append(msg)

def app(environ, start_response):
    """MockApp for testing"""
    req = Request(environ)
    res = Response()
    res.body = 'Just a holder'
    res.content_type = 'text/plain'
    req.environ['paste.testing_variables']['req'] = req
    req.environ['paste.testing_variables']['response'] = res
    return res(environ, start_response)

class FixtureBase(Base):
    def setUp(self):
        self.plugin = self._make_one()
        self.app = TestApp(app, extra_environ={
            'REMOTE_ADDR':'127.0.0.1',
            'repoze.who.logger':DummyLogger(),
        }).get('/')
        self.session_app = TestApp(SessionMiddleware(app), extra_environ={
            'REMOTE_ADDR':'127.0.0.1',
            'repoze.who.logger':DummyLogger(),
        }).get('/')

class TestBeakerAuthTktPlugin(FixtureBase):
    def _getTargetClass(self):
        from repoze.who.plugins.beaker_tkt import BeakerAuthTktPlugin
        return BeakerAuthTktPlugin

    def _make_one(self, **kw):
        plugin = self._getTargetClass()(**kw)
        return plugin

    def test_make_plugin(self):
        from repoze.who.plugins.beaker_tkt import make_plugin
        plugin = make_plugin(key_name='foo', session_name='bar')

        self.assertEqual(plugin.key_name, 'foo')
        self.assertEqual(plugin.session_name, 'bar')

    def test_implements(self):
        from zope.interface.verify import verifyClass
        from repoze.who.interfaces import IIdentifier
        klass = self._getTargetClass()
        verifyClass(IIdentifier, klass)

    def test_usual_workflow(self):
        plugin = self._make_one()
        identity = {'repoze.who.userid': 'chiwawa'}
        environ = self.session_app.request.environ

        r = plugin.identify(environ)
        self.assertEqual(r, None)

        plugin.remember(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, identity)

        plugin.forget(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, None)

    def test_call_twice(self):
        plugin = self._make_one()
        identity = {'repoze.who.userid': 'chiwawa'}
        environ = self.session_app.request.environ

        plugin.forget(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, None)

        plugin.remember(environ, identity)
        plugin.remember(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, identity)
