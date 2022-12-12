from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
driver_options = webdriver.ChromeOptions()
import os
import time
from parsel import Selector
import platform
import datetime
from datetime import timedelta
import csv

class Browser(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self,asins,domain,sleeptime):
        QThread.__init__(self)
        self.asins = asins
        self.domain = domain
        self.sleeptime = sleeptime

        print(self.asins)


    def run(self):
        options = webdriver.ChromeOptions()

        if platform.system() == "Windows":
            newpath = os.getenv('LOCALAPPDATA')+"\\Google\\Chrome\\User Data\\Selenium Profile"
            options.add_argument("--user-data-dir="+newpath)

            self.driver = webdriver.Chrome(
                executable_path=os.getcwd()+'\\chromedriver.exe',
                options=options
            )

        else:
            options.add_argument("user-data-dir=~/.config/chromium")
            self.driver = webdriver.Chrome(
                executable_path=os.getcwd()+'/chromedriver',
                options=options
            )

        self.driver.get(self.domain)
        time.sleep(int(self.sleeptime))
        time.sleep(5)
        # self.driver.get("https://www.amazon.com/dp/B076PSBJX7")

        jse,jsp = '',''
        he,hp = '',''
        ke,kp = '',''
        se,sp = '',''
        oe,op = '',''

        with open("credentials.csv","r") as r:
            reader = csv.reader(r)
            for line in reader:
                if line[0] == "junglescout username":
                    jse = line[1]
                if line[0] == "junglescount password":
                    jsp = line[1]
                if line[0] == "helium username":
                    he = line[1]
                if line[0] == "helium password":
                    hp = line[1]
                if line[0] == "keepa username":
                    ke = line[1]
                if line[0] == "keepa password":
                    kp = line[1]
                if line[0] == "scanunlimited username":
                    se = line[1]
                if line[0] == "scanunlimited password":
                    sp = line[1]
                if line[0] == "onlineseller username":
                    oe = line[1]
                if line[0] == "onlineseller password":
                    op = line[1]

        try:
            self.driver.get("https://app.scanunlimited.com/session/signin")
            time.sleep(2)
            self.driver.find_element_by_id("mat-input-0").send_keys(se)
            time.sleep(2)
            self.driver.find_element_by_id("mat-input-1").send_keys(sp)
            time.sleep(2)
            self.driver.find_element_by_xpath('.//div/text()[contains(.,"Login")]/..').click()
            time.sleep(5)

        except:
            pass

        try:
            self.driver.get("https://login.junglescout.com/")
            time.sleep(2)
            self.driver.find_element_by_id("email").send_keys(jse)
            time.sleep(1)
            self.driver.find_element_by_id("current-password").send_keys(jsp)
            time.sleep(1)
            self.driver.find_element_by_xpath('.//button[contains(.,"Log in")]').click()
            time.sleep(3)
        except:
            pass

        try:
            self.driver.get("https://members.helium10.com/user/signin")
            time.sleep(2)
            self.driver.find_element_by_id("loginform-email").send_keys(he)
            time.sleep(1)
            self.driver.find_element_by_id("loginform-password").send_keys(hp)
            time.sleep(2)
            self.driver.find_element_by_xpath('.//button[contains(.,"Log In")]').click()
            time.sleep(3)

        except:
            pass

        try:
            self.driver.get("https://keepa.com/#!manage")
            time.sleep(15)
            self.driver.find_element_by_id("panelUserRegisterLogin").click()
            time.sleep(2)
            self.driver.find_element_by_id("submitLogin").click()
            time.sleep(2)
            self.driver.find_element_by_id("username").send_keys(ke)
            time.sleep(1)
            self.driver.find_element_by_id("password").send_keys(kp)
            time.sleep(1)
            self.driver.find_element_by_id("submitLogin").click()
            time.sleep(2)
        except:
            pass


        for asin in self.asins:
            print(self.domain+"/dp/"+str(asin))
            self.driver.get(self.domain+"/dp/"+str(asin))
            time.sleep(10)

            try:
                scan_unlimited_danger = "No Danger" if 'help_outline-24px.svg' in  self.driver.find_element_by_xpath('.//*[@id="ipwarning"]/@src').text else "Danger"
            except:
                scan_unlimited_danger = ''
            try:
                brand = self.driver.find_element_by_xpath('.//a[contains(.,"Brand:")]').text.replace("Brand:",'').split()[0]
            except:
                brand = ''
            try:
                monthly_sale_js = self.driver.find_element_by_xpath('.//label[contains(.,"Monthly Sales")]/../following-sibling::label').text
            except:
                monthly_sale_js = ''
            try:
                monthly_sale_helium = self.driver.find_element_by_xpath('.//div[@class="sc-jWESwd fmIRyj"][contains(.,"30-Day Sales")]/following-sibling::div').text
            except:
                monthly_sale_js,monthly_sale_helium = '',''

            print(monthly_sale_js)
            print(monthly_sale_helium)


            ActionChains(self.driver).send_keys(Keys.SPACE).perform()
            ActionChains(self.driver).send_keys(Keys.SPACE).perform()

            try:
                self.driver.switch_to.frame(self.driver.find_element_by_xpath('.//*[@id="keepa"]'))
                time.sleep(1)
                self.driver.find_element_by_xpath('.//li[contains(.,"Data")]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('.//li[contains(.,"Buy Box Statistics")]').click()
                time.sleep(7)
                self.driver.find_element_by_xpath('.//span[@data-range="180"]').click()
                time.sleep(7)

                keepa_stock = self.driver.find_element_by_xpath('.//*[@class="ag-center-cols-container"]/div/div[4]/span').text
            except:
                keepa_stock = ''
            print("keepa stock: "+str(keepa_stock))

            self.driver.switch_to.default_content()

            # driver.find_element_by_id("scxt-stock-btn").click()
            try:
                self.driver.execute_script("document.getElementById('scxt-stock-btn').click()")
                time.sleep(7)
                self.driver.switch_to.frame(self.driver.find_element_by_xpath('.//*[@id="scxt-widget"]/iframe'))

                brands = Selector(text=self.driver.page_source).xpath('.//*[@id="results"]//tr/td[1]/a/text()').extract()

                os_fba = "NO"
                for b in brands:

                    if brand in b:
                        os_fba = 'YES'
                        break



                # os_fba = self.driver.find_element_by_xpath('.//div/text()[contains(.,"FBA")]/../following-sibling::div').text
            except:
                os_fba = ''
            print("os fba : "+str(os_fba))
            self.driver.switch_to.default_content()

            self.signal.emit([asin,monthly_sale_js,monthly_sale_helium,keepa_stock,scan_unlimited_danger,os_fba])
            print([asin,monthly_sale_js,monthly_sale_helium,keepa_stock,scan_unlimited_danger,os_fba])

        self.driver.close()