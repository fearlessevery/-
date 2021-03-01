import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from InitConfig import PATHConfig
pathConfig=PATHConfig()
header = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
chrome_options = Options()
chrome_options.add_argument('--headless')#设置为无头，即不显示浏览器窗口
chrome_options.add_argument('user-agent='+header)
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])  #设置为开发者模式，防止被识别出来使用了Selenium
chrome_options.add_experimental_option("prefs",{"profile.managed_default_content_settings.images": 2})  # 不加载图片
domain='https://www.dy2018.com'
def getUrl(title,detailurl):

    request = urllib.request.Request(url=detailurl)
    request.add_header('user-agent', header)
    html = urllib.request.urlopen(request).read().decode('gb2312','ignore')
    # print(html)
    # print('start')
    soup = BeautifulSoup(html, 'lxml')
    # print('end')
    href = soup.select('td a')
    lst=[]
    for i in href:
        if i['href'][:7]=='magnet:' or i['href'][:4]=='ftp:':
            lst.append([title,'电影天堂',i.get_text(),i['href'],detailurl])
    if len(lst)>0:
        return lst
    else:
        return None

def getDownloadUrl(keywords):
    browser = webdriver.Chrome(pathConfig.CHROMEPATH, options=chrome_options)
    try:
        browser.get(domain)
        wait = WebDriverWait(browser,10)  # 等待
        wait.until(EC.presence_of_element_located((By.NAME, 'keyboard')))  # 等待元素加载
        lst=browser.find_elements_by_name('keyboard')
        if len(lst)>0:
            lst[0].send_keys(keywords)  # 向元素里发送（敲入）Python
            lst[0].send_keys(Keys.ENTER)  # 敲回车
        wait = WebDriverWait(browser, 5)  # 等待
        browser.switch_to.window(browser.window_handles[1])#切换为新页面
        html=browser.page_source
        soup=BeautifulSoup(html, 'lxml')
        urlLst=soup.select('.ulink')
        result=[]
        for i in urlLst:
            result_get=getUrl(i['title'], domain + i['href'])
            if result_get!=None:
                result=result+result_get
    finally:
        browser.close()
    if len(result)>0:
        return result
    else:
        return [['未找到资源!','','','','']]
# resultLst=getDownloadUrl('花千骨')
# for i in resultLst:
#     print(i)
# print(resultLst)
# a=getUrl('误杀','https://www.dy2018.com/i/95161.html')
# for i in a:
#     print(i)