# -*- coding: utf-8 -*-

from threading import Thread,get_ident
from config.config import dictConfig
from flask import Flask, jsonify,request,current_app,render_template,redirect,make_response
from flask_cors import CORS, cross_origin   #解决跨域问题会在response header添加策略
from helpers.fetch_parse import fetch_parse
from prometheus_client import start_http_server
from helpers.metrics import c1
import requests, os
from helpers.log_helper import logger1
import traceback

app = Flask('jack')


@app.route('/hupu', methods=['GET'], endpoint='hp')
@cross_origin(origins='*')    # 允许跨域
def get_hp():
    num = int(request.args.get('num'))   # 必须转换为整数
    if num <= 0:
        response = make_response('400：Bad Request, number should be > 0 ', 400, {"header": "test header"})
        logger1.info('400：Bad Request, number should be > 0 status_code: {}'.format(response.status_code))
    else:
        fetch_parse(num)
        # result = list2[0:num*2]
        #print(request.environ.items())
        log_req_record=[request.environ['REQUEST_URI'], request.environ["REQUEST_METHOD"], request.environ['SERVER_PROTOCOL'],request.environ['REMOTE_ADDR'],request.environ['HTTP_USER_AGENT']]
        # logger.warning(log_req_record)
        response = make_response(render_template('result.html'), 200, {"header": "test header"})
        #response = make_response(jsonify(result), 200, {"header1": "jordan"})
        logger1.info('request info: {} status_code: {}'.format(log_req_record, response.status_code))

    return response


@app.route('/hello', methods=['GET'], endpoint='hello')
@cross_origin(origins='*')
def hello():
    log_req_record = [request.environ['REQUEST_URI'], request.environ["REQUEST_METHOD"], request.environ['SERVER_PROTOCOL'],request.environ['REMOTE_ADDR'],request.environ['HTTP_USER_AGENT']]
    response = make_response(render_template('hello.html'), 200, {"header": "test header"})
    logger1.info('request info: {} status_code: {}'.format(log_req_record, response.status_code))
    return response


@app.route('/nginx', methods=['GET'], endpoint='nginx')
@cross_origin(origins='*')
def nginx():
    log_req_record=[request.environ['REQUEST_URI'], request.environ["REQUEST_METHOD"], request.environ['SERVER_PROTOCOL'],request.environ['REMOTE_ADDR'],request.environ['HTTP_USER_AGENT']]
    try:
       response = make_response(requests.get('http://ng.default.svc.cluster.local:8000').text, 200, {"header": "test header"})
       logger1.info('request info: {} status_code: {}'.format(log_req_record, response.status_code))
       return response
    except Exception as e:
        logger1.info(e)



@app.route('/', methods=['GET'], endpoint='root')
@cross_origin(origins='*')
def hello():
    log_req_record=[request.environ['RAW_URI'],request.environ['REMOTE_ADDR'],request.environ['HTTP_USER_AGENT'],request.environ['RAW_URI']]
    logger1.info(log_req_record)
    return redirect('hello')


@app.after_request
def metric_write(response):
    # print('after request')
    c1.labels(hostname=os.getenv('HOSTNAME'), node='node1', code=response.status_code).inc(1)
    # logger.info('prometheus metric request_total written')
    return response


# @app.after_request    #  after request函数接收response后记得再return回去 不然就空了
# def log_response(response):
#     # print('after request')
#     app.logger.warning(f'response data logged in after request func:{response.status}')
#     return response

if __name__ == '__main__':
    start_http_server(9090)
    try:
        app.run()
        logger1.debug('flask main app started')
    except Exception as e:
        logger1.error(f'flask main app start failed:{e}')


