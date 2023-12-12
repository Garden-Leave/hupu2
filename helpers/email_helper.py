import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config.config import Config
from email.mime.multipart import MIMEMultipart


class EmailHelper:
    mail_user = Config.mail_user
    mail_pass = Config.mail_pass
    server=Config.mail_server
    sender = Config.sender
    receivers = Config.receivers

    def __init__(self):
        #会话
        self.email_session = smtplib.SMTP_SSL(self.server, 465)
        self.email_session.login(self.mail_user,self.mail_pass)
        #消息
        self.email_msg = MIMEMultipart()  # --父类是mimebase然后父类是--->Message, Message有attach方法

    def set_header(self, sub=None, title=None, code=None):
        self.email_msg[sub]=Header(title, code)

    def att(self, payload, type, encoding):
        self.email_msg.attach(MIMEText(payload,type,encoding))


def get_default_email_helper():
    return EmailHelper()