import os
import requests
from bs4 import  BeautifulSoup
from config.config import Config
from datetime import datetime
from flask import current_app
from helpers.log_helper import logger1


def fetch_parse(num):
    list1 =[]
    i = 0
    line_num = 1
    t_body=''
    #timestamp = str(datetime.now())[11:13] + '-' + str(datetime.now())[14:16]
    try:
        r = requests.get(url=Config.target_url)
        file = r.text
        f = open('./helpers/temp.html', 'w', encoding='utf-8')   # 清空原来文件内容并写入 html返回内容
        f.write(file)
        f.close()
        with open('./helpers/temp.html','r',encoding='utf-8') as t:
           soup = BeautifulSoup(t, features='lxml')  # 传入文件 中间文件
           s1 = soup.find_all("a", class_="content-wrap-span")  # 返回字典类型
           for x in s1:
            link = x.get('href')
            text = x.text
            list1.append(text)
            list1.append(link)
        if len(list1) > 0:
            logger1.info('page fetched and parsed!')
        while i <= len(list1) - 4 and line_num <= num:   # 控制结果行数 只抓一页，最多20行
            title = list1[i]
            module = list1[i + 2]
            i += 4
            t_body = t_body + f'<tr><td>{line_num}</td><td>{title}</td><td>{module}</td></tr>'
            # print(line_num)
            line_num += 1
        output = f'''<!DOCTYPE html><head> <meta charset="UTF-8"><title>虎扑热帖</title></head><body><table border="1"class="left"><thead><tr><th>
        序号</th><th>帖子标题</th><th>板块</th></tr></thead><tbody>{t_body}</tbody></table></body>'''
        output=output + '<body> 20 links most</body>' if num > 20 else output
        # print(output)
        with open('./templates/result.html', 'w', encoding='utf-8') as f:
            f.write(output)
            f.flush()
            logger1.info('result file populated!')
    except Exception as e:
        import traceback
        print(e)
        logger1.info(e)


if __name__ == '__main__':
    fetch_parse()