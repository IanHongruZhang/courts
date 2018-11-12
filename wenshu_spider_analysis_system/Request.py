import requests
from urllib import parse
from Pipelines import Save
import execjs
import json
import GetContent
import Proxypool
import Getcode
import Verification
import Settings
from Settings import Mysql_Save

session = requests.Session()
with open('./getKey.js') as fp:
    js = fp.read()
    ctx = execjs.compile(js)

with open('./docid.js') as fp:
    js = fp.read()
    ctx2 = execjs.compile(js)

def get_vjkl5(guid,number,Param,proxies):
    """
    获取cookie中的vjkl5
    """
    url1 = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number="+number+"&guid="+guid+"&conditions=searchWord+QWJS+++"+parse.quote(Param)
    Referer1 = url1
    headers1 = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Host":"wenshu.court.gov.cn",
        "Proxy-Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
    }
    req1 = session.get(url=url1,headers=headers1,timeout=10,proxies = proxies)
    try:
        vjkl5 = req1.cookies["vjkl5"]
        return vjkl5
    except:
        return get_vjkl5(guid,number,Param)

def get_data(Param,Page,Order,Direction):
    """
    获取数据
    """
    index = 1 #第几页
    if Settings.Proxy_Single == 1 and Settings.Proxy_Pool == 0:
        proxy = Proxypool.get_single_proxy() #详细在Proxypool里去做
    else:
        proxy = Proxypool.get_proxy() #详细在Proxypool里去做
    proxies = {
        "http": "http://" + proxy.strip("\n"),
        "https": "https://" + proxy.strip("\n"),
    }
    print("---------当前代理地址是------------")
    print(proxies)
    guid = Getcode.get_guid()
    print("---------当前guid是------------")
    print("guid:",guid)
    number = Getcode.get_number(guid,proxies)
    print("---------当前number是------------")
    print("number:",number)
    vjkl5 = get_vjkl5(guid,number,Param,proxies) #注意，此步必须要在主程序里完成，目前原因不明
    vl5x = Getcode.get_vl5x(vjkl5)
    print("---------当前vl5x是------------")
    print(vl5x)
    data_save_list = []
    while(True):
        print('###### 第{0}页 ######'.format(index))
        #获取数据
        url = "http://wenshu.court.gov.cn/List/ListContent"
        headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Host":"wenshu.court.gov.cn",
            "Origin":"http://wenshu.court.gov.cn",
            "Proxy-Connection":"keep-alive",
            "Referer":"http://wenshu.court.gov.cn/list/list/?sorttype=1&number={0}&guid={1}&conditions=searchWord+QWJS+++{2}".format(number,guid,parse.quote(Param)),
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }
        data = {
            "Param":Param,
            "Index":index,
            "Page":Page,
            "Order":Order,
            "Direction":Direction,
            "vl5x":vl5x,
            "number":number,
            "guid":guid
        }
        req = session.post(url,headers=headers,data=data,proxies = proxies)
        req.encoding = 'utf-8'
        return_data = req.text.replace('\\','').replace('"[','[').replace(']"',']')\
                    .replace('＆ｌｄｑｕｏ;', '“').replace('＆ｒｄｑｕｏ;', '”')
        print(req.text)
        if return_data == '"remind"' or return_data == '"remind key"':
            print('出现验证码')
            Verification.check_code()
            guid = Getcode.get_guid()
            number = Getcode.get_number(guid)
        else:
            json_data = json.loads(return_data)
            if not len(json_data):
                print('采集完成')
                break
            else:
                RunEval = json_data[0]['RunEval']
                for i in range(1,len(json_data)):
                    name = json_data[i]['案件名称'] if '案件名称' in json_data[i] else ''
                    court = json_data[i]['法院名称'] if '法院名称' in json_data[i] else ''
                    number = json_data[i]['案号'] if '案号' in json_data[i] else ''
                    type = json_data[i]['案件类型'] if '案件类型' in json_data[i] else ''
                    id = json_data[i]['文书ID'] if '文书ID' in json_data[i] else ''
                    id = GetContent.decrypt_id(RunEval, id)
                    date = json_data[i]['裁判日期'] if '裁判日期' in json_data[i] else ''
                    data_dict = dict(
                                    id=id,
                                    name=name,
                                    type=type,
                                    date=date,
                                    number=number,
                                    court=court
                                )
                    data_save_list.append(data_dict)
                    print(data_dict)
            index += 1
            guid = Getcode.get_guid()
            number = Getcode.get_number(guid,proxies)
        #if index == 2:
            #break
    save = Save(data_save_list)
    if Mysql_Save == 1:
        save.MysqlPipelines() ### Mysql存储逻辑开始
    if Settings.Mongodb_Save == 1:
        save.MongoPipelines(data_save_list) ### Mongodb存储逻辑开始
    if Settings.General_Save == 1:
        save.GeneralPipelines(data_save_list) ### 存成CSV的存储逻辑开始
