[![Build Status](https://travis-ci.org/geekofalltrades/GEventHttpServer.png?branch=master)](https://travis-ci.org/geekofalltrades/GEventHttpServer)

GEvent HTTP Server
======
###### Based on an HTTP server co-authored with [James White](https://github.com/jwhite007) and [Luke Petschauer](https://github.com/lhp81/)

This is a revision of the [simple HTTP server](https://github.com/geekofalltrades/HttpServer) to use Python's GEvent.
The server accepts only GET requests to its very limited 'webroot' resource directory.
Tests are reused (with minor revisions). The conversion to GEvent was done by me.

Tests are passing:

$ python test_http_server.py
....
Ran 4 tests in 0.003s

OK
$ python test_message_parser.py
..
Ran 2 tests in 0.000s

OK
$ python http_server_tests.py
..
Ran 2 tests in 0.000s

OK
