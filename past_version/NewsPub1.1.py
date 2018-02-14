#-*- coding: utf-8 -*-
import sys

from PyQt5 import QtWidgets
from dialog import Ui_Dialog

from core import NCastToEpub
from past_version import KoreanNewsEpub


class NewsPaperMaker(Ui_Dialog):
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.news = 0
        self.ncast = 0
        self.many = 15
        self.format = 'epub'
        self.pushButton.clicked.connect(self.ok)
        self.pushButton_2.clicked.connect(self.cancle)
        self.comboBox.activated.connect(self.handleActivated)
        self.comboBox_2.activated.connect(self.handleActivated_2)


    def ok(self):
        if self.news != 0:
            ns = KoreanNewsEpub.KoreanNewsEpub(self.news - 1, self.many)
        if self.ncast != 0:
            cs = NCastToEpub.ContentToEpub(self.ncast - 1)
        sys.exit(app.exec_())


    def cancle(self):
        print('bye')
        sys.exit(app.exec_())

    def handleActivated(self, index):
        self.news = int(index)

    def handleActivated_2(self, index):
        self.ncast = int(index)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = NewsPaperMaker(dialog)
    dialog.show()
    sys.exit(app.exec_())