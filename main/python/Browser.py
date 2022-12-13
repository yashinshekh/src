from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer
from parsel import Selector
from selenium import webdriver
import os
import platform

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
import csv
from datetime import datetime as dt
import time as t


class Browser(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self,csv,folder):
        QThread.__init__(self)
        self.expirydate = '2023/12/20'

        self.csv = csv
        self.folder = folder
        self.upload_url = 'https://www.pinterest.com/pin-builder/'

    def waituntildie(self,string):
        if string not in str(self.driver.page_source):
            print('waiting ...  '+str(string))
            t.sleep(3)
            return self.waituntildie(string)
        return

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

        self.driver.maximize_window()

        try:
            self.driver.get("https://www.pinterest.com/login/")
            self.waituntildie("Notifications")
        except:
            pass

        with open(self.csv,"r") as r:
            reader = csv.reader(r)
            next(reader)
            for data in reader:
                try:
                    self.pinboard = str(data[0])  # Required.
                    self.file_path = self.folder+'/'+str(data[1])  # Required.

                    if data[1] not in os.listdir(self.folder):
                        self.signal.emit({'msg':'image not found ...'})

                    print(self.file_path)
                    self.title = str(data[2])  # Required.
                    self.description = str(data[3])  # Optional.
                    self.alt_text = str(data[4])  # Optional.
                    self.link = str(data[5])  # Optional.

                    # try:
                    self.driver.get(self.upload_url)  # Go to upload pins URL.
                    t.sleep(3)
                    self.driver.find_element_by_xpath('//button[@data-test-id="board-dropdown-select-button"]').click()
                    t.sleep(4)
                    try:
                        self.driver.find_element_by_xpath('//div/text()[contains(.,"'+str(self.pinboard)+'")]/../../..').click()
                    except:
                        self.signal.emit({'msg':'Invalid pin board.'})
                    t.sleep(2)
                    self.driver.find_element_by_xpath('//input[contains(@id, "media-upload-input")]').send_keys(self.file_path)
                    t.sleep(1)
                    self.driver.find_element_by_xpath('//textarea[contains(@id, "pin-draft-title")]').send_keys(self.title)
                    t.sleep(1)
                    self.driver.find_element_by_xpath('//*[@role="combobox"]/div/div/div/span/br').send_keys(self.description)
                    t.sleep(1)
                    self.driver.find_element_by_xpath('//div[@data-test-id="pin-draft-alt-text-button"]/button').click()
                    t.sleep(1)
                    self.driver.find_element_by_xpath('//textarea[contains(@id, "pin-draft-alttext")]').send_keys(self.alt_text)
                    t.sleep(1)
                    self.driver.find_element_by_xpath('//textarea[contains(@id, "pin-draft-link")]').send_keys(self.link)
                    t.sleep(1)
                    self.driver.find_element_by_xpath('//button[@data-test-id="board-dropdown-save-button"]').click()
                    # If a dialog div appears, pin is uploaded.
                    t.sleep(15)

                    self.signal.emit({
                        'msg':'uploaded ...'
                    })

                except:
                    self.signal.emit({'msg':"error during upload"})
        self.driver.close()



