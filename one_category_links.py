import random
import requests
from bs4 import BeautifulSoup
import time
import pymongo


client = pymongo.MongoClient('localhost', 27017)
weixiaobao = client['weixiaobao']
all_links = weixiaobao['all_links']  # 存储所有目录的链接
link_details = weixiaobao['link_details']  # 存储所有链接的正文


# http://cn-proxy.com/ 每天更新
proxy_list = [
    'http://58.240.53.196:80',
    'http://61.160.190.146:8090',
    'http://114.112.104.223:80',
    'http://61.160.190.147:8090',
    'http://120.77.201.46:8080',
    'http://58.240.53.194:8080'

]
proxy_ip = random.choice(proxy_list)
proxies = {
    'http': proxy_ip
}

headers = {
    'Cookie': 'visit-wxb-id=b63f5d2a0c2b9eab1fd76a823988f029; wxb_fp_id=3514672447; Hm_lvt_5859c7e2fd49a1739a0b0f5a28532d91=1520903399,1520935053,1520993092,1521007170; PHPSESSID=hfc2jjk6t817i07i2adlu9fs95; Hm_lpvt_5859c7e2fd49a1739a0b0f5a28532d91=1521007966',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Connection': 'keep-alive'
}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'Connection': 'keep-alive'
}


# spider 1
# url = 'https://data.wxb.com/rankArticle?cate=-1&page=1'
def get_one_category(url):
    time.sleep(2)
    res = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    category = soup.select('div.title')[1].text
    titles = soup.select('div.article-title > a.title-text')
    accounts = soup.select('tr.ant-table-row.ant-table-row-level-0 > td:nth-of-type(2) > a')
    spread_nums = soup.select('span.spread-text')
    page_views = soup.select('tr.ant-table-row.ant-table-row-level-0 > td:nth-of-type(4)')
    like_nums = soup.select('tr.ant-table-row.ant-table-row-level-0 > td:nth-of-type(5)')
    for i, a, s, p, l in zip(titles, accounts, spread_nums, page_views, like_nums):
        print(category)
        print(i.text)
        print(i.get('href'))
        print(a.text)
        print(s.text)
        print(p.text)
        print(l.text)
        print('\n')
        data = {
            'page_link': url,
            'category': category,
            'title': i.text,
            'href': i.get('href'),
            'account': a.text,
            'spread_nums': s.text,
            'page_views': p.text,
            'like_nums': l.text
        }
        all_links.insert_one(data)


#  总榜链接（均为第一页）
# url = 'https://data.wxb.com/rankArticle?cate=-1&page=3'
# get_one_category(url)


# spider 2
# url = 'https://mp.weixin.qq.com/s?__biz=MzA4NDI3NjcyNA==&mid=2649387099&idx=1&sn=251aaee7b544d5931caa55c66cc034be&chksm=87f774c0b080fdd67d9fe9fe21caf5a67b34218f401c41fe54e8be136a880862f35044929548&scene=27#wechat_redirect'
def get_details(url):
    time.sleep(2)
    try:
        res = requests.get(url, headers=headers2, proxies=proxies)
        soup = BeautifulSoup(res.text, 'html.parser')
        post_date = soup.select('em#post-date')[0].text
        contents = soup.select('div.rich_media_content p')
        original = soup.find(id='copyright_logo')
        print('\n')
        print(url)
        print(post_date)
        if original:
            original_tag = 1
        else:
            original_tag = 0
        print(str(original_tag))
        contents_array = [i.text.split()[0] for i in contents if len(i.text.split()) > 0]
        contents_str = '\n'.join(contents_array)
        data = {
            'url': url,
            'post_date': post_date,
            'original': original_tag,
            'contents': contents_str
        }
        link_details.insert_one(data)
    except:
        print('error!')
        print(proxies)
        print(url)


# url = 'https://mp.weixin.qq.com/s?__biz=MjM5MjAxNDM4MA==&mid=2666189702&idx=3&sn=404739b2b044befd4d331395ef09490d&chksm=bdb2bac58ac533d3d7e9d7c4aaba3748b58f934000ccca3faefd15c1a9af5ad1f695cbc2d9a2&scene=27#wechat_redirect'
# url = 'https://mp.weixin.qq.com/s?__biz=MjM5NzM4MDg1MA==&mid=2652156449&idx=1&sn=931835ea171e3208fe1306e38b0cec3d&chksm=bd3ac5bc8a4d4caa279133a7a46c2f0112455ad50b98eb0a0d9ff299db82bfc1bf0cc500b458&scene=27#wechat_redirect'
# get_details(url)


# spider 3
# 得到每一个目录的页数
def get_page_nums(url):
    time.sleep(2)
    res = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(res.text, 'html.parser')
    nums = len(soup.find_all('li', 'ant-pagination-item'))
    if nums == 6:
        page_nums = soup.select('ul.ant-pagination.ant-table-pagination > li:nth-of-type(8)')[0].text
        if page_nums == '':
            page_nums = 6
        print(page_nums)
        print('true')
        return page_nums
    elif nums == 0:
        print('1')    # 只有一页的情况
        a = 1
        return a
    else:
        print(nums)
        return nums






