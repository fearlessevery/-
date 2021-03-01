import requests
from bs4 import BeautifulSoup
from RankingView import *
#定义函数获取并检测页面信息
def Text(url):
     # 爬虫请求头信息
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    }
    try:
        respone = requests.get(url,headers=headers,timeout=30)
        respone.raise_for_status()
        #解决中文字符编码问题
        respone.encoding = respone.apparent_encoding
        return respone.text
    except:
        return ""
def bang(url):
    html = Text(url)
    #使用BeautifulSoup解析页面信息
    soup = BeautifulSoup(html, "html.parser")
    name,zhishu,xingxi = [],[],[]
    #开始获取作品名称信息
    allname = soup.find_all('p',class_ = 'm-title')
    for x in allname:
        name.append(x.string) #使用列表方式 添加信息
    #获取作品昨日指数信息
    allzhishu = soup.find_all("li",class_='m-item-playcount')
    for y in allzhishu:
        zhishu.append(y.span.string)
    #使用中文字符的空格填充
#     print("{0}\t{1}\t{2:^40}".format("排名","作品名称","昨日指数",chr(12288)))
    #用range函数获取前50个数据
    for i in range(50):
#         print("{0}\t{1}\t{2:^40}".format(i+1, name[i], zhishu[i],chr(12288)))
#         xingxi.append([i+1, name[i], zhishu[i]])
        xingxi.append([name[i], zhishu[i]])
    return xingxi
def hot_search(mode='电视剧'):
    url=['https://www.360kan.com/rank/dianshi','https://www.360kan.com/rank/dianying']
    if mode=='电视剧':
        k=0
    elif mode=='电影':
        k=1
    else:
        return [['未找到!','','']]
    list = bang(url[k])
    if k==0:
        dainshi_bang(list)
        reli2(list)
    if k==1:
        dainying_bang(list)
        reli(list)
    return list
def cloudGen():
    lst=[]
    lst.append(hot_search('电视剧'))
    lst.append(hot_search('电影'))
    word_cloud(lst)
# cloudGen()
# t=hot_search('电影')
# print(t)
