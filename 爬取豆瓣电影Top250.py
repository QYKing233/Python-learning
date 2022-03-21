# 卿与
# python学习之路
# 开发时间：2022/3/21 18:49
import json
import re
import time

import requests


# 获取第一页数据函数
def get_one_page(url):
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.74 Safari/537.36 '
    }
    # 发送GET请求
    response = requests.get(url, headers=headers)
    # 如果成功就存储数据到response，否则返回None
    if response.status_code == 200:
        return response.text
    return None


# 分析第一页数据，然后正则提取排名、海报地址、主演、评分函数
def parse_one_page(html):
    # 正则表达式
    pattern = re.compile(
        '<li>.*?class="".*?>(.*?)</em>.*?src="(.*?)".*?"title">(.*?)<.*?<p class="">(.*?)</p>.*?average">(.*?)<', re.S)
    # 用正则表达式提取数据
    items = re.findall(pattern, html)
    # 截止到敲完代码2022-03-21-22:49,下边的没看懂
    for item in items:
        yield {
            '排名': item[0],
            '海报': item[1],
            '名字': item[2],
            '导演': item[3].strip(),
            '评分': item[4],
        }


# 把提取后的数据写入到豆瓣TOP250.TXT
def write_to_file(content):
    with open('豆瓣TOP250.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


# 主函数
def main(start):
    # 拼装URL
    url = 'https://movie.douban.com/top250?start=' + str(start)
    # 获取第一页数据并存储到html变量
    html = get_one_page(url)
    # 分析第一页数据
    parse_one_page(html)
    # 遍历第一页正则提取后的数据
    for item in parse_one_page(html):
        # 在屏幕上打印出来
        print(item)
        # 写入到文件
        write_to_file(item)


# 分页爬取，一共10页。每页25个
for i in range(10):
    main(start=i * 25)
    # 爬完一页等待10S，防止黑IP
    time.sleep(10)
