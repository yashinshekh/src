from PyQt5.QtCore import QThread, pyqtSignal
import datetime
from datetime import timedelta
from selenium import webdriver
import platform
import os
import re
from parsel import Selector
from selenium.webdriver.firefox.options import Options
import time


class Browser(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self,searchterm):
        QThread.__init__(self)
        self.expirydate = '2023/04/01'
        self.searchterm = searchterm

    def getdata(self,url):
        self.driver.get(url)

        alltexts = ''.join([i.strip() for i in Selector(text=self.driver.page_source).xpath('.//text()').extract() if i.strip()])
        emails = list(set([i.lower() for i in re.findall(r'[\w\.-]+@[\w\.-]+', alltexts) if '.png' not in str(i) and 'wixpress' not in str(i)
                                    and '@1' not in str(i) and '@2' not in str(i) and '@2' not in str(i) and '@3' not in str(i) and '@4' not in str(i)
                                    and '@5' not in str(i) and '@6' not in str(i) and '@7' not in str(i) and '@8' not in str(i) and '@9' not in str(i)
                                    and '.x' not in str(i) and '.xn' not in str(i) and 'nr@' not in str(i) and '@n0' not in str(i) and '.content' not in str(i)
                                    and 'name@' not in str(i) and 'email@' not in str(i) and 'content@' not in str(i) and 'filterempty' not in str(i)
                                    and 'striphtml' not in str(i) and '.0' not in str(i) and 'domain' not in str(i) and 'example' not in str(i) and '.n02' not in str(i)
                                    and 'jpeg' not in str(i) and 'jpg' not in i and 'png' not in i and 'sentry' not in i and 'svg' not in str(i) and '@0' not in str(i)
                                    and '.js' not in str(i) and '@.' not in i and '.@' not in i and 'email' not in i and 'media' not in i and '-' not in i
                                    ]))

        for email in emails:
            if '.com' in email:
                email = email[:email.index('.com')+4]
                self.signal.emit([email])
                print([email])


        nextlink = Selector(text=self.driver.page_source).xpath('.//*[@id="pnnext"]/@href').extract_first()
        if nextlink:
            time.sleep(10)
            self.getdata("https://www.google.com"+nextlink)



    def run(self):
        options = Options()
        # options.add_argument('--headless')

        if platform.system() == "Windows":
            self.driver = webdriver.Firefox(executable_path=os.getcwd()+'\\geckodriver.exe',options=options)
        else:
            self.driver = webdriver.Firefox(options=options)

        if datetime.datetime.strptime(self.expirydate,'%Y/%m/%d')+timedelta(days=46) >= datetime.datetime.now():

            self.getdata('https://www.google.com/search?q='+self.searchterm)

        self.driver.close()