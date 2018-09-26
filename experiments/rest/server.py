import logging
import urlparse
from flask import Flask, request, make_response
from flask_restful import Api, Resource
from gevent.pywsgi import WSGIServer

logger = logging.getLogger(__name__)


class Resources(Resource):
    settings = {
        'content-type':'application/json'
    }
    api = Api()

    def __init__(self, **kwargs):
        self.handlers = kwargs['handlers']
        self.content_type = kwargs['content-type']
        Resources.settings['content-type'] = self.content_type
        Resources.api = kwargs['api']

    def parse_path(self, path):
        prefix, call = '', ''
        if path:
            try:
                prefix, call = path.rsplit('/', 1)
            except:
                prefix = path
                call = ""
            call = call.replace('-', '_')
            prefix = prefix.replace('-', '_')
        return prefix, call

    @api.representation(settings['content-type'])
    def post(self, path=None):
        method = 'post'
        prefix, call = self.parse_path(path)
        data = request.data
        address = request.remote_addr
        handler = self.handlers[method]
        ack, reply = handler((address, prefix, call, data))
        code = 200 if ack else 500
        resp = make_response(reply, code)
        resp.headers['Content-Type'] = self.content_type
        return resp

    @api.representation(settings['content-type'])
    def get(self, path=None):
        method = 'get'
        prefix, call = self.parse_path(path)
        data = request.data
        address = request.remote_addr
        handler = self.handlers[method]
        ack, reply = handler((address, prefix, call, data))
        code = 200 if ack else 500
        resp = make_response(reply, code)
        resp.headers['Content-Type'] = self.content_type
        return resp

    @api.representation(settings['content-type'])
    def put(self, path=None):
        method = 'put'
        prefix, call = self.parse_path(path)
        data = request.data
        address = request.remote_addr
        handler = self.handlers[method]
        ack, reply = handler((address, prefix, call, data))
        code = 200 if ack else 500
        resp = make_response(reply, code)
        resp.headers['Content-Type'] = self.content_type
        return resp

    @api.representation(settings['content-type'])
    def delete(self, path=None):
        method = 'delete'
        prefix, call = self.parse_path(path)
        data = request.data
        address = request.remote_addr
        handler = self.handlers[method]
        ack, reply = handler((address, prefix, call, data))
        code = 200 if ack else 500
        resp = make_response(reply, code)
        resp.headers['Content-Type'] = self.content_type
        return resp


class WebServer():
    def __init__(self, url, handlers,
                 content_type='application/json'):
        self.path = "/<path:path>"
        self.prefix = '/'
        self.app = app = Flask(__name__)
        self.api = Api(app)
        self.url = url
        self.host = urlparse.urlparse(self.url).hostname
        self.port = urlparse.urlparse(self.url).port
        self.resource = {
            'class': Resources,
            'path': self.path,
            'prefix': self.prefix,
        }
        self.settings = {
            'handlers': handlers,
            'content-type': content_type,
            'api': self.api,
        }
        self.server = None

    def add_resources(self, resource, **kwargs):
        self.api.add_resource(resource['class'], resource['path'], resource['prefix'],
                              resource_class_kwargs=kwargs)

    def init(self, debug=False, reloader=False):
        self.add_resources(self.resource, **self.settings)
        self.server = WSGIServer((self.host, self.port), self.app)
        self.server.serve_forever()



if __name__ == '__main__':
    pass