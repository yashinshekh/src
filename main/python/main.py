from PyQt5.uic.properties import QtWidgets
from PyQt5 import QtCore, QtWidgets
import requests
from PyQt5.QtCore import QThread, pyqtSignal, QEventLoop, QTimer
from PyQt5.QtWidgets import QFileDialog
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from parsel import Selector
import csv
from datetime import datetime, timedelta
from Browser import Browser


class Ui_Dialog(QtWidgets.QMainWindow):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(352, 362)
        self.gridLayout = QtWidgets.QGridLayout(widget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(widget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(widget)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Google Email Scraper"))
        self.lineEdit.setPlaceholderText(_translate("widget", "Google Search Term"))
        self.pushButton.setText(_translate("widget", "Start Scraping"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("widget", "Main"))
        self.label_2.setText(_translate("widget", "https://fiverr.com/ajmiranisha"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("widget", "Contact"))

        self.pushButton.clicked.connect(self.start)
        self.threads = []


    def start(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","CSV Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            self.textBrowser.append("Started web scraping ....")

            loop = QEventLoop()
            QTimer.singleShot(1000, loop.quit)
            loop.exec_()

            self.filename = fileName + '.csv'
            with open(self.filename,"w",newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(['email'])


            self.browser = Browser(self.lineEdit.text())
            self.threads.append(self.browser)
            self.browser.start()
            self.browser.signal.connect(self.finished)


    def finished(self, result):
        self.textBrowser.append(result[0])
        with open(self.filename,"a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(result)



class AppContext(ApplicationContext):
    def run(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    import sys
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
