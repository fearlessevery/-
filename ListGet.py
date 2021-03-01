import urllib.request,json
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

def getList(keywords):
    browser = webdriver.Chrome(pathConfig.CHROMEPATH, options=chrome_options)
    url = 'https://search.douban.com/movie/subject_search?search_text=' + urllib.parse.quote(keywords) + '&cat=1002'
    browser.get(url)
    try:
        wait = WebDriverWait(browser,10)  # 等待
        wait.until(EC.presence_of_element_located((By.ID, 'root')))  # 等待元素加载
        # browser.find_elements_by_class_name()
        lst=browser.find_elements_by_class_name('item-root')
        classList=['title-text','rating','abstract_2']
        result=[]
        for i in lst:
            record = []
            for j in range(0,len(classList)):
                txt=i.find_elements_by_class_name(classList[j])
                if len(txt)>0:
                    record.append(txt[0].text.replace(' ',''))
                else:
                    record.append('无')
            record.append(i.find_element_by_tag_name('a').get_attribute('href'))
            result.append(record)
    finally:
        browser.close()
    return result
def getDetails(url):
    request = urllib.request.Request(url=url)
    request.add_header('user-agent', header)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')

    img=soup.select('#mainpic img')
    # print(img[0]['src'])
    if len(img)>0:
        urllib.request.urlretrieve(img[0]['src'], filename=pathConfig.IMAGESPATH+'details.png')
    info=soup.select('#info')
    if len(info)>0:
        txt=info[0].get_text()
        txt = txt.replace(' ', '').strip('\n').split('\n')
        # print('\n'.join(txt))
        return ';\n'.join(txt)
    else:
        return '无'
    # return soup.select('a')
# a=getDetails(r'https://movie.douban.com/subject/30176393/')

# resultLst=getList('误杀')
# print(resultLst)
# for i in resultLst:
#     getDetails(i[-1])