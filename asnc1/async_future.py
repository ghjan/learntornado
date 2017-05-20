from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future

'''
 Error handling is more consistent since the Future.result method can simply raise an exception
 (as opposed to the ad-hoc error handling common in callback-oriented interfaces),
 and Futures lend themselves well to use with coroutines.
'''
def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    # IOLoop.add_future
    return my_future
