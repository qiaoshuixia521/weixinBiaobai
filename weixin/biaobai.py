#-*-encoding:utf8-*-
'''
查看python项目在虚拟环境中添加的依赖包（框架）-------- pip3 list
1.  ('\n\t\u3000\u3000')   表示空行，在应用中，我们可以利用他来分割
2.
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import requests
import re
import os
import datetime
import itchat
import time

def pa_qing_hua(love_word_path):
    print("正在抓取你要的句子............")
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # browser=webdriver.PhantomJS('D:\chromedriver_win32\chromedriver.exe')
    browser=webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)
    url="http://www.binzz.com/yulu2/3588.html"
    browser.get(url)
    html = browser.page_source        #html为字符串
    Selector= etree.HTML(html)
    lover_words_xpath_str='//*[@id="content"]/p/text()'
    lover_words=Selector.xpath(lover_words_xpath_str )  #文档.xpath(要提取内容的表达式)
    for i in lover_words :
        word=i.strip('\n\t\u3000\u3000').strip()
        with open(love_word_path,'a+',encoding= 'utf8') as file:
            file.write(word+'\n')
    print("你要的情话爬取完成")

#爬取我爱你的图片
def get_love_phtot(pic_path):
    print('正在爬取我爱你的图片........')
    for i in range(1,22):
        url = 'http://tieba.baidu.com/p/3108805355?pn={}'.format(i)   #构造每一页的url
        response=requests.get(url)
        html=response.text
        pattern=re.compile(r'<img class="BDE_Image" src="(.*?)".*?>',re.S)
        image_url=re.findall(pattern,html)         #首先转换一个正则表达式的匹配模式，然后用re.findall（）方法，传入模式，和要查询的文本
        for j,data in enumerate(image_url):
            # print(j,data)
            pics=requests.get(data)
            mkdir(pic_path)
            fg=open(pic_path+'\\'+str(i)+"_"+str(j)+'.jpg','wb')   #python3中创建路径的方式
            fg.write(pics.content)
            fg.close()
    print('爬取图片完成')
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  #判断是否存在文件夹，如果不存在则创建文件夹
        os.makedirs(path)   #makedirs 创建文件是如果路径不存在会创建路径
        print("-----   new folder .... ----------")
        print('------- ok --------------')
    else:
        print("正在保存图片中......")

def send_news(pic_path,love_word_path):      #时间的计算
    #计算相识天数
    inLoveDate=datetime.datetime(2018,8,15)
    print(inLoveDate)
    todayDate=datetime.datetime.today()
    print(todayDate)
    inLoveDays=(todayDate - inLoveDate).days
    print(inLoveDays)

    #获取情话
    file_path=os.getcwd()+'\\'+love_word_path
    with open(file_path,'r',encoding= 'utf8') as file:
        love_word=file.readlines()
        print(love_word)
        love_word2=love_word[inLoveDays]
        print(love_word2.split(':'))


    itchat.auto_login(hotReload=True)    #热启动，不需要多次扫码登录
    my_friend = itchat.search_friends(name='段呀佩')
    print(my_friend)
    girlfriend = my_friend[0]["UserName"]
    print(girlfriend)
    message='''
    情爱的{}：
        早上好，今天是和KOC 相识的第{}天~~~~~~~~~~~~
        今天他想对你说的话是：
        {}
        最后也是最重要的！
        
    '''.format("XXX",str(inLoveDays),love_word)
    itchat.send(message,toUserName=girlfriend)


    files=os.listdir(pic_path)    #列出pic_path目录下的左右文件
    file=files[inLoveDays]
    love_image_file=file
    try:
        itchat.send_image(love_image_file,toUserName=girlfriend)
    except Exception as e:
        print(e)
    print("成功发送")



def main():
    love_word_path = './love_hua.txt'
    photo_file = '../phtot'
    if os.path.exists(love_word_path):
        print('文件存在')
    else:
        pa_qing_hua(love_word_path)
    if os.path.exists(photo_file):
        print('图片资源已存在')
    else:
        get_love_phtot(photo_file)

    send_news(photo_file,love_word_path)



if __name__=='__main__':
    # #定时发送版本
    # while True:
    #     curr_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())   #格式化字符串
    #     love_time=curr_time.split("")[1]   #2018-09-10 13：04：02  获取时分秒
    #     if love_time =="22:46:01":
    #         main()
    #         time.sleep(60)
    #     else:
    #         print("爱你的每一天都是如此美好，现在时间："+love_time)

    main()
