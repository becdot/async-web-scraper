from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol
from twisted.web.client import getPage

import re
import json

class UrlProtocol(protocol.Protocol):

    def __init__(self):
        self.url = ''
        self.kw = []

    def dataReceived(self, data):
        "Receives data from the client"
        data = json.loads(data)
        "received from client:", data
        self.url = str(data['url'])
        self.kw = [str(kw) for kw in data['kw']]
        self.respond_with_scrape(self.url, self.kw)

    def respond_with_scrape(self, url, kw):
        "Scrapes the url, and adds callbacks for finding keywords, sending data, and stopping"
        d = getPage(url)
        print "got page"
        d.addCallback(self.factory.search_for, kw)
        d.addCallback(self.sendData)
        d.addBoth(self.stop)

    def sendData(self, data):
        "Writes data back to the client"
        print "sending data back to client"
        self.transport.write(data)

    def stop(self, result):
        "Closes the connection"
        print "closing client connection"
        self.transport.loseConnection()

class UrlFactory(Factory):

    protocol = UrlProtocol

    def search_for(self, scraped_page, kw_list): 
        "Uses regular expressions to find keywords in the provided page and returns {'kw': [kw1, kw2...]}"
        kws = [kw for kw in kw_list if re.search(kw, scraped_page) is not None]
        print "found", kws
        return json.dumps(dict(kw=kws))

if __name__ == '__main__':
    reactor.listenTCP(8000, UrlFactory())
    reactor.run()