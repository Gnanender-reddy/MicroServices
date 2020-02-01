import os
import re
from email.mime.text import MIMEText
import jwt
from nameko.rpc import rpc
from microservices.users.config.connection import Connection
from microservices.users.vendor.smtp import smtp


class Query:
    """Summary:- This class is used to form connection with the database and perform operation update, add and check
    entry into the database
    """
    name = "data_service"

    def __init__(self):
        self.c = Connection()
        self.r = self.c.redis_conn()
        self.s = self.c.smtp_conn()

    @rpc
    def registration(self, data):
        print(type(data['password']))
        # This function is used to store a registration entry into database using sql command
        query = "INSERT INTO users(email,password) VALUES ('" + data['email'] + "'," + data['password'] + ") "
        self.c.execute(query)
        # self.mydbobj.execute(query)

    @rpc
    def email_exist(self, data):  # This function is used to check email already exist in database using sql query
        query = "SELECT email from users where email = '" + data['email'] + "'"
        result = self.c.run_query(query)
        # result = self.mydbobj.run_query(query)
        if len(result):
            return False
        else:
            return True

    @rpc
    def user_exist(self, data):
        # This function is used to check valid user  using sql query for login according return true or false value
        result = jwt.decode(data, 'secret', algorithms=['HS256'])
        query = "SELECT * from user where email = '" + result['some']['email'] + "' and password = '" + \
                result['some']['password'] + "'"
        result = self.c.run_query(query)
        # result = self.mydbobj.run_query(query)
        if len(result):
            return False
        else:
            return True

    @rpc
    def email_validate(self, email):
        # This function is used to check email is in valid format or not and return true or false value
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    @rpc
    def password_validate(self, data):
        # This function is used to check psw and cnf psw is in valid or not and return true and false value
        if data['password'] == data['confirmpassword']:
            return True
        else:
            return False

    @rpc
    def update_password(self, email, data):  # This function is used to update a password in database using sql query
        query = " UPDATE users SET password = '" + data + "'WHERE  email = '" + email + "' "
        self.c.execute(query)
        # self.mydbobj.execute(query)

    @rpc
    def send_mail(self, email):
        encoded_jwt = jwt.encode({'email': email}, 'secret', algorithm='HS256').decode("UTF-8")
        data = f"http://localhost:9090/forget/?new={encoded_jwt}"
        # s=smtp()
        # s.send_mail(email,data)
        msg = MIMEText(data)
        self.s.sendmail(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), email, msg.as_string())
        self.s.quit()

    @rpc
    def put_cache(self, data):
        self.r.hmset(data['email'], data)

    @rpc
    def get_cache(self, data):
        result = jwt.decode(data, 'secret', algorithms=['HS256'])
        x = self.r.hkeys(result['some']['email'])
        return len(x)
    @rpc
    def read_email(self, email=None):
        id = None
        sql = "SELECT email,id FROM users where email = '" + email + "'"
        result = self.c.run_query(sql)
        print(result)
        print(email, id)
        if result is not None:
            email, id = result[0]
            return id, email
        else:
            return None
    @rpc
    def checking_email(self,email):
        query="select * from users where email='"+email+"'"
        result=self.c.run_query(query)
        if result:
            return True
        else:
            return False

    @rpc
    def set(self, key, value):
        self.r.set(key, value)

    @rpc
    def get(self, key):
        print(key)
        value = self.r.get(key)
        return value