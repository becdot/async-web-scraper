# 1. Input: url, keywords, time interval, (login & password for post sites)
# 2. Makes a request to scraper server (every time interval)
# 3. Output: whether match exists

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site

from flask import Flask, render_template, request, session, redirect, url_for

import sys

from client import UrlClientFactory

events = {}

def make_request(url, kw):
    deferred = Deferred()
    def result(data):
        print "data", data
        return True if data else False
    def stop(result): 
        if reactor.running: 
            reactor.stop()
            return result
        return result
    deferred.addCallback(result)
    deferred.addCallback(stop)
    client = UrlClientFactory(url, [kw], deferred)
    reactor.connectTCP('localhost', 8000, client)
    reactor.run(installSignalHandlers=0)
    return deferred.result

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/checker', methods=['GET', 'POST'])
def checker():
    if request.method == 'GET':
        return render_template('checker.html', events=events)
    else:
        print request.form
        url = str(request.form['url'])
        kw = [str(request.form['keywords'])]
        events[url] = {key:True for key in kw if make_request(url, [kw])}

        return render_template('checker.html', events=events)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
