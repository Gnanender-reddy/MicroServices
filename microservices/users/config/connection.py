import smtplib

import mysql
import os
from dotenv import load_dotenv
import mysql.connector
import redis
load_dotenv()

def singleton(myClass):
    instances = {}
    def get_instance(*args, **kwargs):
        if myClass not in instances:
            instances[myClass] = myClass(*args, **kwargs)
        return instances[myClass]
    return get_instance

@singleton
class Connection:
    def __init__(self):
        self.conn = self.connect()
        self.mycursor = self.conn.cursor()

    def connect(self):
        mydb = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER_DB"),
            passwd=os.getenv("PASSWD"),
            database=os.getenv("DATABASE"))

        return mydb

    def redis_conn(self):
        r = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=6379
            )
        return r

    # def smtp_conn(self):
    #     server = os.getenv("SMTP_EXCHANGE_SERVER")
    #     port = os.getenv("SMTP_EXCHANGE_PORT")
    #     s = smtplib.SMTP(server, port)
    #     s.starttls()  # start TLS for security
    #     s.login(os.getenv("SMTP_EXCHANGE_USER_LOGIN"),
    #             os.getenv("SMTP_EXCHANGE_USER_PASSWORD"))  # Authentication and login
    #     return s

    def run_query(self, query):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def execute(self, query):
        self.mycursor.execute(query)
        self.conn.commit()