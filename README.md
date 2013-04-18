###Project to get my feet wet with [Twisted](twistedmatrix.com) and learn more about event-driven programming.  *This project is currently incomplete!*

####Overview
The Twisted client makes an asynchronous request to a Twisted server with a url and keyword.  The server scrapes the webpage, searches for the keyword within the scraped html, and sends a response back to the client about whether the url contained that keyword.

I also added a very minimal Flask application (checker.py), which lets users submit a url and keyword, makes requests to the Twisted server, and then displays the result of the search.

####Useage
Twisted must be installed to run client.py and scraper.py
Flask must be installed to run checker.py

For either the client or the flask app, scraper must be running first.  Enter python scraper.py on the command line.
To run the flask app, run python checker.py and visit http://localhost:5000.

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