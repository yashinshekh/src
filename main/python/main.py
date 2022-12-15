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


class Ui_Form(QtWidgets.QMainWindow):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(392, 355)
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
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
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
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(widget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Pinterest Auto Uploader"))
        self.pushButton.setText(_translate("widget", "*csv pinterst data"))
        self.pushButton_3.setText(_translate("widget", "Image Location"))
        self.lineEdit.setPlaceholderText(_translate("widget", "inital delay (in seconds)"))
        self.pushButton_2.setText(_translate("widget", "Start Automation"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("widget", "Main"))
        self.label_2.setText(_translate("widget", "https://fiverr.com/ajmiranisha"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("widget", "Contact"))

        self.threads = []
        self.pushButton.clicked.connect(self.getcsvfilename)
        self.pushButton_3.clicked.connect(self.getimagefolder)
        self.pushButton_2.clicked.connect(self.start)
        self.fileName = "test"
        self.profiles = []


    def getimagefolder(self):
        self.folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        self.textBrowser.append(str(self.folder))

    def getcsvfilename(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.csv, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getSaveFileName()","","CSV Files (*);;CSV Files (*.csv)", options=options)

        self.textBrowser.append(str(self.csv))


    def start(self):
        self.textBrowser.append("Web scraping started ...")

        self.browser = Browser(self.csv,self.folder,self.lineEdit.text())
        self.threads.append(self.browser)
        self.browser.start()
        self.browser.signal.connect(self.trackdata)


    def trackdata(self,result):
        self.textBrowser.append(result['msg'])




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
