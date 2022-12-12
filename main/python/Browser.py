from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer
from parsel import Selector
import time
from selenium import webdriver
import os
import platform

class Browser(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self,links):
        QThread.__init__(self)
        self.expirydate = '2023/06/20'

        self.links = links

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

        for link in self.links:
            self.driver.get(link)

            time.sleep(5)
            datas = Selector(text=self.driver.page_source).xpath('.//*[@data-e2e="user-post-item-list"]/div//a/@href[contains(.,"/video/")]').extract()[:6]

            self.signal.emit([link]+datas)
            print([link]+datas)

            time.sleep(30)



        self.driver.close()



