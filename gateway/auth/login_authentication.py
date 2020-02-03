import sys

sys.path.insert(0,'/home/admin1/PycharmProjects/Microservices')
import jwt
from werkzeug.wrappers import Response

from microservices.users.models.datamanagement import Query


def response(success=False, message='something went wrong', data=[]):
    response = {'success': success,
    "message": message,
    "data": data, }
    return response

def is_authenticated(method):
    def authenticate_user(self,request):
        try:
            print(request.path, type(request.path))
            if request.path in ['/api/note']:
                token = request.headers['token']
                payload = jwt.decode(token, "secret", algorithms='HS256')
                id_key = payload['id']
                obj=Query()
                tokenn = obj.get(id_key)
                print(tokenn)
                if token is None:
                    raise ValueError("You Need To Login First")
                return method(self,request)
            else:
                return method(self,request)
        except jwt.ExpiredSignatureError:
                res = response(message="Signature expired. Please log in again.")
                # Response(self).jsonResponse(status=404, data=res)
                Response(res)
        except jwt.DecodeError:
                res = response(message="DecodeError")
                # Response(self).jsonResponse(status=404, data=res)
                Response(res)

        except jwt.InvalidTokenError:
                res = response(message="InvalidTokenError")
                # Response(self).jsonResponse(status=404, data=res)
                Response(res)
    return authenticate_user
