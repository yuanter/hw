"""
cron: 22 22 * * *
new Env('妖火吃肉肉');
"""
#青龙变量一共新增2个地方
#1.青龙变量新增PUSH_PLUS_TOKEN
#2.青龙变量新增yaohuo_COOKIE
import os
import requests, time, re,datetime,json,random
from ql_api import get_envs, disable_env, post_envs, put_envs


#这里是微信推送PUSH_PLUS_TOKEN
PUSH_PLUS_TOKEN = ""
# 从环境变量获取url,不存在则从配置获取
PUSH_PLUS_TOKEN = os.getenv("PUSH_PLUS_TOKEN", PUSH_PLUS_TOKEN)
if PUSH_PLUS_TOKEN is None:
    PUSH_PLUS_TOKEN = ""

def Get_ID(cookie):
    HEADERS = {
    'Cookie': cookie,
    'Host': 'yaohuo.me',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    IDs=[]
    for i in range(1,10):
        url = 'https://yaohuo.me/bbs/book_list.aspx?action=new&siteid=1000&classid=0&getTotal=2022&page='+str(i)
        pagelist = requests.get(url, headers=HEADERS)
        respons = pagelist.content.decode('utf-8')
        ID_ALL = re.findall(r'.+?<img src="/NetImages/li.gif" alt="礼"/><a href="/bbs-(.+?).html.+?">', respons,re.DOTALL)
        for Id in ID_ALL:
            IDs.append(Id)
    print('本次扫描肉贴列表：')
    print(IDs)
    return IDs

# 获取要执行吃肉的cookie
def get_cookie():
    ck_list = []
    pin = "null"
    cookie = None
    cookies = get_envs("yaohuo_COOKIE")
    for ck in cookies:
        if ck.get('status') == 0:
            ck_list.append(ck.get('value'))
    if len(ck_list) < 1:
        print('共配置{}条CK,请添加环境变量,或查看环境变量状态'.format(len(ck_list)))
    return ck_list 

def main(cookie,sid):
    Rou_IDs = open(r'IDs.txt','r+', encoding='utf-8')
    HEADERS = {
    'Cookie': cookie,
    'Host': 'yaohuo.me',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    YaoJing = 0
    JingYan = 0
    dic=[]
    reqtext = ["chi", "吃", "c", "恰", "吃肉", "吃了", "吃吃吃","吃吃"]
    for item in Rou_IDs:
        item = item.replace('\n','')
        dic.append(item)
    print('吃过肉的帖子：{}'.format(dic))
    date  = str(datetime.date.today())
    Stime = int(str(datetime.date.today()).split('-')[2])
    IDs = Get_ID(cookie)
    i =0
    for ID in IDs:
        if str(ID) in dic:
            print('FUCK:'+str(ID))
            print("已经吃过的肉贴。")
            continue
        else:
            ID = str(ID)
            print('FUCK:'+ID)
            url = 'https://yaohuo.me/bbs-'+ID+'.html'
            page = requests.get(url,headers=HEADERS)
            html = page.content.decode('utf-8')
            rou = re.findall(r'.+?<div class="content">.+?余(.+?)\)<br/>每人每日一次派礼', html,re.DOTALL)[0]
            time = int(str(re.findall(r'.+?阅.+?<br/>(.+?)<div class="dashed">', html,re.DOTALL)[0]).split(' ')[1].split('/')[2])
            if time < Stime:
                print(str(time)+":不是今天的肉贴，肉臭了不吃。")
                break
            print(rou)
            if rou == '0' :
                print("肉被吃没了。")
                continue
            data = {
                'face': "",
                'sendmsg': 0,
                'content': reqtext[random.randint(0,7)],
                'action': 'add',
                'id': ID,
                'siteid': 1000,
                'lpage': 1,
                'classid': 177,
                'sid': sid,
                'g': '快速回复'
            }
            req_url = 'https://yaohuo.me/bbs/book_re.aspx'
            req = requests.post(req_url, headers=HEADERS, data=data)
            req_html = req.content.decode('utf-8')
            #print(req_html)
            repe = req_html.find('请不要发重复内容')
            if repe == 1:
                data = {
                    'face': "",
                    'sendmsg': 0,
                    'content': reqtext[random.randint(0,7)],
                    'action': 'add',
                    'id': ID,
                    'siteid': 1000,
                    'lpage': 1,
                    'classid': 177,
                    'sid': sid,
                    'g': '快速回复'
                }
                req_html = requests.post(req_url, headers=HEADERS, data=data)
            Rou_IDs.write(ID+'\n')
            try:
                i = i+1
                msg = str(re.findall(r'.+?获得妖晶:(.+?)，获得经验:(.+?)<br/>', req_html,re.DOTALL)[0])
            except:
                msg = str((0,0))
            print(msg)
            msg = msg.replace('(', '')
            msg = msg.replace(')', '')
            msg = msg.replace('\'', '')
            msg = msg.replace(' ', '')
            msg = msg.split(',')
            YaoJing =YaoJing+ int(msg[0])
            JingYan = JingYan+ int(msg[1])
            print(ID)
       #time.sleep(2)
    
    print(YaoJing)
    print(JingYan)
    message = "****妖火吃肉助手****\n"
    message = "助手执行时间："+str(datetime.datetime.now())+"\n"
    message += '本次运行有'+str(i)+"个肉贴\n"
    message += '共吃了' + str(YaoJing) +"妖精，获得"+ str(JingYan)+"经验。\n"
    pushplus_bot("妖火吃肉小助手",message)
    print(message)
    Rou_IDs.close()
    
def pushplus_bot(title,content):
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSH_PLUS_TOKEN,
        "title": title,
        "content": content,
        "topic": '',
    }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=body, headers=headers).json()

    if response["code"] == 200:
        print("PUSHPLUS 推送成功！")

    else:

        url_old = "http://pushplus.hxtrip.com/send"
        response = requests.post(url=url_old, data=body, headers=headers).json()

        if response["code"] == 200:
            print("PUSHPLUS(hxtrip) 推送成功！")

        else:
            print("PUSHPLUS 推送失败！")

if __name__ == '__main__':
    user_map = get_cookie()
    for i in range(len(user_map)):
        #array = re.split('[;,]', user_map[i])
        sid=re.findall(r"sidyaohuo=(.+?);",user_map[i])
        print('sid账号信息为：{}'.format(sid))
        main(user_map[i],sid)
