
FROM welersonb/python3.8-alpine
WORKDIR /hupu
#ENTRYPOINT ping
COPY ./ /hupu
#COPY __init__.py  /usr/local/lib/python3.7/site-packages/urllib3/__init__.py

#RUN pip install --upgrade pip==20.3
pip install -r requirements.txt

#COPY __init__.py  /usr/local/lib/python3.7/site-packages/urllib3/__init__.py
ENTRYPOINT python3 main.py