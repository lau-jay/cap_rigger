#!/usr/bin/env python
# encoding: utf-8

import os

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application

import aiomysql

from app import DBCONFIG
from app import APPCONFIG


class App(Application):
    def __init__(self, pool, **settings):
        self._pool = pool
        super().__init__(**settings)

    @property
    def pool(self):
        return self._pool


async def init_db_pool(loop):

    return await aiomysql.create_pool(
        loop=loop,
        host=DBCONFIG['host'] or '127.0.0.1',
        port=DBCONFIG['port'] or 3306,
        user=DBCONFIG['user'] or 'root',
        password=DBCONFIG['pwd'] or 'root',
        db=DBCONFIG['db'] or 'test')


def init_app(pool):
    settings = {}
    app = App(pool, **settings)
    return app


def main():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    }
    loop = IOLoop.current()
    pool = loop.run_until_complete(init_db_pool(loop=loop))
    app = init_app(
        pool=pool, handlers=[], debug=APPCONFIG['debug'], **settings)

    http_server = HTTPServer(app)
    http_server.listen()
    loop.start()


if __name__ == '__main__':
    main()
