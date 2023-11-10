from PySide2.QtWidgets import *
from PySide2.QtCore import QTimer
from PySide2.QtGui import *

class infoMessage(QWidget):
    def __init__(self, info, title,_x=230,_y=200):
        super().__init__()
        self.x = _x
        self.y = _y
        self.m_title = title
        self.m_info = info
        self.InitUI()

    def InitUI(self):
        m_title = self.m_title
        m_info = self.m_info
        m_box = QMessageBox()
        if m_title != '':
            m_box.setWindowTitle(m_title)
        m_box.setWindowTitle(m_title)
        m_box.setText(m_info)
        timer = QTimer()
        timer.timeout.connect(m_box.close)
        timer.start(2500)
        m_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        btnOk = m_box.button(QMessageBox.StandardButton.Ok)
        # timetosleep = 2000
        # btnOk.animateClick(timetosleep)
        btnOk.setText(" ")
        btnOk.setFixedSize(1, 1)
        btnOk.setStyleSheet(u"font: 20pt \"\u5b8b\u4f53\";" \
                            "border:4px solid rgb(0,0,0);" \
                            "background-color:#05abc2;")

        stylesheet = "QMessageBox{" \
                     "font: 20pt \"\u5b8b\u4f53\";" \
                     "border:4px solid rgb(0,0,0);" \
                     "background-color:#05abc2;\
                     }"
        m_box.setStyleSheet(stylesheet)
        m_box.setWindowFlags(Qt.FramelessWindowHint)
        # m_box.setFixedSize(400, 400)
        m_box.setGeometry(self.x, self.y, 400, 400)
        m_box.buttonClicked.connect(lambda: self.checkBoxInfo(m_title))
        m_box.exec_()