import random
import requests
from bs4 import BeautifulSoup
import time
import pymongo
from fake_useragent import UserAgent

client = pymongo.MongoClient('localhost', 27017)
weixiaobao = client['weixiaobao']
category_pages_links = weixiaobao['category_pages_links']  # 存储所有目录的所有页面链接
all_links = weixiaobao['all_links']  # 存储所有目录中所有页面的文章链接
link_details = weixiaobao['link_details']  # 存储所有链接的正文

ua = UserAgent(path='User-Agent.json')

# http://cn-proxy.com/ 每天更新 需翻墙 暂时用Excel对付着
proxy_list = []
with open('ip.txt', 'rt') as f:
    for line in f:
        proxy_list.append(line.strip())
# print(proxy_list)


# spider 1
# url = 'https://data.wxb.com/rankArticle?cate=-1&page=1'
def get_one_category(url, my_cookie):
    time.sleep(random.uniform(2, 3))
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cookie': my_cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Connection': 'keep-alive'
    }
    res = requests.get(url, headers=headers)
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
# cookie = 'visit-wxb-id=b63f5d2a0c2b9eab1fd76a823988f029; wxb_fp_id=3514672447; Hm_lvt_5859c7e2fd49a1739a0b0f5a28532d91=1520903399,1520935053,1520993092,1521007170; PHPSESSID=hfc2jjk6t817i07i2adlu9fs95; Hm_lpvt_5859c7e2fd49a1739a0b0f5a28532d91=1521007966'
# get_one_category(url, cookie)


# spider 2
# url = 'https://mp.weixin.qq.com/s?__biz=MzA4NDI3NjcyNA==&mid=2649387099&idx=1&sn=251aaee7b544d5931caa55c66cc034be&chksm=87f774c0b080fdd67d9fe9fe21caf5a67b34218f401c41fe54e8be136a880862f35044929548&scene=27#wechat_redirect'
def get_details(url):
    time.sleep(random.uniform(1, 2))
    proxies = {
        'http': random.choice(proxy_list)
    }
    headers2 = {
        'User-Agent': ua.random,
        'Connection': 'keep-alive'
    }
    try:
        res = requests.get(url, headers=headers2, proxies=proxies, timeout=5)
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
    except Exception as e:
        print('error!')
        print(e)
        print(url)


# url = 'https://mp.weixin.qq.com/s?__biz=MjM5MjAxNDM4MA==&mid=2666189702&idx=3&sn=404739b2b044befd4d331395ef09490d&chksm=bdb2bac58ac533d3d7e9d7c4aaba3748b58f934000ccca3faefd15c1a9af5ad1f695cbc2d9a2&scene=27#wechat_redirect'
# url = 'https://mp.weixin.qq.com/s?__biz=MjM5NzM4MDg1MA==&mid=2652156449&idx=1&sn=931835ea171e3208fe1306e38b0cec3d&chksm=bd3ac5bc8a4d4caa279133a7a46c2f0112455ad50b98eb0a0d9ff299db82bfc1bf0cc500b458&scene=27#wechat_redirect'
# get_details(url)


# spider 3
# 得到每一个目录的页数
def get_page_nums(url, my_cookie):
    time.sleep(random.uniform(1, 3))
    headers = {
        'Cookie': my_cookie,
        'User-Agent': ua.random,
        'Connection': 'keep-alive'
    }
    res = requests.get(url, headers=headers)
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
        print('1')  # 只有一页的情况
        a = 1
        return a
    else:
        print(nums)
        return nums
