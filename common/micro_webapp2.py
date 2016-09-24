import webapp2
import collections

class WSGIApplication(webapp2.WSGIApplication):
    def __init__(self, *args, **kwargs):
        super(WSGIApplication, self).__init__(*args, **kwargs)
        self.router.set_dispatcher(self.__class__.custom_dispatcher)

    @staticmethod
    def custom_dispatcher(router, request, response):
        rv = router.default_dispatcher(request, response)
        if isinstance(rv, basestring):
            rv = webapp2.Response(rv)
        elif isinstance(rv, tuple):
            rv = webapp2.Response(*rv)

        return rv

    def route(self, *args, **kwargs):
        def wrapper(func):
            self.router.add(webapp2.Route(handler=func, *args, **kwargs))
            return func

        return wrapper

    def routes(self, urls, *args, **kwargs):
        if not isinstance(urls, collections.Iterable):
            raise Exception('urls is not a list')
        def wrapper(func):
            for url in urls:
                self.router.add(webapp2.Route(url, handler=func, *args, **kwargs))
            return func
        return wrapper
