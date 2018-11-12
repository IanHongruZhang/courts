### 协程的Splash处理器
# -*-encoding:utf-8-*-

import asyncio
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

wenshu_source = ""
lua = '''
function main(splash, args)
  assert(splash:go("http://wenshu.court.gov.cn/content/content?DocID=f05b8b81-b647-11e3-84e9-5cf3fc0c2c18&KeyWord=%E6%9D%80%E4%BA%BA"))
  assert(splash:wait(0.5))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
'''
url = "http://192.168.99.100:8050/execute?lua_source=" + quote(lua)

async def get_page(url):
    response = requests.get(url)
    response.encoding = "gbk"
    rtext = response.text
    await asyncio.sleep(3)
    return rtext


async def parse_page(url):
    response_text = await get_page(url)  ###await 代表可以挂起的入口
    text = response_text.encode('utf-8').decode('unicode_escape')
    html_soup = BeautifulSoup(text, 'lxml')
    print(html_soup)
    return html_soup


def main(url):
    loop = asyncio.get_event_loop()
    tasks = [parse_page(url)]
    result, _ = loop.run_until_complete(asyncio.wait(tasks))
    return result, _

result, _ = main(url)