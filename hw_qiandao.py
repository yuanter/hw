"""
cron: 0 */8 * * *
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
from requests.packages import urllib3
urllib3.disable_warnings()


# 需要安装环境cryptography pyOpenSSL certifi
# pip install cryptography
# pip install pyOpenSSL
# pip install certifi

# 账号or邮箱 密码 格式如下: xxx&pwd=xxx
# https://aitk.app/wp-login.php签到
# 青龙变量名称  
# HWLSP_COOKIE
# 变量值：  
# 账号or邮箱 密码 格式如下: xxx&pwd=xxx

# 获取要执行兑换的cookie
def get_cookie():
    ck_list = []
    pin = "null"
    cookie = None
    cookies = get_envs("HWLSP_COOKIE")
    for ck in cookies:
        if ck.get('status') == 0:
            ck_list.append(ck.get('value'))
    if len(ck_list) < 1:
        print('共配置{}条CK,请添加环境变量,或查看环境变量状态'.format(len(ck_list)))
    return ck_list


def aitk_login(user):
    url = 'https://aitk.app/wp-login.php'
    headers = {
        'Host': 'aitk.app',
        'referer': 'https://aitk.app/wp-login.php',
        'content-type': 'application/x-www-form-urlencoded;',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    data = 'log='+user+'&rememberme=forever&wp-submit=%E7%99%BB%E5%BD%95&redirect_to=https%3A%2F%2Faitk.app%2Fwp-admin%2F&testcookie=1'
    try:
        res = requests.post(url, headers=headers, data=data, verify=False).headers.get('set-cookie')
        array = re.split('[;,]', res)
        return array[5].strip()
    except:
        print("请检查用户信息是否正确")


def checkin(user,cookie):
    if cookie is None:
        return
    url = 'https://aitk.app/wp-admin/admin-ajax.php?action=epd_checkin'
    headers = {
        'referer': 'https://aitk.app/user?pd=money',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }
    r = requests.get(url, headers=headers, verify=False)
    res = r.json()
    if res['status'] == 200:
        print('账号信息：{},签到成功：{}\n'.format(user,res))
    else:
        print('账号信息：{},签到状态：{}\n'.format(user,res))


if __name__ == '__main__':
    user_map = get_cookie()
    for i in range(len(user_map)):
        #print('账号信息为：{}'.format(user_map[i]))
        checkin(user_map[i],aitk_login(user_map[i]))
