from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor

import json

from scraper import UrlFactory

class UrlClientProtocol(Protocol):

    def __init__(self):
        self.data = ''

    def dataReceived(self, data):
        "Receives data from the server"
        self.data += data

    def connectionMade(self):
        "Sends the url and keywords (provided by Factory) to the server"
        to_send = json.dumps({'url': self.factory.url, 'kw': self.factory.kw})
        print "sending to server", to_send
        self.transport.write(to_send)

    def connectionLost(self, reason):
        "Calls the callback provided by the factory initialization -- important for testing!"
        print "Received", self.data
        self.factory.d.callback(self.data)

class UrlClientFactory(ClientFactory):

    protocol = UrlClientProtocol

    def __init__(self, url, kw, d):
        self.url = url
        self.kw = kw
        self.d = d


if __name__ == '__main__':
    d = Deferred()
    def boom(data): print "boom!", data
    d.addCallback(boom)
    reactor.connectTCP('localhost', 8000, UrlClientFactory('http://www.google.com', ['google'], d))
    reactor.run()
