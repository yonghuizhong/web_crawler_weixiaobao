from one_category_links import get_one_category
from one_category_links import get_page_nums
from multiprocessing import Pool
from one_category_links import all_links

# 首先得到所有目录的页数
# page_nums_array = []  # 存储所有目录的页数
# url = 'https://data.wxb.com/rankArticle?cate=-1&page=1'  # 总榜链接
# page_nums = get_page_nums(url)
# page_nums_array.append(int(page_nums))
# for i in range(1, 22):
#     url = 'https://data.wxb.com/rankArticle?cate={}&page=1'.format(str(i))
#     page_nums_array.append(int(get_page_nums(url)))
# print(page_nums_array)
page_nums_array = [10, 10, 1, 2, 1, 2, 5, 10, 10, 6, 1, 10, 1, 10, 3, 3, 10, 10, 3, 3, 10, 5]
print(len(page_nums_array))


# 得到所有目录的所有页的链接
all_page_urls = []
# 总榜目录
for i in range(1, page_nums_array[0]+1):
    url = 'https://data.wxb.com/rankArticle?cate=-1&page={}'.format(str(i))
    all_page_urls.append(url)


# 其他目录：1-21目录的所有页的链接
# url = 'https://data.wxb.com/rankArticle?cate=1&page=1'
for i in range(1, 22):
    for num in range(1, page_nums_array[i]+1):
        url = 'https://data.wxb.com/rankArticle?cate={}&page={}'.format(str(i), str(num))
        all_page_urls.append(url)


# 程序中断时从断点处开始爬取
# index_links = [link['page_link'] for link in all_links.find()]
# x = set(all_page_urls)
# y = set(index_links)
# rest_links = x.difference(y)
rest_links = all_page_urls  # 放在集合后页码会乱掉，所以还是这样吧


# if __name__ == '__main__':
#     pool = Pool()
#     pool.map(get_one_category, rest_links)

# 还是一个个来吧，被拉黑账号了
for i in rest_links:
    get_one_category(i)
