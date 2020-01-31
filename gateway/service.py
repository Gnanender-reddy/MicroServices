"""
http GET and POST extension
"""
import json

import jwt
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.web.handlers import http


config = {
'AMQP_URI': 'amqp://guest:guest@localhost',
}

class HttpService(object):
    name = "http_services"

    @http('POST', '/login')
    def get_login(self, request):
        request_data = json.loads(request.get_data(as_text=True))
        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.user_service.user_login(request_data)
            return json.dumps(response)

    @http('POST', '/register')
    def get_register(self, request):
        request_data = json.loads(request.get_data(as_text=True))
        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.user_service.user_register(request_data)
            return json.dumps(response)

    @http('POST', '/forget')
    def get_forget(self, request):
        request_data = json.loads(request.get_data(as_text=True))
        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.user_service.forget_password(request_data)
            return json.dumps(response)

    @http('POST', '/api/note')
    def do_create(self, request):
        request_data = json.loads(request.get_data(as_text=True))
        token = request_data['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = str(payload['id'])
        request_data['user_id'] = id
        print(request_data, "request dat1111111111---------------")
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.note_service.create_note(request_data)
            return json.dumps(response)

    @http('DELETE', '/api/note')
    def do_delete(self, request):
        request_data = json.loads(request.get_data(as_text=True))
        token = request_data['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = str(payload['id'])
        request_data['user_id'] = id

        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.note_service.delete_note(request_data)
            return json.dumps(response)

    @http('PUT', '/api/note')
    def do_update(self, request):
        request_data = json.loads(request.get_data(as_text=True))
        token = request_data['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = str(payload['id'])
        request_data['user_id'] = id

        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.note_service.update_note(request_data)
            return json.dumps(response)

    @http('GET', '/api/note')
    def do_read(self, request):
        request_data = json.loads(request.get_data(as_text=True))
        token = request_data['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = str(payload['id'])
        request_data['user_id'] = id

        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.note_service.read_note(request_data)
            return json.dumps(response)