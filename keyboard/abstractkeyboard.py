from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

"""
@detail 初始化线程，同时创建记录异常的信息
@detail 构造函数
"""


class abstractkeyboard(QWidget):
    """
    @detail 初始化界面
    @detail 构造函数
    """
    def __init__(self):
        super().__init__()
        self.m_name = ''

    # virtual function
    def update(self):
        pass

    def getName(self):
        return self.m_name

    def setName(self, name):
        self.m_name = name
        print(self.m_name)

    def onKeyPressed(self, key, value):
        recevier = QApplication.focusWidget()
        # print(recevier)
        if recevier is None:
            return
        keyPress = QKeyEvent(QEvent.KeyPress, key, Qt.NoModifier, value)
        keyRelease = QKeyEvent(QEvent.KeyRelease, key, Qt.NoModifier, value)

        QApplication.sendEvent(recevier, keyPress)
        QApplication.sendEvent(recevier, keyRelease)

        return False
