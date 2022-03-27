# 卿与
# python学习之路
# 开发时间：2022/3/27 19:46
import requests
from lxml import html
import time

tree = html.etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/99.0.4844.82 Safari/537.36'
}
input('请按任意键开始！')
for i in range(2, 25):
    # 2-25页地址组装
    url = 'http://www.n63.com/photodir/?album=/china/liuyifei&page=' + str(i) + '&'
    # 请求主页（非首页）
    resp = requests.get(url, headers=headers)
    child_page = tree.HTML(resp.text)
    # 截取刘亦菲的大图页面地址
    page = child_page.xpath('//*[@id="container"]/div/div/a/@href')[0:-1]
    for alone_page in page:
        # 请求大图页面地址
        resp1 = requests.get(alone_page, headers=headers)
        image_page = tree.HTML(resp1.text)
        # xpath解析到图片的href链接
        image_href = image_page.xpath('//*[@id="image_show"]/a[1]/img/@src')[0]
        # 组装成正常图片地址
        image_link = 'http://www.n63.com/photodir/' + image_href
        print('**************************************************')
        print('爬取地址OVER!' + image_link)
        # 请求图片地址，并把二进制数据塞给resp2
        resp2 = requests.get(image_link).content
        # 提取图片的名字
        image_name = image_href.split('?', -1)[1]
        # 把图片二进制数据写入到图片文件
        with open(image_name, mode='wb+') as f:
            f.write(resp2)
        print('文件写入OVER!' + image_name)
        print('等待1s.....防止黑IP')
        print('**************************************************\n\n\n')
        time.sleep(1)
        resp1.close()
print('ALL OVER!')
input("请按任意键退出！")
resp.close()
