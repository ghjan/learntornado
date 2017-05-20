from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.ioloop

import tornado.web
from tornado.options import define, options

import logging

define("port", 8889, help="port", type=int)
URL_Weather = "https://api.thinkpage.cn/v3/weather/now.json?key=j900cje6kieg3pph&location=shanghai&language=zh-Hans&unit=c"


@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    print("fetch_coroutine, reponse.body:{}".format(response.body.decode(encoding="utf-8")))
    raise gen.Return(response.body)


class FetchHandler_coroutine(tornado.web.RequestHandler):
    def get(self):
        fetch_coroutine(URL_Weather)
        # tornado.ioloop.IOLoop.current().spawn_callback(fetch_coroutine, URL_Weather)
        self.write("Hello, world:FetchHandler_coroutine")


def make_app():
    return tornado.web.Application([
        # (r"/", MainHandler),
        # (r"/good", GoodcallHandler),
        # (r"/bad", BadcallHandler),
        (r"/coroutine", FetchHandler_coroutine),
    ])


def start_web():
    options.parse_command_line()
    logging.debug("debug ...")
    options.parse_command_line()
    application = make_app()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


def asynchronous_fetch_callback(url, callback):
    http_client = AsyncHTTPClient()

    def handle_response(response):
        print("asynchronous_fetch_callback, response.body:{}".format(response.body))
        callback(response.body)

    http_client.fetch(url, callback=handle_response)


@gen.coroutine
def call_task(url, callback):
    # Note that there are no parens on some_function.
    # This will be translated by Task into
    #   some_function(other_args, callback=callback)
    yield gen.Task(asynchronous_fetch_callback, url, callback)


def callback_me(response):
    print("response.body:{}".format(response.body))
    return response.body


async def fetch_async(url):
    http_client = AsyncHTTPClient()
    # response = await http_client.fetch(url)
    response = await gen.convert_yielded(http_client.fetch(url))
    return response.body


if __name__ == "__main__":
    start_web()
    # result = call_task(URL_Weather, callback_me)
    # print("result:{}".format(result))

    # asynchronous_fetch_callback(URL_Weather, callback_me)
    # tornado.ioloop.IOLoop.current().spawn_callback(fetch_coroutine, URL_Weather)
