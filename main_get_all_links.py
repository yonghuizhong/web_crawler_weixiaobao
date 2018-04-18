from one_category_links import get_one_category
import pymongo

client = pymongo.MongoClient('localhost', 27017)
weixiaobao = client['weixiaobao']
category_pages_links = weixiaobao['category_pages_links']  # 存储所有目录的所有页面链接


with open('cookie.txt', 'rt') as f:
    for line in f:
        cookie = line.strip()
# print(cookie)
print('获取所有目录中的文章链接...')
for i in category_pages_links.find():
    print(i['url'])
    get_one_category(i['url'], cookie)
