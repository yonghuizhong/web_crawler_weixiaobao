import os
import random
import time
import sys

from one_category_links import all_links
from one_category_links import link_details

count = 0  # main_get_link_details.py执行次数


def watch():
    global count    # 定义全局变量
    while True:
        count = count + 1
        data_array = [i['href'] for i in all_links.find()]  # 数据库的原始数据
        got_array = [i['url'] for i in link_details.find()]  # 已经爬到的数据
        x = set(data_array)
        y = set(got_array)
        rest_array = x.difference(y)  # 需要爬的数据
        print(len(x), len(y), len(rest_array))
        if len(rest_array) > 0 and count < 6:
            if count == 1:
                print('第', count, '次运行程序')
                os.system('python main_get_link_details.py')
            else:
                print('第', count, '次运行程序')
                print('暂停30秒...')
                time.sleep(30+random.uniform(1, 3))
                os.system('python main_get_link_details.py')
        else:
            print('爬虫重启次数达到限值，已停止；或已经爬取完毕~')
            sys.exit()


watch()
