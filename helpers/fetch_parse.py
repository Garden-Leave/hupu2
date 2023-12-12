import os
import requests
from bs4 import  BeautifulSoup
from config.config import Config
from datetime import datetime
from flask import  current_app


def fetch_parse():
    list1 =[]
    timestamp = str(datetime.now())[11:13] + '-' + str(datetime.now())[14:16]
    try:
        r = requests.get(url=Config.target_url)
        file = r.text
        # f =open('./{}.html'.format(date),'w',encoding='utf-8')
        f = open(f'{timestamp}.html', 'w', encoding='utf-8')
        f.write(file)
        f.close()
        current_app.logger.info('file fetched successfully!')
    except Exception as e:
        print(e)
    fh = open(f'{timestamp}.html', 'r', encoding='utf-8')  # 打开文件，指定模式和编码
    soup = BeautifulSoup(fh, 'lxml')  # 传入文件

    s1 = soup.find_all("a", class_="content-wrap-span")
    for x in s1:
        link = x.get('href')
        text = x.text
        list1.append(text)
        list1.append(link)
    if len(list1) > 0:
        current_app.logger.info('info parsed successfully!')
    fh.close()
    os.remove(f'{timestamp}.html')
    current_app.logger.info('result from parse')
    return list1
    # print(self.list1)
    # i = 0
    # j = 1
    # while i <= len(self.list1)-4:
    #     title = self.list1[i]
    #     module = self.list1[i+2]
    #     i += 4
    #     self.t_body = self.t_body + f'<tr><td>{j}</td><td>{title}</td><td>{module}</td></tr>'
    #     j += 1
    # self.output = f'''<!DOCTYPE html><head> <meta charset="UTF-8"><title>虎扑热帖</title></head><body><table border="1"class="left"><thead><tr><th>
    # 序号</th><th>帖子标题</th><th>板块</th></tr></thead><tbody>{self.t_body}</tbody></table></body>'''

    # with open('result.html', 'w', encoding='utf-8') as f:
    #     f.write(self.output)
    #     f.flush()
    #     f.close()

