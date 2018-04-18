from one_category_links import get_details
from one_category_links import all_links
from one_category_links import link_details
from multiprocessing import Pool

# 程序中断时从断点处开始爬取
db_links = [link['href'] for link in all_links.find()]
index_links = [link['url'] for link in link_details.find()]
x = set(db_links)
y = set(index_links)
rest_links = x.difference(y)
print(len(x), len(y), len(rest_links))

if __name__ == '__main__':
    pool = Pool()
    pool.map(get_details, rest_links)

