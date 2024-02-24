import logging
from logging.config import dictConfig

class Config:
    target_url = 'https://bbs.hupu.com/search?q=%E6%9D%9C%E5%85%B0%E7%89%B9&topicId=240&sortby=light&page=1'

    mail_server = "smtp.qq.com"  # 设置服务器
    mail_user = "457638186@qq.com"  # 用户名
    mail_pass = ""  # 口令
    sender='457638186@qq.com'
    receivers=['457638186@qq.com']


class DB_Config:
    host = '192.168.1.3'
    port = '3306'
    user = 'root'
    password = '111'
    database = 'f1'


#
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': "[%(asctime)s] %(levelname)s in %(module)s line-%(lineno)s: %(message)s",
#     }},
#     'handlers': {
#         'wsgi-file': {
#         'class': 'logging.handlers.RotatingFileHandler',
#         'filename': "./logs/flask.log",
#         'level': 'DEBUG',
#         'maxBytes': 1024 * 1024 * 5,
#         'backupCount': 5,
#         'formatter': 'default',
#         'encoding': 'utf-8'
#
#     },
#         'console': {
#             'class': 'logging.StreamHandler',
#             'level': 'DEBUG',
#             'formatter': 'default'
#         }
#
#     },
#     'root': {
#         'level': 'DEBUG',
#         'handlers': ['wsgi-file','console']
#     }
# })
# 下面这个字典里的配置 因为指定了名字叫root,所以其实只是在修改RootLogger这个特殊logger的属性，flask帮忙生成的名字叫jack的logger 并没有得到配置，默认只有stderr
#，此时你可以把jack这个logger对象也声明到字典里
#但是你可以通过向jack,先声明对象再添加的方式 给它指定上 app.logger.addhandler(handler1对象) 一次一个， 但是你会发现你用app.logger的都能输出到你指定的handler了，
#但是serving里面调用的不会写到你这handler，因为它没走这个logger，走的是werkzeug这个logger，那个logger默认只有sys.stderr这个console输出。
