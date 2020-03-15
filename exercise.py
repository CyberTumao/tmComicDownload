from selenium import webdriver  #导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys  #导入Keys
import requests
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# driver = webdriver.Firefox()  #指定使用的浏览器，初始化webdriver
# driver.get("http://www.mangabz.com/m102476/")  #请求网页地址
# assert "Python" in driver.title  #看看Python关键字是否在网页title中，如果在则继续，如果不在，程序跳出。
# elem = driver.find_element_by_name("q")  #找到name为q的元素，这里是个搜索框
# elem.clear()  #清空搜索框中的内容
# elem.send_keys("pycon")  #在搜索框中输入pycon
# elem.send_keys(Keys.RETURN)  #相当于回车键，提交
# assert "No results found." not in driver.page_source  #如果当前页面文本中有“No results found.”则程序跳出
# driver.close()  #关闭webdrivertp response的网页HTML
# elem = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/a[3]")
# driver.execute_script('ShowNext();')
# elem = driver.find_element_by_link_text("javascript:ShowNext();")
# elem.click()

class AlbumCover():

    def __init__(self):
        self.init_url = "http://www.mangabz.com/297bz/" #请求网址
        self.folder_path = "/Users/tumao/Documents/达尔文游戏/" #想要存放的文件目录

    def save_img(self, url, file_name):  ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name, '图片保存成功！')
        f.close()

    def request(self, url):  # 封装的requests 请求
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

    def get_files(self, path):  # 获取文件夹中的文件名称列表
        pic_names = os.listdir(path)
        return pic_names

    def spider(self):
        print("Start!")
        driver = webdriver.Firefox()
        driver.get(self.init_url)
        html = driver.page_source

        all_a = BeautifulSoup(html, 'lxml').find(attrs={'class':'detail-list-form-con'}).find_all('a')

        for item in all_a:
            chapter_url = "http://www.mangabz.com"
            self.chapter_sipder(chapter_url, item['href'])

        driver.close()

    def chapter_sipder(self, path, href_code):
        driver = webdriver.Firefox()
        driver.get(path+href_code)
        print("path:")
        print(path+href_code)
        #等待页面加载
        loc1 = (By.ID, 'lbcurrentpage')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(loc1))
        html = driver.page_source
        #章节
        chapter = BeautifulSoup(html, 'lxml').find(attrs={'class':'top-bar'}).find(attrs={'class':'container'}).find('p')
        chapter_text = chapter.text.replace(' ','')
        #页数
        elem = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/span").text
        result = elem.split('-')

        href_string = href_code.replace('/','')
        dir_path = self.folder_path+chapter_text+"_"+href_string+"/"
        self.mkdir(dir_path)  # 创建文件夹
        os.chdir(dir_path)  # 切换路径至上面创建的文件夹
        file_names = self.get_files(dir_path)  # 获取文件夹中的所有文件名，类型是list

        driver.close()

        print("result")
        print(result)
        page = len(file_names)
        num = 1
        if page > 0 :
            if page - 1 == int(result[-1]):
                print("该章节已下载")
                return
            elif page != 1:
                num = page - 1

        path_circle = path+href_code
        self.save_img_circle(path_circle[:-1], chapter_text, file_names, str(num), result)

    def save_img_circle(self, path, chapter_text, file_names, num, result):
        driver = webdriver.Firefox()
        if num ==1 :
            driver.get(path)
        else :
            driver.get(path+"-p"+str(num)+"/")
        #等待页面加载
        loc1 = (By.ID, 'cp_image')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(loc1))
        html = driver.page_source

        album_name = chapter_text + "_" + num + '.jpg'
        cp_img = BeautifulSoup(html, 'lxml').find(id='cp_img')
        all_a = cp_img.find(id='cp_image')
        album_img = all_a['src']

        if album_name in file_names:
            print('图片已经存在，不再重新下载')
        else:
            self.save_img(album_img, album_name)

        if num < result[-1]:
            driver.close()
            self.save_img_circle(path, chapter_text, file_names, str(int(num)+1), result)
        else:
            driver.close()

album_cover = AlbumCover()
album_cover.spider()
# album_cover.chapter_sipder("http://www.mangabz.com/m102476")