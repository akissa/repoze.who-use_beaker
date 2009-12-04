#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from paste.deploy.converters import asbool
from paste.request import get_cookies
from paste.auth import auth_tkt
from zope.interface import implements

from repoze.who.interfaces import IIdentifier


class BeakerAuthTktPlugin(object):

    implements(IIdentifier)
    
    def __init__(self,
                 key_name='repoze.who.tkt',
                 session_name='beaker.session'):
        self.key_name = key_name
        self.session_name = session_name

    def identify(self, environ):
        """Return identity from Beaker session"""

        s = self._get_beaker(environ)
        userid = s.get(self.key_name, None)
        if userid:
            return {'repoze.who.userid': userid}

    def forget(self, environ, identity):
        """Does not return any headers,
        just deletes the session entry.
        
        """

        s = self._get_beaker(environ)

        try:
            del s[self.key_name]
        except:
            pass
        else:
            s.save()

        return []
    
    def remember(self, environ, identity):
        """Does not return any headers,
        just saves identity to Beaker session
        
        """
        s = self._get_beaker(environ)
        userid = s.get(self.key_name)

        iuserid = identity.get('repoze.who.userid')
        if userid != iuserid:
            s[self.key_name] = iuserid
            s.save()
        return []

    def _get_beaker(self, environ):
        """Returns Beaker session"""
        s = environ.get(self.session_name, None)

        if not s:
            raise ValueError('No Beaker session (%s) in environment'\
                % self.session_name)

        return s

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))

def make_plugin(key_name='repoze.who.tkt', session_name='beaker.session'):
    return BeakerAuthTktPlugin(key_name, session_name)
