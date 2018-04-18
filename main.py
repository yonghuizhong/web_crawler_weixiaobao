import os
import pymongo

client = pymongo.MongoClient('localhost', 27017)
weixiaobao = client['weixiaobao']
category_pages_links = weixiaobao['category_pages_links']  # 存储所有目录的所有页面链接
all_links = weixiaobao['all_links']  # 存储所有目录中所有页面的文章链接
link_details = weixiaobao['link_details']  # 存储所有链接的正文

print('请确定cookie.txt与ip.txt已更新，1：是；0：否')
check = input('是否已更新：')
if check == '1':
    category_pages_links.remove()
    all_links.remove()
    link_details.remove()
    print('已清空数据库，开始运行程序')

    os.system('python main_get_all_category.py')  # 获取所有目录的所有页面链接
    os.system('python main_get_all_links.py')  # 获取上面链接中的所有文章链接
    print('获取文章链接成功！程序将获取所有文章的正文...')

    os.system('python details_watch.py')  # 自动监控获取所有文章的正文
    print('文章正文获取完毕！正在导出...')

    os.system('python to_excel.py')  # 导出Excel表格
    print('已导出。')
else:
    print('关闭程序')
