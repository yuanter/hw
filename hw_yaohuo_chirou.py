"""
cron: */7 0-1,6-23 * * *
new Env('妖火吃肉肉');
"""
#青龙变量一共新增2个地方
#需要使用pushplus时，请新建青龙变量PUSH_PLUS_TOKEN，变量值为它的token
#使用
#青龙变量名称  
#yaohuo_COOKIE
#变量值：  
#提取整串妖火CK，如果sidyaohuo=xxxx后面没有分号，请加上英文格式的分号;
import os
import requests, time, re,datetime,json,random
from ql_api import get_envs, disable_env, post_envs, put_envs
import datetime
import random




#创建肉贴id文件
if not os.path.exists('IDs.txt'):
    print('本次不存在IDs文件，执行创建操作')
    txt = open(r'IDs.txt','a+')
    txt.close()
#创建记录三天前的时间文件
if not os.path.exists('date.txt'):
    print('本次不存在DateFile文件，执行创建操作')
    date_flie = open(r'date.txt','a+')
    date_flie.close()


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

def main(cookie,sid,flag):
    print("板块对应：\n*201*-*资源共享*|||*197*-*综合技术*\n*177*-*妖火茶馆*|||*240*-*贴图晒照*\n*204*-*有奖活动*|||*203*-*免流讨论*\n*213*-*悬赏问答*|||*201*-*安卓专区*\n*288*-*网站公告*|||*199*-*站务处理*")
    Rou_IDs = open(r'IDs.txt','r+', encoding='utf-8')

    #判断时间问题
    if flag:
        #先判断时间是否已经到三天
        date_flie = open(r'date.txt','r+', encoding='utf-8')
        old_date = None
        for item in date_flie:
            print("item："+item)
            old_date = item
        now_date = datetime.datetime.now()
        #print("当前时间旧时间："+old_date)
        # 加减天数
        if old_date is None:
            old_date = now_date.strftime('%Y%m%d')
            date_flie.write(now_date.strftime('%Y%m%d'))
        #关闭文件
        date_flie.close()
        new_date = (now_date + datetime.timedelta(days=-3)).strftime('%Y%m%d')
        print('打印存储时间：{}，当前时间：{}，以及减去3天的时间：{}'.format(old_date,now_date,new_date))
        if ((int(new_date) - int(old_date)) >= 0):
            print("开始清理"+str(int(new_date) - int(old_date)+3)+"天之内的帖子记录")
            date_flie1 = open(r"date.txt", 'w')
            date_flie1.write(datetime.datetime.now().strftime('%Y%m%d'))
            date_flie1.close()
            Rou_IDs.truncate(0)
        

    HEADERS = {
    'Cookie': cookie,
    'Host': 'yaohuo.me',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    YaoJing = 0
    JingYan = 0
    dic=[]
    reqtext = ["来吃肉", "吃", "先吃肉", "吃点肉", "吃肉", "吃了", "吃吃吃","吃吃"]
    for item in Rou_IDs:
        item = item.replace('\n','')
        dic.append(item)
    #print('吃过肉的帖子：{}'.format(dic))
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
            classid= re.findall(r'.+?<a href="/bbs/book_list.aspx\?action=class&classid=(.+?)">', html, re.DOTALL)[0]
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
                'classid': classid,
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
                    'classid': classid,
                    'sid': sid,
                    'g': '快速回复'
                }
                req_html = requests.post(req_url, headers=HEADERS, data=data)
            if flag:
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
    try:
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
    except Exception as r:
        print('出现异常：%s' %r)

if __name__ == '__main__':
    user_map = get_cookie()
    for i in range(len(user_map)):
        #array = re.split('[;,]', user_map[i])
        sid=re.findall(r"sidyaohuo=(.+?);",user_map[i])
        print('账号：{}的sid账号信息为：{}'.format((i+1),sid))
        if i == (len(user_map)-1):
            main(user_map[i],sid,True)
        else:
            main(user_map[i],sid,False)
            ran_time = random.randint(4, 10)
            print('随机休眠{}秒执行下一个账号\n'.format(ran_time))
            time.sleep(ran_time)
