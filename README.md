###An event-based web scraper that checks to see whether a given keyword appears on the page.

*This project is currently incomplete!*

####Overview
The program uses [Twisted](twistedmatrix.com) to make requests, scrape web pages, and return reponses to the client.

I added a simple web interface using Flask which provides form fields for a url and keyword, and then makes an asynchronous request to the Twisted server under the hood.

####Requirements
- Twisted
- Flask (to use the web interface)

####Usage
To run either the client or the web interface, the scraper must be running first.  

To get the web interface:
```
$ python scraper.py # Listens on port 8000
$ python checker.py # Runs the app on localhost:5000
```
To run a single client task:
```
$ python scraper.py
$ python client.py
```

####How to Test
Testing uses the built-in Twisted testing framework, [trial](http://twistedmatrix.com/trac/wiki/TwistedTrial), which extends the Python unittest module and provides support for evented testing.  Trial comes preloaded with Twisted.

To run tests:
```
trial test_server_sync.py test_server_async.py <any additional test files>
```

####Problems and to-dos
- Flask is not currently well-integrated into the Twisted aspect of the project
    * If a user tries to make a second request, the program will fail with a reactor not restartable error
    * Need to find a better way to make and receive async calls to/from the server
- Poor error handling
    * Need to add errbacks to handle error cases within the program (e.g. if a webpage does not exist)
- Ugly!
    * Use CSS for prettification of the html pages
- Ability to enter multiple keywords
- Better searching (currently does a naive regex search through the scraped html)
- Database integration
- Ability to specify timing
    * User should be able to specify how often they want a search run
    * Program should be able to run searches every so often
- It would be cool to be able to email users if their keyword was found