# import os
# import smtplib
# from email.mime.text import MIMEText
# from dotenv import load_dotenv
# load_dotenv()
# class smtp:
#     """
#     This class is for starting smtp and send email to other accounts.
#     """
#     def __init__(self):
#         self.con = self.connect()
#
#     def connect(self):
#         server = os.getenv("SMTP_EXCHANGE_SERVER")
#         port = os.getenv("SMTP_EXCHANGE_PORT")
#         s = smtplib.SMTP(server, port)
#         s.starttls()
#         s.login(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), os.getenv("SMTP_EXCHANGE_USER_PASSWORD"))
#         return s
#     def send_mail(self, email_id,data):
#         print(email_id)
#         print(data)
#         msg = MIMEText(data)
#         print(msg)
#         self.con.sendmail(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), email_id, msg.as_string())
#         self.con.quit()
