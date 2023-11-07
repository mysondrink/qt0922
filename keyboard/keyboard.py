import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from keyboard.mykeyboard import MyKeyBoard

qss = "QLineEdit {                    \
            border-style: none;        \
            padding: 3px;              \
            border-radius: 5px;        \
            border: 1px solid #dce5ec; \
            font-size: 30px;           \
        }                              \
        "
label_qss = "QLabel {                    \
            border-style: none;        \
            padding: 3px;              \
            border-radius: 5px;        \
            border: 1px solid #dce5ec; \
            font-size: 30px;           \
        }                              \
        "


class KeyBoard(QWidget):
    text_msg = Signal(str)
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        desktop = QApplication.desktop()

        screenRect = desktop.screenGeometry()
        height = int(screenRect.height() / 2)
        height = 480
        width = screenRect.width()
        width = 800
        self.mywin = QWidget()
        self.mywin.setGeometry(0, 0, width, height)
        # 设置窗口接受焦点事件
        # self.mywin.setWindowFlags(
        #     Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)
        self.mywin.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.textInput = QLineEdit()
        self.textInput.setFocus()
        self.textInput.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.textInput.setStyleSheet(qss)
        self.nameLabel = QLabel()
        self.nameLabel.setStyleSheet(label_qss)
        self.mykeyboard = MyKeyBoard()
        self.mykeyboard.info_msg.connect(self.infoMsg)
        h = QHBoxLayout()
        h.addWidget(self.nameLabel, 1)
        h.addWidget(self.textInput, 5)
        v = QVBoxLayout()
        v.addLayout(h, 1)
        v.addWidget(self.mykeyboard, 5)
        self.mywin.setLayout(v)

    def showWindow(self):
        self.mywin.show()

    def infoMsg(self, msg):
        if msg == "close":
            self.text_msg.emit(self.textInput.text())
            self.mywin.deleteLater()
