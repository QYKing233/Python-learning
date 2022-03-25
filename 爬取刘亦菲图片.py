# 卿与
# python学习之路
# 开发时间：2022/3/25 20:13
import requests
from bs4 import BeautifulSoup
import re

# 首页地址
url = 'http://www.n63.com/photodir/?album=/china/liuyifei&page=1&'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/99.0.4844.82 Safari/537.36'
}
# 拿到首页源码
response = requests.get(url, headers=headers)
# 转码为gbk2312
response.encoding = 'gb2312'
# 使用BeautifuiSoup+lxml格式化主页源码
page = BeautifulSoup(response.text, 'lxml')
# 寻找属性值为wjole的div标签下的所有a节点
links = page.find('div', attrs={'id': 'whole'}).findAll('a')
lin = []
clean_lin = []
endurl = []
# 定义解析高清图片链接的正则表达式
regex = re.compile('<img border="0" height="900" src="(.*?)"', re.S)
# 循环把a节点下标签为href的值存储到列表lin
for link in links:
    lin.append(str(link.get('href')))
# 从杂乱地址中拿到子页面地址
clean_lin = lin[2:14]
# 遍历列表并且组装子页面地址
for url2 in clean_lin:
    # 拿到子页面地址源码
    response1 = requests.get(url2, headers=headers)
    response1.encoding = 'gb2312'
    page1 = BeautifulSoup(response1.text, 'lxml')
    # 拿到属性值为image_content的div节点下的所有a节点
    link1 = page1.find('div', attrs={'id': 'image_content'}).findAll('a')
    # 遍历a节点拿到高清大图地址
    for link2 in link1:
        # 正则提取到高清大图地址
        result = regex.finditer(str(link2))
        for result1 in result:
            # 把地址存储到列表
            endurl.append(result1.group(1))
num = 0
for eendurl in endurl:
    # 遍历地址列表并组装成完整地址
    url3 = 'http://www.n63.com/photodir/' + eendurl
    # 拿到图片源码
    response2 = requests.get(url3)
    # 以二进制形式写入到文件
    with open('{0}.jpg'.format(num), 'wb+') as f:
        f.write(response2.content)
    num += 1

# 关闭所有请求
response.close()
response1.close()
response2.close()
