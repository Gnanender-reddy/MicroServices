import sys

import jwt

from nameko.rpc import rpc



sys.path.insert(0,'/home/admin1/PycharmProjects/Microservices')
from microservices.users.models.datamanagement import Query
from microservices.users.config.redis_connection import RedisService

class User(object):  # This class is used to handle a services of user
    name = "user_service"

    @rpc
    def user_login(self, data):
        obj = Query()
        email = data['email']
        # responce = {'success': True, 'data': [], 'message': "", 'data': ''}
        if obj.checking_email(email):
            id, email = obj.read_email(email=email)
            if id:
                payload = {'id': id}
                # 'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)}
                encoded_token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
                print(id, encoded_token)
                obj.set(id,encoded_token)
                print(obj.get(id), '------------->r.get')
                # redis_obj = RedisService()
                # redis_obj.set(id, encoded_token)
                # print(redis_obj.get(id), '------------->r.get')
                response = {'success': True, 'data': [], 'message': "Login Successful","token":encoded_token}
                # responce.update({'success': True, 'data': [], 'message': "Successfully login", "token": encoded_token})
                return response
        else:
            response = {'success': False, 'data': [], 'message': "Email not in valid format"}
            # res = response(message="Login unsuccessfull")
            return response
        # encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
        # if obj.email_validate(data['email']):
        #     result = obj.get_cache(encoded_jwt)
        #     print(data)
        #     if result:
        #         payload = {'id': id,}
        #         encoded_token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
        #         response = {'success': True, 'data': [], 'message': "Login Successful"}
        #         return response
        #     else:
        #         response = {'success': False, 'data': [], 'message': "Not a Register User"}
        #         return response
        # else:
        #     response = {'success': False, 'data': [], 'message': "Email not in valid format"}
        #     return response

    @rpc
    def user_register(self, data):
        obj = Query()
        encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
        result_passwd = obj.password_validate(data)
        result_email = obj.email_validate(data['email'])
        if result_email and result_passwd:
            result = obj.get_cache(encoded_jwt)
            if result:
                response = {'success': False, 'data': [], 'message': "Email already exist"}
                return response
            else:
                obj.put_cache(data)
                obj.registration(data)
                response = {'success': True, 'data': [], 'message': "Successfully Registered"}
                return response
        else:
            response = {'success': False, 'data': [], 'message': "not a valid email or password and cnf "
                                                                 "password not match"}
            return response

    @rpc
    def forget_password(self, data):
        obj = Query()
        obj.send_mail(data['email'])
        response = {'success': False, 'data': [], 'message': "Message sent Successfully"}
        return response
        # encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
        # if obj.get_cache(encoded_jwt):
        #     response = {'success': False, 'data': [], 'message': "Not a Register User"}
        #     return response
        # else:
        #     obj.send_mail(data['email'])
        #     # s = smtp()
        #     # s.start()  # start TLS for security
        #     # s.login()  # Authentication and login
        #     # s.send_mail(data['email'])  # sending the mail
        #     response = {'success': False, 'data': [], 'message': "Message sent Successfully"}
        #     return response