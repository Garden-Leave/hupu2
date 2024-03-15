FROM ccr.ccs.tencentyun.com/allen-images/flask-demo:base
WORKDIR /hupu
#ENTRYPOINT ping
COPY ./ /hupu/

RUN pip3.8 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ENTRYPOINT python3.8 main.py




