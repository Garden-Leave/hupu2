FROM yankovg/python3.8.2-ubuntu18.04:latest
WORKDIR /hupu
#ENTRYPOINT ping
COPY ./ /hupu

RUN pip3.8 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ENTRYPOINT python3.8 main.py