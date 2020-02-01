"""
http GET and POST extension
"""
import json
import jwt
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.web.handlers import http
from auth.login_authentication import is_authenticated

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
    @is_authenticated
    def do_create(self, request):

        print(request.headers['token'],'---->sedr')
        # print(dir(request))
        # print(request.path)

        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = str(payload['id'])
        request_data['user_id'] = id
        print(request_data)
        # print(request_data, "request dat1111111111---------------")
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.note_service.create_note(request_data)
            return json.dumps(response)

    @http('DELETE', '/api/note')
    @is_authenticated
    def do_delete(self, request):
        request_data = {}
        token = request.headers['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = str(payload['id'])
        request_data['user_id'] = id
        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.note_service.delete_note(request_data)
            return json.dumps(response)

    @http('PUT', '/api/note')
    @is_authenticated
    def do_update(self, request):
        request_data = json.loads(request.get_data(as_text=True))
        token = request.headers['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = str(payload['id'])
        request_data['user_id'] = id
        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.note_service.update_note(request_data)
            return json.dumps(response)

    @http('GET', '/api/note')
    @is_authenticated
    def do_read(self, request):
        request_data = {}
        token = request.headers['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        id = str(payload['id'])
        request_data['user_id'] = id
        print(request_data)
        with ClusterRpcProxy(config) as cluster_rpc:
            response = cluster_rpc.note_service.read_note(request_data)
            return json.dumps(response)