# -*- coding: utf-8 -*-
import logging
from threading import Thread,get_ident
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s.%(msecs)d|%(thread)d|%(filename)s|%(levelname)s|%(message)s'
            , 'datefmt': '%Y-%m-%d %H:%M:%S'}
        , 'detail': {
            'format': '%(asctime)s.%(msecs)d|%(thread)d|%(levelname)s|%(filename)s|%(lineno)d|%(message)s'
            , 'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'class': 'logging.handlers.RotatingFileHandler',  # 将日志消息发送到磁盘文件，并支持日志文件按大小切割
            'filename': "./logs/flask.log",  # 日志输出文件
            'maxBytes': 1024 * 1024 * 1024,  # 文件大小
            'formatter': 'detail',  # 使用哪种formatters日志格式
            'encoding': 'utf-8'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "./logs/flask.log",
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,  # 备份份数
            'formatter': 'detail',
            'encoding': 'utf-8'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "./logs/flask.log",
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        'flask': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'flask.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'spring': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        }
    }
})

logger = logging.getLogger('flask')
# print(id(logger),__name__,get_ident())
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    try:
        logger.info('info info')
        logger.debug('debug info')
        print(1/0)
    except Exception as err:
        print(err)
        logger.error('task1 failed:{}'.format(err),exc_info=True)  # 将异常信息添加到日志消息中
