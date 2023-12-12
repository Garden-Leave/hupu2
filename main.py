# -*- coding: utf-8 -*-

from threading import Thread,get_ident
from config.config import dictConfig
from flask import Flask, jsonify,request,current_app,render_template,redirect
from flask_cors import CORS, cross_origin   #解决跨域问题会在response header添加策略
from helpers.fetch_parse import fetch_parse
from prometheus_client import start_http_server
from helpers.metrics import c1


app = Flask('jack')

@app.route('/hupu', methods=['GET'], endpoint='hp')
@cross_origin(origins='*')    # 允许跨域
def get_hp():
    num = int(request.args.get('num'))
    app.logger.info(num)
    list2 = fetch_parse()
    # app.logger.info(list2)
    result = list2[0:num*2]
    log_req_record=[request.environ['RAW_URI'],request.environ['REMOTE_ADDR'],request.environ['HTTP_USER_AGENT'],request.environ['RAW_URI']]
    app.logger.warning(log_req_record)
    return jsonify(result)


@app.route('/hello', methods=['GET'], endpoint='hello')
@cross_origin(origins='*')
def hello():

    return render_template('hello.html')


@app.route('/', methods=['GET'], endpoint='root')
@cross_origin(origins='*')
def hello():
    return redirect('hello')


@app.after_request
def metric_write(response):
    # print('after request')
    c1.labels(pod='pod1', node='node1', code=response.status_code).inc(1)
    return response




# @app.after_request    #  after request函数接收response后记得再return回去 不然就空了
# def log_response(response):
#     # print('after request')
#     app.logger.warning(f'response data logged in after request func:{response.status}')
#     return response
# # @app.before_request

if __name__ == '__main__':
    start_http_server(9090)
    try:
            app.logger.info('starting app using logger ')
            app.run('0.0.0.0')
    except Exception as e:
            import traceback
            app.logger.error(f'flask main app start failed:{e}')

    finally:
            app.logger.info('app stopped')

    # run.send_mail()
