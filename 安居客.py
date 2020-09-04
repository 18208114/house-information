import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
def getheaders(page,cookie):
    headers={
        'authority': 'nc.anjuke.com',
        'method': 'GET',
        'path': '/community/p{}/'.format(page),
        'scheme': 'https',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip,deflate,br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie,
        'referer': 'https://nc.anjuke.com/community/p1/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-size': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'x - requested - with': 'XMLHttpRequest'

    }
    return headers
def get_html_by_page(page,cookie):
    headers=getheaders(page,cookie)
    url='https://nc.anjuke.com/community/p{}/#'.format(page)
    r=requests.get(url,headers=headers)
    r.encoding=r.apparent_encoding
    if r.status_code!=200:
        print("页面不存在")
        return None
    else:
        return r.text
def extract_data_from_html(html):
    soup=BeautifulSoup(html,'html.parser')
    list_content = soup.find(id="list-content")
    if  not list_content:
        print("无内容")
        return None
    else:
        items=list_content.find_all('div',class_='li-itemmod')
    if len(items)==0:
        print("无内容")
        return None
    else:
        return [extract_data(item) for item in items]
def extract_data(item):
    name=item.find_all('a')[1].text.strip()

    address=item.address.text.strip()
    if item.strong is not None:
        price1=item.strong.text.strip()
    else:
        price1=None
    print(name,address,price1)
    return name,address,price1
def crawl_all_page(cookie):
    page=1
    data_raw = []
    while True:
        try:
            html = get_html_by_page(page, cookie)
            data_page = extract_data_from_html(html)
            if not data_page:
                break
            data_raw += data_page
            print('crawling {}th page ...'.format(page))
            if(page<=50):
                page += 1
            else:
                break
        except:
            print('maybe cookie expired!')
            break
    print('crawl {} pages in total.'.format(page - 1))
    return data_raw
def create_df(data):
    columns = ['name', 'address', 'price1']
    return pd.DataFrame(data, columns=columns)
def clean_data(df):
    df.dropna(subset=['price1'], inplace=True)
    df = df.astype({'price1': 'float64'})
    return df
def run(cookie):
    data = crawl_all_page(cookie)
    df = create_df(data)
    df = clean_data(df)
    df.sort_values('price1', inplace=True)
    df.reset_index(drop=True, inplace=True)
def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cookie', type=str, help='cookie.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_cli_args()
    print(args.cookie)
    run(args.cookie)
