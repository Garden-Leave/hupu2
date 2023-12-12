
import  requests
from datetime import  datetime
import requests
from requests import utils
from bs4 import BeautifulSoup
timestamp = str(datetime.now())[11:13] +'-'+str(datetime.now())[14:16]

def get_baidu_search_result(keyword):
    url = 'https://www.baidu.com/s'
    # params = {'wd': keyword}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    params = {
        'ie': 'UTF-8',
        'wd': 'Python'
    }
    res1 = requests.get('https://www.baidu.com/', headers=headers)
    cookie_dict= requests.utils.dict_from_cookiejar(res1.cookies)
    res2 = requests.get(url, headers=headers,params=params,cookies=cookie_dict)
    print(res2.encoding)
    res2.encoding='apparent_encoding'    # 默认取回的内容response里是 ISO-8859-1 编码 导致中文乱码，需要手动修改 apparent_coding自动分析，或者指定utf-8
    print(res2.text)
    with open(f'baidu{timestamp}.html','w+',encoding='utf-8') as f:
        f.write(res2.text)
        f.flush()

    soup = BeautifulSoup(res2.text, 'html.parser')
    results = soup.find_all('div', class_='result')
    for result in results:
        try:
            title = result.h3.a.text
            link = result.h3.a['href']
            desc = result.find('div', class_='c-abstract').text
        except Exception as e:
            pass


if __name__ == '__main__':
    keyword = 'Python'
    get_baidu_search_result(keyword)