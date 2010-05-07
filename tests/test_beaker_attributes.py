#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_beaker import TestBaseUseBeakerPlugin

class TestUseBeakerPluginAttributes(TestBaseUseBeakerPlugin):

    def test_remember_userdata(self):
        plugin = self._make_one(delete_on_logout=True)
        identity = {'repoze.who.userid': 'chiwawa','userdata':'speedy'}
        environ = self.session_app.request.environ

        r = plugin.identify(environ)
        self.assertEqual(r, None)

        plugin.remember(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r, identity)

        plugin.forget(environ, identity)

    def test_forget_unregistered_data(self):
        plugin = self._make_one(delete_on_logout=True)
        identity = {'repoze.who.userid': 'chiwawa','forgetme':'aliendog'}
        environ = self.session_app.request.environ

        r = plugin.identify(environ)
        self.assertEqual(r, None)

        plugin.remember(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r.get('repoze.who.userid'), identity['repoze.who.userid'])
        self.assertTrue(r.get('forgetme') is None)

        plugin.forget(environ, identity)

    def test_configure_persistent_data(self):
        persistent = ['persistdata','alsopersist']
        plugin = self._make_one(delete_on_logout=True, alsopersist=persistent)
        identity = {'repoze.who.userid': 'chiwawa','persistdata':'forgetmenot', 'alsopersist':'stillhere', 'userdata':'oblivion'}
        environ = self.session_app.request.environ

        r = plugin.identify(environ)
        self.assertEqual(r, None)

        plugin.remember(environ, identity)
        r = plugin.identify(environ)
        self.assertEqual(r.get('repoze.who.userid'), identity['repoze.who.userid'])
        for i in persistent:
            self.assertTrue(r.get(i) == identity[i])
        self.assertTrue(r.get('userdata') is None)

        plugin.forget(environ, identity)
