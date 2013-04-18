from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor

import json

from scraper import UrlFactory
from client import UrlClientFactory


class UrlTestFactory(unittest.TestCase):

    def setUp(self):
        self.server_factory = UrlFactory()
        self.port = reactor.listenTCP(0, self.server_factory, interface='localhost')
        self.portnum = self.port.getHost().port

    def tearDown(self):
        port, self.port = self.port, None
        return port.stopListening()


 
    def test_full_circle(self):
        """Makes sure that the server receives the sent data, 
        finds 'google' in www.google.com, and returns the correct response"""
        d = Deferred()
        def test_kw(returned_data):
            self.assertEqual(json.loads(returned_data), {'kw': ['google']})
        d.addCallback(test_kw)
        client_factory = UrlClientFactory('http://www.google.com', ['google'], d)
        reactor.connectTCP('localhost', self.portnum, client_factory)
        return d
