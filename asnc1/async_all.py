from tornado.httpclient import AsyncHTTPClient
from tornado import gen


async def fetch_async(url):
    http_client = AsyncHTTPClient()
    # response = await http_client.fetch(url)
    response = await gen.convert_yielded(http_client.fetch(url))
    print("fetch_async, reponse.body:{}".format(response.body.decode(encoding="utf-8")))
    return response.body


@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    print("fetch_coroutine, reponse.body:{}".format(response.body.decode(encoding="utf-8")))
    raise gen.Return(response.body)


@gen.coroutine
def fetch_task(url, cb):
    # Note that there are no parens on some_function.
    # This will be translated by Task into
    #   some_function(other_args, callback=callback)
    response = yield gen.Task(asynchronous_fetch_callback, url)
    cb(response)

@gen.coroutine
def asynchronous_fetch_callback(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    return response