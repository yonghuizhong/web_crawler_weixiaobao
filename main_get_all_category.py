from one_category_links import get_page_nums
import pymongo

client = pymongo.MongoClient('localhost', 27017)
weixiaobao = client['weixiaobao']
category_pages_links = weixiaobao['category_pages_links']  # 存储所有目录的所有页面链接

with open('cookie.txt', 'rt') as f:
    for line in f:
        cookie = line.strip()
# print(cookie)

print('获取所有目录的页数...')
# 首先得到所有目录的页数
page_nums_array = []  # 存储所有目录的页数
url = 'https://data.wxb.com/rankArticle?cate=-1&page=1'  # 总榜链接
page_nums = get_page_nums(url, cookie)
page_nums_array.append(int(page_nums))
for i in range(1, 22):
    url = 'https://data.wxb.com/rankArticle?cate={}&page=1'.format(str(i))
    page_nums_array.append(int(get_page_nums(url, cookie)))
print(page_nums_array)

# 得到所有目录的所有页的链接
# 总榜目录
for i in range(1, page_nums_array[0] + 1):
    url = 'https://data.wxb.com/rankArticle?cate=-1&page={}'.format(str(i))
    category_pages_links.insert_one({'url': url})

# 其他目录：1-21目录的所有页的链接
# url = 'https://data.wxb.com/rankArticle?cate=1&page=1'
for i in range(1, 22):
    for num in range(1, page_nums_array[i] + 1):
        url = 'https://data.wxb.com/rankArticle?cate={}&page={}'.format(str(i), str(num))
        category_pages_links.insert_one({'url': url})

