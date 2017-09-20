#!/usr/bin/env python
# encoding: utf-8

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application

url_map = None


def main():
    APPLICATION_SETTINGS = {}
    app = Application(
        handlers=url_map,
        **APPLICATION_SETTINGS
    )

    http_server = HTTPServer(app)
    http_server.listen()
    IOLoop.current().start()


if __name__ == '__main__':
    main()
