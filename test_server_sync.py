from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor

import json

from scraper import UrlFactory
from client import UrlClientFactory
from scraper import UrlFactory

class FakeDeferred:

    def callback(self, input):
        self.callback = 'called back'

class UrlTestSync(unittest.TestCase):

    def test_client_send(self):
        "Tests to make sure that the client sends the correct data to the server"
        d = FakeDeferred()
        client = UrlClientFactory('www.example.com', ['example'], d)
        proto = client.buildProtocol(('localhost', 0))
        transport = proto_helpers.StringTransport()
        proto.makeConnection(transport)
        print "transport", transport.value()
        test_dict = json.dumps({'url': 'www.example.com', 'kw': ['example']})
        self.assertEqual(transport.value(), test_dict)

    def test_client_receive(self):
        "Tests to make sure that the client is receiving data properly"
        d = FakeDeferred()
        client = UrlClientFactory('www.example.com', ['example'], d)
        proto = client.buildProtocol(('localhost', 0))
        transport = proto_helpers.StringTransport()
        proto.makeConnection(transport)
        test_dict = json.dumps({'url': 'www.example.com', 'kw': ['example']})
        proto.dataReceived(test_dict)
        self.assertEqual(proto.data, test_dict)

    def test_client_lost_connection(self):
        "Tests to make sure that the deferred is called upon a lost connection"
        d = FakeDeferred()
        client = UrlClientFactory('www.example.com', ['example'], d)
        proto = client.buildProtocol(('localhost', 0))
        proto.connectionLost('reason')
        self.assertEquals(d.callback, "called back")


    def test_server_receive(self):
        "The server should receive sent data"
        server = UrlFactory()
        server_proto = server.buildProtocol(('localhost', 0))
        test_dict = json.dumps({'url': 'www.example.com', 'kw': ['example']})
        server_proto.transport = proto_helpers.StringTransport()
        server_proto.dataReceived(test_dict)
        self.assertEqual(server_proto.url, 'www.example.com')
        self.assertEqual(server_proto.kw, ['example'])

    def test_server_send(self):
        "sendData method should send the appropriate data"
        server = UrlFactory()
        server_proto = server.buildProtocol(('localhost', 0))
        server_proto.transport = proto_helpers.StringTransport()
        server_proto.sendData('data')
        self.assertEqual(server_proto.transport.value(), 'data')

    def test_server_factory_search_for(self):
        "factory.search_for should return a json dict of found keywords"
        server = UrlFactory()
        test_page = '<html><body><h1>Test Page!</h1></body></html>'
        self.assertEquals(server.search_for(test_page, ['Test']), '{"kw": ["Test"]}')
        self.assertEquals(server.search_for(test_page, ['Test Page']), '{"kw": ["Test Page"]}')
        self.assertEquals(server.search_for(test_page, ['A different page!']), '{"kw": []}')