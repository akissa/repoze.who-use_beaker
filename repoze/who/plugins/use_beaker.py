#!/usr/bin/env python
# -*- coding: utf-8 -*-
"repoze.who identifier plugin that persists to beaker sessions"
import re

from zope.interface import implements

from repoze.who.interfaces import IIdentifier

SPLIT_RE = re.compile(r'\s*,\s*')
PERSIST_KEYS = ['userdata', 'tokens']


class UseBeakerPlugin(object):
    "Identify plugin that uses beaker"
    implements(IIdentifier)

    def __init__(  # pylint: disable=dangerous-default-value
            self, key_name='repoze.who.tkt',
            session_name='beaker.session', delete_on_logout=False,
            alsopersist=PERSIST_KEYS):
        """Create an identification plugin storing at least the
        ``identity['repoze.who.userid']`` item in a beaker session.

        :param alsopersist: names of additional identity items saved in
        session. Default: ``alsopersist==['userdata']``
        :type alsopersist: sequence
        """

        self.key_name = key_name
        self.session_name = session_name
        self.delete_on_logout = delete_on_logout
        self.persistkeys = alsopersist

    def identify(self, environ):
        """Return identity from Beaker session"""

        _sess = self._get_beaker(environ)
        identity = _sess.get(self.key_name, None)
        if identity and isinstance(identity, dict) and \
                identity.get('repoze.who.userid'):
            return identity

    def forget(self, environ, identity):  # pylint: disable=unused-argument
        """Does not return any headers, just deletes the session entry.
        """

        _sess = self._get_beaker(environ)

        if self.delete_on_logout:
            # When the user logs out remove the session altogether
            _sess.delete()
        else:
            # Only erase the user name. If the user logs in again he will get
            # the same session
            try:
                del _sess[self.key_name]
            except BaseException:
                pass
            else:
                _sess.save()

        return []

    def remember(self, environ, identity):
        """Does not return any headers, just saves identity to Beaker session
        """
        _sess = self._get_beaker(environ)
        pidentity = _sess.get(self.key_name)
        if pidentity and isinstance(pidentity, dict):
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
            _sess[self.key_name] = tkt_identity
            _sess.save()
        return []

    def _get_beaker(self, environ):
        """Returns Beaker session"""
        _sess = environ.get(self.session_name, None)

        if not _sess:
            raise ValueError(
                'No Beaker session (%s) in environment' % self.session_name)

        return _sess

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))


def make_plugin(  # pylint: disable=dangerous-default-value
        key_name='repoze.who.tkt', session_name='beaker.session',
        delete_on_logout=False, alsopersist=PERSIST_KEYS):
    """see :class:`UseBeakerPlugin`"""
    if isinstance(alsopersist, basestring):
        alsopersist = SPLIT_RE.split(alsopersist)
    return UseBeakerPlugin(
        key_name, session_name, delete_on_logout, alsopersist)
