import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
domain='https://www.dytts.com'
def getPlayUrl(title,url):
    request = urllib.request.Request(url=url)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    urlLst = soup.select('#playlist1 li a')
    result=[]
    for i in urlLst:
        result.append([title+i.get_text(),'电影天堂',domain+i['href']])
    if len(result)>0:
        return result
    else:
        return [[]]
def getOnlineUrl(keywords):
    res = quote(keywords)
    url = domain+"/so/-------------.html?wd="+res+"&submit="
    s = urllib.request.urlopen(url)
    soup = BeautifulSoup(s, 'lxml')
    title = soup.select('.detail h3 a')
    result=[]
    for i in title:
        result+=getPlayUrl(i.get_text(),domain+i['href'])
    if len(result)>0:
        return result
    else:
        return [['未找到资源!','','']]
# a=getOnlineUrl('花千骨')
# for i in a:
#     print(i)
