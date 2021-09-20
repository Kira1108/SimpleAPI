from webob import Request, Response
from parse import parse
import inspect
from jinja2 import Environment, FileSystemLoader
import os

class API():
    
    def __init__(self,templates_dir='templates'):
        self.routes = {}

        # 来个东西记录我我所有的模版
        self.templates_env = Environment(
            loaders = FileSystemLoader(os.path.abspath(templates_dir)),
        )

    def template(self, template_name, context = None):
        # 其实吧，就是format string, 把html里面花括号里面的东西给format到
        # 用这个context字典来format就好了
        if context is None:
            context = {}
        return self.templates_env.get_template(template_name).render(**context)

    def add_route(self, path, handler):
        assert path not in self.routes, "Such route already exists"
        self.routes[path] = handler

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

        def wrapper(handler):
            self.add_route(path, handler)
            self.routes[path] = handler
            return handler
        return wrapper