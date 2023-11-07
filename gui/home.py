# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 450)
        Form.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 800, 450))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(410, 100, 80, 80))
        self.label_2.setStyleSheet(u"font: 20pt \"\u5e7c\u5706\";\n"
"border:4px solid rgb(0,0,0);\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius: 35px;\n"
"\n"
"")
        self.btnData = QPushButton(self.frame)
        self.btnData.setObjectName(u"btnData")
        self.btnData.setGeometry(QRect(100, 100, 280, 80))
        self.btnData.setStyleSheet(u"QPushButton {\n"
"font: 20pt \"\u5b8b\u4f53\";\n"
"border:4px solid rgb(0,0,0);\n"
"border-radius: 35px;\n"
"background-color:#05abc2;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: rgb(255, 0, 0);\n"
"}\n"
"")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(410, 220, 80, 80))
        self.label_4.setStyleSheet(u"font: 20pt \"\u5e7c\u5706\";\n"
"border:4px solid rgb(0,0,0);\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius: 35px;\n"
"\n"
"")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(100, 100, 80, 80))
        self.label.setStyleSheet(u"font: 20pt \"\u5e7c\u5706\";\n"
"border:4px solid rgb(0,0,0);\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius: 35px;\n"
"\n"
"")
        self.btnSet = QPushButton(self.frame)
        self.btnSet.setObjectName(u"btnSet")
        self.btnSet.setGeometry(QRect(100, 220, 280, 80))
        self.btnSet.setStyleSheet(u"QPushButton {\n"
"font: 20pt \"\u5b8b\u4f53\";\n"
"border:4px solid rgb(0,0,0);\n"
"border-radius: 35px;\n"
"background-color:#05abc2;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: rgb(255, 0, 0);\n"
"}\n"
"")
        self.btnPower = QPushButton(self.frame)
        self.btnPower.setObjectName(u"btnPower")
        self.btnPower.setGeometry(QRect(10, 360, 780, 80))
        self.btnPower.setStyleSheet(u"QPushButton {\n"
"font: 20pt \"\u5b8b\u4f53\";\n"
"border:4px solid rgb(0,0,0);\n"
"background-color:#05abc2;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: rgb(255, 0, 0);\n"
"}\n"
"")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(100, 220, 80, 80))
        self.label_3.setStyleSheet(u"font: 20pt \"\u5e7c\u5706\";\n"
"border:4px solid rgb(0,0,0);\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius: 35px;\n"
"\n"
"")
        self.btnPara = QPushButton(self.frame)
        self.btnPara.setObjectName(u"btnPara")
        self.btnPara.setGeometry(QRect(410, 220, 280, 80))
        self.btnPara.setStyleSheet(u"QPushButton {\n"
"font: 20pt \"\u5b8b\u4f53\";\n"
"border:4px solid rgb(0,0,0);\n"
"border-radius: 35px;\n"
"background-color:#05abc2;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: rgb(255, 0, 0);\n"
"}\n"
"")
        self.btnHistory = QPushButton(self.frame)
        self.btnHistory.setObjectName(u"btnHistory")
        self.btnHistory.setGeometry(QRect(410, 100, 280, 80))
        self.btnHistory.setStyleSheet(u"QPushButton {\n"
"font: 20pt \"\u5b8b\u4f53\";\n"
"border:4px solid rgb(0,0,0);\n"
"border-radius: 35px;\n"
"background-color:#05abc2;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: rgb(255, 0, 0);\n"
"}\n"
"")
        self.btnData.raise_()
        self.label.raise_()
        self.btnSet.raise_()
        self.btnPower.raise_()
        self.label_3.raise_()
        self.btnHistory.raise_()
        self.btnPara.raise_()
        self.label_4.raise_()
        self.label_2.raise_()

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText("")
        self.btnData.setText(QCoreApplication.translate("Form", u"  \u8367\u5149\u68c0\u75ab", None))
        self.label_4.setText("")
        self.label.setText("")
        self.btnSet.setText(QCoreApplication.translate("Form", u"  \u68c0\u75ab\u8bbe\u7f6e", None))
        self.btnPower.setText(QCoreApplication.translate("Form", u"\u7535\u6e90", None))
        self.label_3.setText("")
        self.btnPara.setText(QCoreApplication.translate("Form", u"  \u7cfb\u7edf\u8bbe\u7f6e", None))
        self.btnHistory.setText(QCoreApplication.translate("Form", u"  \u5386\u53f2\u8bb0\u5f55", None))
    # retranslateUi

