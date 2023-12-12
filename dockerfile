
FROM temp1:latest
WORKDIR /hupu
ENV id  999
ENV db_ip  888
#ENTRYPOINT ping
COPY ./hupu2  /hupu
COPY __init__.py  /usr/local/lib/python3.7/site-packages/urllib3/__init__.py

RUN pip install --upgrade pip==20.3
RUN pip install flask flask_cors  pymysql dbutils requests beautifulsoup4 lxml

COPY __init__.py  /usr/local/lib/python3.7/site-packages/urllib3/__init__.py
ENTRYPOINT python3 main.py