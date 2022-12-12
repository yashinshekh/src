# -*- coding: utf-8 -*-
from PyQt5.uic.properties import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
from Browser import Browser
import os
import platform
import wget

if platform.system() == "Windows":
    import pkg_resources.py2_warn

# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options


class Ui_Form(QtWidgets.QMainWindow):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(361, 406)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(widget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(widget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "AMAZON SCRAPER"))
        self.lineEdit.setPlaceholderText(_translate("widget", "AMAZON domain (http://amazon.com/)"))
        self.lineEdit_2.setPlaceholderText(_translate("widget", "Waiting Delay (s)"))
        self.pushButton.setText(_translate("widget", "*.CSV Sku"))
        self.pushButton_2.setText(_translate("widget", "Start Automation "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("widget", "Main"))
        self.label_2.setText(_translate("widget", "https://fiverr.com/ajmiranisha"))
        self.label.setText(_translate("widget", "RUN AS ADMINISTRATOR"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("widget", "Contact"))


        self.threads = []
        self.pushButton.clicked.connect(self.getfilename)
        self.pushButton_2.clicked.connect(self.start)
        self.fileName = "test"
        self.profiles = []


    def getfilename(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getSaveFileName()","","CSV Files (*);;CSV Files (*.csv)", options=options)

        try:
            with open(self.fileName,"r") as r:
                reader = csv.reader(r)
                for line in reader:
                    self.profiles.append(line[0])
                    self.textBrowser.append(line[0])

        except:
            self.eliminate = []


    def start(self):
        self.textBrowser.append("Started web scraping ...")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.outputFile, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","CSV Files (*);;CSV Files (*.csv)", options=options)

        self.outputFile = self.outputFile+'.csv' if self.outputFile else ''

        if self.outputFile:
            with open(self.outputFile,"w",newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(['asin','monthly_sale_js','monthly_sale_helium','keepa_stock','scanunlimited','Has the brand owner or amazon made sales in the last 90 days?'])


            self.textBrowser.append("Starting chrome browser ...")

            newlists = self.profiles
            # print(newlists)

            if newlists and self.lineEdit.text() and self.lineEdit_2.text():
                self.browser = Browser(newlists,self.lineEdit.text(),self.lineEdit_2.text())

                self.threads.append(self.browser)
                self.browser.start()
                self.browser.signal.connect(self.trackdata)

            else:
                self.textBrowser.append("Missing values")


    def trackdata(self,result):
        self.textBrowser.append(result[0])
        with open(self.outputFile,"a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(result)
            print(result)





class AppContext(ApplicationContext):
    def run(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = Ui_Form()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    import sys
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
