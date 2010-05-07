#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from paste.deploy.converters import asbool
from paste.request import get_cookies
from paste.auth import auth_tkt
from zope.interface import implements

from repoze.who.interfaces import IIdentifier

PERSIST_KEYS = ['userdata']

class UseBeakerPlugin(object):

    implements(IIdentifier)
    
    def __init__(self, key_name='repoze.who.tkt',
                       session_name='beaker.session', delete_on_logout=False,
                       alsopersist = PERSIST_KEYS):
        """Create an identification plugin storing at least the ``identity['repoze.who.userid']`` item
        in a beaker session.

        :param alsopersist: names of additional identity items saved in session. Default: ``alsopersist==['userdata']``
        :type alsopersist: sequence
        """
        
        self.key_name = key_name
        self.session_name = session_name
        self.delete_on_logout = delete_on_logout
        self.persistkeys = alsopersist

    def identify(self, environ):
        """Return identity from Beaker session"""

        s = self._get_beaker(environ)
        identity = s.get(self.key_name, None)
        if identity and identity.get('repoze.who.userid'):
            return identity

    def forget(self, environ, identity):
        """Does not return any headers, just deletes the session entry.
        
        """

        s = self._get_beaker(environ)

        if self.delete_on_logout:
            # When the user logs out remove the session altogether
            s.delete()
        else:
            # Only erase the user name. If the user logs in again he will get
            # the same session
            try:
                del s[self.key_name]
            except:
                pass
            else:
                s.save()

        return []
    
    def remember(self, environ, identity):
        """Does not return any headers, just saves identity to Beaker session
        
        """
        s = self._get_beaker(environ)
        pidentity = s.get(self.key_name)
        if pidentity:
            puserid = pidentity.get('repoze.who.userid')
        else:
            puserid = None

        iuserid = identity.get('repoze.who.userid')
        if puserid != iuserid:
            tkt_identity = {'repoze.who.userid': iuserid}
            for i in self.persistkeys:
                item = identity.get(i)
                if item:
                    tkt_identity[i] = item
            s[self.key_name] = tkt_identity
            s.save()
        return []

    def _get_beaker(self, environ):
        """Returns Beaker session"""
        s = environ.get(self.session_name, None)

        if not s:
            raise ValueError('No Beaker session (%s) in environment' % \
                self.session_name)

        return s

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))

def make_plugin(key_name='repoze.who.tkt', session_name='beaker.session', delete_on_logout=False, alsopersist = PERSIST_KEYS):
    """see :class:`UseBeakerPlugin`"""
    return UseBeakerPlugin(key_name, session_name, delete_on_logout, alsopersist)
