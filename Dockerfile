
FROM welersonb/python3.8-alpine
WORKDIR /hupu
#ENTRYPOINT ping
COPY ./ /hupu
COPY __init__.py  /usr/local/lib/python3.7/site-packages/urllib3/__init__.py

RUN pip install --upgrade pip==20.3
RUN pip install flask flask_cors  pymysql dbutils requests beautifulsoup4 lxml

#COPY __init__.py  /usr/local/lib/python3.7/site-packages/urllib3/__init__.py
ENTRYPOINT python3 main.py