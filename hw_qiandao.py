"""
cron: 50 59 * * * *
new Env('黄网签到By片王');
"""
import os
import re
import time
import json
import datetime
import requests
from notify import send
from ql_util import get_random_str
from ql_api import get_envs, disable_env, post_envs, put_envs


# 账号or邮箱 密码 格式如下: xxx&pwd=xxx
#user_map = [
#    'xxx&pwd=xxx',
#    'xxx&pwd=xxx',
#]

# 获取要执行兑换的cookie
def get_cookie():
    ck_list = []
    pin = "null"
    cookie = None
    cookies = get_envs("HWLSP_COOKIE")
    for ck in cookies:
        if ck.get('status') == 0:
            ck_list.append(ck)
    if len(ck_list) < 1:
        print('共配置{}条CK,请添加环境变量,或查看环境变量状态'.format(len(ck_list)))
    return ck_list


def aitk_login(user):
    url = 'https://aitk.app/wp-login.php'
    headers = {
        'referer': 'https://aitk.app/wp-login.php',
        'content-type': 'application/x-www-form-urlencoded;',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    }
    data = 'log='+user+'&rememberme=forever&wp-submit=%E7%99%BB%E5%BD%95&redirect_to=https%3A%2F%2Faitk.app%2Fwp-admin%2F&testcookie=1'
    try:
        res = requests.post(url, headers=headers, data=data).headers.get('set-cookie')
        array = re.split('[;,]', res)
        return array[5].strip()
    except:
        print("请检查用户信息是否正确")


def checkin(cookie):
    if cookie is None:
        return
    url = 'https://aitk.app/wp-admin/admin-ajax.php?action=epd_checkin'
    headers = {
        'referer': 'https://aitk.app/user?pd=money',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    }
    res = requests.get(url, headers=headers).json()
    if res['status'] == 200:
        print("签到成功",res)
    else:
        print(res)


if __name__ == '__main__':
    for i in range(len(user_map)):
        #checkin(aitk_login(user_map[i]))
        user_map = get_cookie()
        for ck in user_map:
            checkin(aitk_login(ck))
