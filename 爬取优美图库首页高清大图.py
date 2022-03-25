# 卿与
# python学习之路
# 开发时间：2022/3/24 22:20
import requests
from bs4 import BeautifulSoup
import re

# 定义优美图库主页链接
url = 'https://www.umeitu.com/p/gaoqing/'
# 定义浏览器标识
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/99.0.4844.82 Safari/537.36'
}
# 拿到主页源码
response = requests.get(url, headers=headers)
# 转码为UTF-8
response.encoding = 'utf-8'
# 使用bs4+lxml格式化主页源码
page = BeautifulSoup(response.text, 'lxml')
# 获取属性值为Typelist的div下的所有a节点
links = page.find('div', attrs={'class': 'TypeList'}).findAll('a')
num = 0
for link in links:
    # 获取到a节点下的链接并组装
    url2 = url + str(link.get('href')).strip('/p/gaoqing')
    # 拿到大图页面网页源码
    response1 = requests.get(url2, headers=headers)
    # 转码为UTF-8
    response1.encoding = 'utf-8'
    # 使用bs4+lxml格式化大图页面源码
    page1 = BeautifulSoup(response1.text, 'lxml')
    # 获取属性值为ImageBody的div节点下的p节点下的所有a节点
    link = page1.find('div', attrs={'class': 'ImageBody'}).find('p').findAll('a')
    for lin in link:
        # 获取img标签下的src链接，并请求此链接，将数据写入response2
        response2 = requests.get(lin.img['src'], 'lxml')
        num += 1
        # 把图片二进制数据流写入到图片
        with open('{0}.jpg'.format(num), 'wb+') as f:
            f.write(response2.content)

# 关闭所有打开的请求
response.close()
response1.close()
response2.close()
