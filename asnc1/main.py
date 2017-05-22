from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.ioloop

import tornado.web
from tornado.options import define, options

import logging
import time

from async_all import fetch_async, fetch_coroutine, fetch_task  # , callback_me
from async_all import call_blocking

define("port", 8890, help="port", type=int)
URL_Weather = "https://api.thinkpage.cn/v3/weather/now.json?key=j900cje6kieg3pph&location=shanghai&language=zh-Hans&unit=c"
config = {
    # 'template_path': os.path.join(APP_PATH, 'farm/templates'),
    # 'static_path': os.path.join(APP_PATH, 'farm/static'),
    'debug': True
}


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/coroutine", CoroutineHandler),
            (r"/async", AsyncHandler),
            (r"/task", TaskHandler),
            (r"/task2", TaskHandler2),
            (r"/atask", AsyncTaskHandler),
            (r"/block", BlockHandler),
            (r"/interleave", InterleaveHandler),
        ]

        # import pdb        # use pdb to debug is usefully
        # pdb.set_trace()

        super(Application, self).__init__(handlers, **config)


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


def callback_me(response):
    print("callback_me, reponse.body:{}".format(response.body.decode(encoding="utf-8")))
    return response.body


class TaskHandler(tornado.web.RequestHandler):
    def get(self):
        fetch_task(URL_Weather, callback_me)
        # tornado.ioloop.IOLoop.current().spawn_callback(fetch_coroutine, URL_Weather)
        self.write("Hello, world:TaskHandler")


class TaskHandler2(tornado.web.RequestHandler):
    # @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # yield result
        response = yield tornado.gen.Task(self.asynchronous_fetch_callback, URL_Weather, callback_me)
        print("response:{}".format(response))

        self.finish('jas')

    @tornado.gen.coroutine
    def asynchronous_fetch_callback(self, url, cb):
        http_client = AsyncHTTPClient()

        def handle_response(response):
            cb(response)

        http_client.fetch(url, callback=handle_response)


class BlockHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        call_blocking(URL_Weather)
        self.write("Hello, world:BlockHandler")


class AsyncTaskHandler(tornado.web.RequestHandler):
    """
    when we need the result of async task to do something with the result,
    we need write tornado task just like this.
    for example:
    """

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # yield result
        response = yield tornado.gen.Task(self.test, 'magic task test')
        print("response:{}".format(response))

        self.finish('jas')

    @tornado.gen.coroutine
    def test(self, params):
        time.sleep(2)
        return params


class InterleaveHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        fetch_future = fab(10)
        while True:
            chunk = yield fetch_future
            if chunk is None: break
            self.write(chunk)
            fetch_future = fab(10)
            yield self.flush()

    @gen.coroutine
    def fetch_next_chunk(self, max):
        yield fab(max)


@gen.coroutine
def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        # print b
        a, b = b, a + b
        n = n + 1


def start_web():
    logging.debug("start_web ...")
    options.parse_command_line()
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_web()
    # run_bat()
    # result = call_task(URL_Weather, callback_me)
    # print("result:{}".format(result))

    # asynchronous_fetch_callback(URL_Weather, callback_me)
