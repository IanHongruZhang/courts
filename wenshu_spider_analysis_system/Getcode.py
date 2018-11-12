#-*-encoding:utf-8-*-
import requests
import execjs
import random

session = requests.Session()
with open('./docid.js') as fp:
    js = fp.read()
    ctx2 = execjs.compile(js)

with open('./getKey.js') as fp:
    js = fp.read()
    ctx = execjs.compile(js)

def get_guid():
    """
    获取guid参数
    """
    # # 原始js版本
    # js1 = '''
    #   function getGuid() {
    #         var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid(); //CreateGuid();
    #           return guid;
    #     }
    #     var createGuid = function () {
    #         return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    #     }
    # '''
    # ctx1 = execjs.compile(js1)
    # guid = (ctx1.call("getGuid"))
    # return guid

    # 翻译成python
    def createGuid():
        return str(hex((int(((1 + random.random()) * 0x10000)) | 0)))[3:]
    return '{}{}-{}-{}{}-{}{}{}'\
            .format(
                createGuid(), createGuid(),
                createGuid(), createGuid(),
                createGuid(), createGuid(),
                createGuid(), createGuid()
            )
def get_number(guid,proxies):
    """
    获取number
    """
    codeUrl = "http://wenshu.court.gov.cn/ValiCode/GetCode"
    data = {
        'guid':guid
    }
    headers = {
        'Host':'wenshu.court.gov.cn',
        'Origin':'http://wenshu.court.gov.cn',
        'Referer':'http://wenshu.court.gov.cn/',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    req1 = session.post(codeUrl,data=data,headers=headers,proxies = proxies)
    number = req1.text
    return number

def get_vl5x(vjkl5):
    """
    根据vjkl5获取参数vl5x
    """
    vl5x = (ctx.call('getKey',vjkl5))
    return vl5x