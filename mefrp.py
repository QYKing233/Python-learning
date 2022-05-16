#  Python学习之路
# 开发时间：2022/5/16 14:03
# 用PYTHON来时实现内网穿透网站领流量

import requests
import re


# 登录
def login(login_url, data):
    with session.post(url=login_url, data=data) as resp:
        print(resp.cookies)


# 签到领流量
# 开始分析签到的请求，由于我今天签到过了。签到按钮不能点击了，我们稍微改一下HTML
def sign_in(csrf_url):
    # 这是签到的连接
    sign_in_url = f'https://mefrp.cn/?page=panel&module=sign&sign&csrf={get_csrf(csrf_url)}'
    with session.get(url=sign_in_url) as resp:
        print(resp.text)


# 获取csrf
def get_csrf(csrf_url):
    with session.get(url=csrf_url) as resp:
        regex = re.compile('csrf_token = "(.*?)"')
        value = re.findall(regex, resp.text)[0]
    return value


if __name__ == '__main__':
    # 登录连接
    login_url = 'https://mefrp.cn/?action=login&page=login'
    # 获取csrf的连接
    csrf_url = 'https://mefrp.cn/?page=panel&module=sign'
    # post请求的登录用户名何密码
    datas = {
        'username': ['asdf123456'],
        'password': ['asdf123456']
    }
    data = {}
    # 用session来维持会话
    session = requests.session()

    # 开始登录+签到
    for username, password in zip(datas['username'],  datas['password']):
        data['username'] = username
        data['password'] = password
        login(login_url, data)
        sign_in(csrf_url)

# 这个CSRF是 每次请求都会改变的一个token  我们得先获取这个token
# 我们用正则表达式提取出来
# 然后我们把这个token与签到的url拼接起来
# 这样看就是成功签到了 ，但是由于今天签到过了所以显示  您今天已经签到过了，请明天再来
# 重新排版一下，理清一下逻辑
# 如果多个账号怎么办，用字典+列表,然后用并行遍历
# OJBK!
