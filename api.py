from webob import Request, Response
from parse import parse
import inspect

class API():
    
    def __init__(self):
        self.routes = {}

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
            
        return None, None

    def default_response(self, response):
        """拿到一个response, 改变一个response的状态"""
        response.status_code = 404
        response.text = "Not found."

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        """真正处理请求的时候是需要匹配path的"""
        response = Response()

        # find a handler
        handler, kwargs = self.find_handler(request_path = request.path)

        # check if the handler if found
        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError('Method not allowed', request.method)

            handler(request, response, **kwargs)

        # if not found, return 404 response
        else:
            self.default_response(response)
 
        return response

    def route(self, path):
        """使用handler这个callable来处理path这个请求
            path和handler这一对东西，注册到API的实例里面
            其实就是存储在self.routers这个字典里面"""

        assert path not in self.routes, "Such route already exists"

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper