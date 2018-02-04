# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog3.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from bs4 import BeautifulSoup
import NCastJson
import NewsJson
from NCastToEpub import NCastToEpub
from ContentToEpub import ContentToEpub
import os

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.resize(400, 400)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, Dialog.height()-50, 220, 40))
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, Dialog.width()-20, Dialog.height()-80))
        self.tabWidget.setFont(font)

        #set tab1
        self.tab = QtWidgets.QWidget()
        self.formLayoutWidget = QtWidgets.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 10, Dialog.width()-50, Dialog.height()-130))
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_2)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.spinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(100)
        self.spinBox.setSingleStep(5)
        self.spinBox.setProperty("value", 10)
        self.spinBox.setDisplayIntegerBase(10)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.radioButton = QtWidgets.QRadioButton(self.formLayoutWidget)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.formLayoutWidget)
        self.radioButton_2.setChecked(True)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.radioButton_2)
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.setTabEnabled(0, False)


        #set tab2
        self.tab_2 = QtWidgets.QWidget()
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, Dialog.width()-50, Dialog.height()-130))
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.comboBox_3 = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_3)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.comboBox_4 = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_4)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.radioButton_3 = QtWidgets.QRadioButton(self.formLayoutWidget_2)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.radioButton_3)
        self.radioButton_4 = QtWidgets.QRadioButton(self.formLayoutWidget_2)
        self.radioButton_4.setChecked(True)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.radioButton_4)
        self.comboBox_5 = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_5)
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget.setCurrentIndex(1)

        #set tab3
        self.tab_3 = QtWidgets.QWidget()
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.tab_3)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(20, 10, Dialog.width()-50, Dialog.height()-130))
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.comboBox_6 = QtWidgets.QComboBox(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_6)
        self.label_10 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.lineEdit_1 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_1)
        self.label_11 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_12 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.label_13 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_14 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_15 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_6)
        self.label_16 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lineEdit_7)
        self.label_17 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.lineEdit_8)
        self.tabWidget.addTab(self.tab_3, "")

        #set tab4
        self.tab_4 = QtWidgets.QWidget()
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_4)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, Dialog.width()-50, Dialog.height()-130))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_18 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.label_18)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.lineEdit_10 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.lineEdit_10)
        self.toolButton = QtWidgets.QToolButton(self.verticalLayoutWidget)
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.listWidget)
        self.tabWidget.addTab(self.tab_4, "")
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)  # multiple selection
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setChecked(True)
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.label_19 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.label_19)
        self.comboBox_7 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.horizontalLayout_3.addWidget(self.comboBox_7)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        #set labels
        self.lang_code = ["ko", "en", "zh", "ja", "fr", "de", "la"]
        Dialog.setWindowTitle("NPub1.3")
        self.label.setText("신 문 사")
        self.label_2.setText("소 분 류")
        self.label_3.setText("매     수")
        self.label_5.setText( "format 선택")
        self.radioButton.setText(".txt")
        self.radioButton_2.setText(".epub")
        self.tabWidget.setTabText(0, "News")
        self.label_4.setText("대 분 류")
        self.label_6.setText("소 분 류")
        self.label_7.setText("페 이 지")
        self.label_8.setText("추출할 순서")
        self.radioButton_3.setText("최신 순")
        self.radioButton_4.setText("주간조회 순")
        self.tabWidget.setTabText(1,  "NCast")
        self.tabWidget.setTabText(2, "HtmlPub")
        self.tabWidget.setTabText(3, "TxtPub")
        self.label_9.setText("언어코드")
        self.comboBox_6.addItems(self.lang_code)
        self.label_10.setText("URL 1")
        self.label_11.setText("URL 2")
        self.label_12.setText("URL 3")
        self.label_13.setText("URL 4")
        self.label_14.setText("URL 5")
        self.label_15.setText("URL 6")
        self.label_16.setText("URL 7")
        self.label_17.setText("URL 8")
        self.label_18.setText("경로 입력(폴더 내 모든 txt 파일이 변환됩니다.)")
        self.label_19.setText("언어코드")
        self.comboBox_7.addItems(self.lang_code)
        self.toolButton.setText("찾기")
        self.checkBox.setText("강제 줄 바꿈 없애기  ")

        self.buttonBox.accepted.connect(self.ok_click)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.ncast = NCastJson.NCast
        for nc in self.ncast:
            self.comboBox_3.addItem(nc['title'])
        self.news = NewsJson.News
        for ns in self.news:
            self.comboBox.addItem(ns['title'])
            print(ns['title'])

        self.comboBox.activated.connect(self.news_select)
        self.comboBox_3.activated.connect(self.ncast_select)
        self.comboBox_2.activated.connect(self.news_subject_select)
        self.comboBox_4.activated.connect(self.ncast_subject_select)
        self.comboBox_5.activated.connect(self.ncast_page_select)
        self.news_range = 0
        self.ncast_range = 0
        self.news_subject = {}
        self.ncast_subject = {}
        self.ncast_page = 1
        self.news_format = 'epub'
        self.news_number = 10
        self.news_select(0)
        self.ncast_select(0)
        self.dir = os.getcwd()
        self.lineEdit_10.setText(self.dir)
        self.sort(self.dir)
        self.toolButton.clicked.connect(self.sort_dir)
        self.file_list = []

    def sort(self, dir):
        self.listWidget.clear()
        self.file_list = []
        for file in os.listdir(dir):
            if file.find('.txt') is not -1:
                self.file_list.append(file)
        self.file_list.sort()
        self.listWidget.addItems(self.file_list)

    def sort_dir(self):
        self.dir = self.lineEdit_10.text()
        self.sort(self.dir)

    def news_select(self, index):
        items = []
        self.comboBox_2.clear()

        for ns in self.news[index]['subs']:
            items.append(ns['name'])

        self.comboBox_2.addItems(items)
        self.news_range = index
        self.news_subject['title'] = self.news[self.news_range]['title']
        self.news_subject_select(0)

    def ncast_select(self, index):
        items = []
        self.ncast_subject = {}
        self.ncast_range = 0
        self.ncast_page = 1
        self.comboBox_5.clear()
        self.comboBox_4.clear()

        for ns in self.ncast[index]['subs']:
            items.append(ns['name'])

        self.comboBox_4.addItems(items)
        self.ncast_range = index
        self.ncast_subject['title'] = self.ncast[self.ncast_range]['title']
        self.ncast_subject_select(0)

    def news_subject_select(self, index):
        self.news_subject['subs'] = self.news[self.news_range]['subs'][index]

    def ncast_subject_select(self, index):
        self.comboBox_5.clear()
        self.ncast_subject['subs'] = self.ncast[self.ncast_range]['subs'][index]
        page = self.find_ncast_pages(self.ncast_subject['subs']['rss'])
        for p in range(page):
            self.comboBox_5.addItem("{0} 페이지({1}~{2})".format(p+1, p*15+1, (p+1)*15))
            if p == 9: break

    def ncast_page_select(self, index):
        self.ncast_page = index + 1

    def find_ncast_pages(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup2 = soup.select("div.paginate")
        return len(soup.select("div.paginate")[0].text)-5

    def ok_click(self):
        selected_tab = self.tabWidget.currentIndex()
        if selected_tab == 1:
            if len(self.ncast_subject)>1:
                rss = self.ncast_subject['subs']['rss']
                if self.radioButton_4.isChecked():
                    rss += "&so=st1.dsc"

                rss += "&page=" + str(self.ncast_page)
                self.ncast_subject['subs']['rss'] = rss
                print(self.ncast_subject)
                ne = NCastToEpub('ncast', self.ncast_subject)
                sys.exit(app.exec_())
            else:
                print("모두 선택해주세요.")
        elif selected_tab == 0:
            if len(self.news_subject)>1:
                self.news_number = self.spinBox.value()
                if self.radioButton.isChecked():
                    self.news_format = 'txt'
            else:
                print("모두 선택해주세요.")
        elif selected_tab == 2:
            language = self.lang_code[self.comboBox_6.currentIndex()]
            urls = [self.lineEdit_1.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(),
                    self.lineEdit_5.text(), self.lineEdit_6.text(), self.lineEdit_7.text(), self.lineEdit_8.text()]
            for url in urls:
                print(url)
                if len(url) > 1:
                    cp = ContentToEpub(language, "html", url, False)
            sys.exit(app.exec_())
        elif selected_tab == 3:
            language = self.lang_code[self.comboBox_7.currentIndex()]
            print(self.checkBox.isChecked())
            for file in self.file_list:
                cp = ContentToEpub(language, "text", self.dir +"/"+file, self.checkBox.isChecked())
            sys.exit(app.exec_())



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

