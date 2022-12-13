from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer
from parsel import Selector
import time
from selenium import webdriver
import os
import platform

class Browser(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self,url):
        QThread.__init__(self)
        self.expirydate = '2023/06/20'

        self.url = url

        # self.image_no = 5
        # self.facebook_url = "https://www.facebook.com/Hikenhill-277963659578031"


    def waituntildie(self,string):
        if string not in str(self.driver.page_source):
            print('waiting ...  '+str(string))
            time.sleep(3)
            return self.waituntildie(string)
        return

    def run(self):
        if platform.system() == "Windows":
            self.driver = webdriver.Firefox(executable_path=os.getcwd()+"\\geckodriver.exe")
        else:
            self.driver = webdriver.Firefox()

        self.driver.maximize_window()

        self.driver.get(self.url)
        time.sleep(10)

        links = Selector(text=self.driver.page_source).xpath('.//*[@class="if sl sm"]/div/a/@href').extract()
        for link in links:
            self.driver.get("https://www.ubereats.com"+str(link))
            time.sleep(7)

            response = Selector(text=self.driver.page_source)

            title = response.xpath('.//h1/text()').extract_first()
            try:
                infos = ''.join(response.xpath('.//*[@class="c3 u2 ah"]/text()').extract())
            except:
                infos = ''
            try:
                rating = infos.split('•')[0]
            except:
                rating = ''
            try:
                cuisine = infos.split('•')[1]
            except:
                cuisine = ''
            try:
                pricing = infos.split('•')[2]
            except:
                pricing = ''
            delivery_info = response.xpath('.//span[contains(.,"Delivery Fee")]/text()').extract_first()

            self.driver.find_element_by_xpath('.//span[contains(.,"Tap for hours, info, and more")]').click()
            time.sleep(5)
            response = Selector(text=self.driver.page_source)
            address = response.xpath('.//*[@class="ce cz cg d0 ah ai e1 vp vq vr bx"][1]/text()').extract_first()
            open_timing = response.xpath('.//*[@class="ce cz cg d0 ah ai e1 vp vq vr bx"][2]/text()').extract_first()


            self.signal.emit(["https://www.ubereats.com"+str(link),title,rating,cuisine,pricing,delivery_info,address,open_timing])


        self.driver.close()



