import requests
from Checkcode import distinguish

session = requests.session()

def check_code(checkcode='',isFirst=True):  # 是否传入验证码,是否第一次验证码错误
    """
    验证码识别，参数为checkcode和isFirst，用于标识是否为第一次验证码识别，
    第一次识别需要下载验证码，由于文书验证码验证经常出现验证码正确但
    但会验证码错误情况，所以第一次验证码错误时不会下载新的验证码.
    """
    if checkcode == '':
        check_code_url = 'http://wenshu.court.gov.cn/User/ValidateCode'
        headers = {
            'Host':'wenshu.court.gov.cn',
            'Origin':'http://wenshu.court.gov.cn',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }
        req = session.get(check_code_url,headers=headers)
        fp = open('./checkCode.jpg','wb')
        fp.write(req.content)
        print(req.content)
        fp.close()
        checkcode = distinguish('checkCode.jpg')
    print('识别验证码为：{0}'.format(checkcode))
    check_url = 'http://wenshu.court.gov.cn/Content/CheckVisitCode'
    headers = {
        'Host':'wenshu.court.gov.cn',
        'Origin':'http://wenshu.court.gov.cn',
        'Referer':'http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    }
    data = {
        'ValidateCode':checkcode
    }
    req = session.post(check_url,data=data,headers=headers)
    if req.text == '2':
        print('验证码错误')
        if isFirst:
            check_code(checkcode,False)
        else:
            check_code()
