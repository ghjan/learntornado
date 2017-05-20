from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.ioloop

import tornado.web
from tornado.options import define, options

import logging

from async_all import fetch_async, fetch_coroutine

define("port", 8890, help="port", type=int)
URL_Weather = "https://api.thinkpage.cn/v3/weather/now.json?key=j900cje6kieg3pph&location=shanghai&language=zh-Hans&unit=c"


def make_app():
    return tornado.web.Application([
        (r"/coroutine", CoroutineHandler),
        (r"/async", AsyncHandler),
        # (r"/cb", CallbackHandler),
        # (r"/bad", BadcallHandler),
    ])


class AsyncHandler(tornado.web.RequestHandler):
    def get(self):
        tornado.ioloop.IOLoop.current().spawn_callback(fetch_async, URL_Weather)
        self.write("Hello, world:AsyncHandler")


# class CallbackHandler(tornado.web.RequestHandler):
#     def get(self):
#         # fetch_coroutine(URL_Weather)
#         tornado.ioloop.IOLoop.current().spawn_callback(fetch_coroutine, URL_Weather)
#         self.write("Hello, world:CallbackHandler")


class CoroutineHandler(tornado.web.RequestHandler):
    def get(self):
        fetch_coroutine(URL_Weather)
        # tornado.ioloop.IOLoop.current().spawn_callback(fetch_coroutine, URL_Weather)
        self.write("Hello, world:CoroutineHandler")


def start_web():
    options.parse_command_line()
    logging.debug("debug ...")
    options.parse_command_line()
    application = make_app()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_web()
    # run_bat()
    # result = call_task(URL_Weather, callback_me)
    # print("result:{}".format(result))

    # asynchronous_fetch_callback(URL_Weather, callback_me)
