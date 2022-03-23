# 卿与
# Python学习之路
# 开发时间：2022/3/22 12:31
import requests
import json
import re


def regex_home_page_url(response):
    pattern_home_page = re.compile(r"2022必看热片.*?<ul>(?P<ul>.*?)</ul>", re.S)
    result_home_page = pattern_home_page.finditer(response.text)
    result = []
    for home_url in result_home_page:
        result.append(home_url.group('ul'))
    return result


def regex_child_page_url(response):
    response1 = ''
    for resp in response:
        response1 += resp
    pattern_child_page = re.compile("<li><a href='(?P<url>.*?)'", re.S)
    result_child_page = pattern_child_page.finditer(response1)
    result = []
    for child_url in result_child_page:
        result.append(child_url.group('url').lstrip('/'))
    return result


def regex_download_url(response):
    pattern_name = re.compile(r"片　　名(?P<name>.*?)<br />", re.S)
    result_name = pattern_name.finditer(response.text)
    pattern_link = re.compile(r"<!--xunleiDownList Start-->.*?<tbody>.*?<tr>.*?<td.*?<a href=\"(?P<link>.*?)"
                              r"</a></td>", re.S)
    result_link = pattern_link.finditer(response.text)
    result = {}
    result_movie_name = []
    result_movie_link = []
    for movie_name in result_name:
        result_movie_name.append(movie_name.group('name').lstrip())
    for movie_link in result_link:
        result_movie_link.append(movie_link.group('link'))
    for name, link in zip(result_movie_name, result_movie_link):
        result[name] = link
    return result

def write_file(response):

    for key, value in response.items():

        with open('盗版天堂2022必看.txt', 'a+', encoding='utf-8') as f:
            f.write(json.dumps(str(key)+'\n', ensure_ascii=False))
            f.write(json.dumps(str(value)+'\n', ensure_ascii=False))
            f.write('\n\n\n')


url = 'https://dytt89.com/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
                  '/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
}
response = requests.get(url, headers=headers)
response.encoding = 'gb2312'
response.close()

for child_url in regex_child_page_url(regex_home_page_url(response)):
    url1 = url + child_url
    response1 = requests.get(url1, headers=headers)
    response1.encoding = 'gb2312'
    print(regex_download_url(response1))
    write_file(regex_download_url(response1))
    response1.close()
