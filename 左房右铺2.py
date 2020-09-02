import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
def get_url(url):
    '''
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',

    }
    proxy = {
        'http': '171.35.175.103:9999',
        'https': '171.35.175.103:9999',
    }
    '''
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text


def parse_page(demo):
    a = []
    soup = BeautifulSoup(demo, 'lxml')
    resmanager = soup.find('div', class_='_res_message')
    resmsgs = resmanager.find_all('div', class_='_res_msg')
    for resmsg in resmsgs:
        dic = {}
        msg3 = resmsg.find('div', class_='msg3')
        ul = msg3.find('ul')
        msg3li2 = ul.find('li', class_='msg3_li2')
        span = msg3li2.find('span')
        price = span.text
        # print(price) #住房单价
        msg12 = resmsg.find('div', class_='_msg12')
        msg2 = msg12.find('div', class_='_msg2')
        ul2 = msg2.find('ul')
        li2 = ul2.find_all('li')[1]
        p = li2.find('p')
        position = p.text
        # print(position) 住房位置
        msg4li4 = ul.find('li', class_='msg4_li4')
        p = msg4li4.find('p')
        name = p.text
        # print(name) 联系人

        dic['价格'] = price
        dic['位置'] = position
        dic['联系人'] = name
        a.append(dic)




    # print(a)
    return a
    #return price,position,name
def print_pandas(data):
    columns = ['价格', '位置', '联系人']
    df = pd.DataFrame(data, columns=columns)
    return df
def urls():
    ulist = []
    for i in range(44):
        if i == 0:
            url = 'https://www.zuofyp.com/loupan.html'
            ulist.append(url)
        else:
            url = 'https://www.zuofyp.com/loupan.html?page={}'.format(i+1)
            ulist.append(url)
    return ulist


if __name__ == '__main__':
    '''
    url = 'https://www.zuofyp.com/loupan.html'
    url2 = 'https://www.zuofyp.com/loupan.html?page=2'
    # 440个楼盘
    for i in range(10):
        
        if i==0:
            url='https://www.zuofyp.com/loupan.html'
            demo=get_url(url)
            text=parse_page(demo)

        else:
            url='https://www.zuofyp.com/loupan.html?page=(i+1)'
            demo2=get_url(url)
            text2=parse_page(demo2)
        
        url = 'https://www.zuofyp.com/loupan.html?page=(i+1)'
        demo = get_url(url)
        text2 = parse_page(demo)
        print_pandas(text2)
    url3 = 'https://www.zuofyp.com/loupan/type/6.html'
    url4 = 'https://www.zuofyp.com/loupan/type/6.html?page=2'
    url5 = 'https://www.zuofyp.com/loupan/type/6.html?page=3'
    # 231个楼盘
    '''
    ulists=urls()
    price = []
    location = []
    person = []
    columns = ['价格', '位置', '联系人']
    data = pd.DataFrame(columns=columns)
    for ulist in ulists:
        demo=get_url(ulist)
        text=parse_page(demo)
        data = data.append(print_pandas(text))

    data = data.reset_index(drop=True) #数据清洗时，会将带空值的行删除，此时DataFrame或Series类型的数据不再是连续的索引，可以使用reset_index()重置索引。
    print(data)
