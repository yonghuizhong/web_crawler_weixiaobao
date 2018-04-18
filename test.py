import time
from fake_useragent import UserAgent
import random

ua = UserAgent(path='User-Agent.json')

# http://cn-proxy.com/ 每天更新 需翻墙 暂时用Excel对付着
proxy_list = [
    'http://120.92.88.202:10000',
    'http://39.134.10.99:8080',
    'http://39.134.10.16:8080',
    'http://39.134.10.10:8080',
    'http://39.134.10.5:8080',
    'http://39.134.10.101:8080',
    'http://221.130.253.135:8090',
    'http://47.95.36.86:8081',
    'http://39.134.10.22:8080',
    'http://39.134.10.3:8080',
    'http://39.134.10.11:8080',
    'http://39.134.10.13:8080',
    'http://39.134.10.12:8080',
    'http://39.134.10.17:8080',
    'http://58.240.53.196:80',
    'http://58.240.53.194:8080',
    'http://120.92.119.187:10010',
    'http://119.28.50.37:82',
    'http://114.215.174.227:8080',
    'http://58.240.53.196:8080'
]


def text(my_cookie):
    proxies = {
        'http': random.choice(proxy_list)
    }
    headers2 = {
        'Cookie': my_cookie,
        'User-Agent': ua.random,
        'Connection': 'keep-alive'
    }
    print(headers2, proxies)


# for i in range(1, 5):
#     cookie = 'fsdfslfjsdlf'
#     text(cookie)

# proxy_list = []
# with open('ip.txt', 'rt') as f:
#     for line in f:
#         proxy_list.append(line.strip())
# print(proxy_list)

print(time.strftime("%m%d", time.localtime()))
print('请确定cookie.txt与ip.txt已更新，1：是；0：否')
check = input('是否已更新：')
if check == '1':
    print(check)
elif check == '0':
    print(check)
else:
    print('error')
