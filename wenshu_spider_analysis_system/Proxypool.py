#-*-encoding:utf-8-*-
# 如果需要用到代理池，请使用以下代码调用
import requests
def get_single_proxy():
    start_url = "http://api.ip.data5u.com/dynamic/get.html?order=a93c435791d8f22ae8c04fb8c28d5586&sep=3"
    response = requests.get(start_url)
    ip = response.text
    proxy = ip.strip("\n")
    return proxy

def get_proxy():
    Proxypool = "http://localhost:5555/random"
    try:
        response = requests.get(Proxypool)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        return None