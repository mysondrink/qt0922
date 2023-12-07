import os
import time
import sys
import traceback

import frozen
from func.infoPage import infoMessage
from gui.wifi import *
from keyboard.keyboard import KeyBoard
from utils.wifi import wifisearch


class wifiPage(Ui_Form, QWidget):
    next_page = Signal(str)
    update_json = Signal(dict)
    update_log = Signal(str)

    """
    @detail 初始化加载界面信息，同时创建记录异常的信息
    @detail 构造函数
    """
    def __init__(self):
        super().__init__()
        sys.excepthook = self.HandleException
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()

    """
    @detail 捕获及输出异常类
    @param excType: 异常类型
    @param excValue: 异常对象
    @param tb: 异常的trace back
    """
    def HandleException(self, excType, excValue, tb):
        sys.__excepthook__(excType, excValue, tb)
        err_msg = ''.join(traceback.format_exception(excType, excValue, tb))
        self.update_log.emit(err_msg)

    """
    @detail 发送异常信息
    @detail 在正常抛出异常时使用
    @detail 未使用
    """
    def sendException(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.update_log.emit(err_msg)

    """
    @detail 设置界面相关信息
    """
    def InitUI(self):
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        confirm_icon_path = frozen.app_path() + r"/res/icon/confirm.png"
        self.ui.btnConfirm.setIconSize(QSize(32, 32))
        self.ui.btnConfirm.setIcon(QIcon(confirm_icon_path))

        return_icon_path = frozen.app_path() + r"/res/icon/return.png"
        self.ui.btnReturn.setIconSize(QSize(32, 32))
        self.ui.btnReturn.setIcon(QIcon(return_icon_path))

        self.setFocusWidget()
        self.installEvent()
        self.setWifiName()
        # self.mytest()


    """
    @detail 测试信息
    """
    def mytest(self):
        self.ui.wifiCb.addItems(["TPLink","TPLink2023"])

    """
    @detail 安装事件监听
    """
    def installEvent(self):
        for item in self.focuswidget:
            item.installEventFilter(self)

    """
    @detail 设置组件点击焦点
    """
    def setFocusWidget(self):
        self.focuswidget = [self.ui.pwdLine]
        for item in self.focuswidget:
            item.setFocusPolicy(Qt.ClickFocus)

    """
    @detail 事件过滤
    @detail 槽函数
    @param obj: 发生事件的组件
    @param event: 发生的事件
    """
    def eventFilter(self, obj, event):
        if obj in self.focuswidget:
            if event.type() == QEvent.Type.FocusIn:
                # print(obj.setText("hello"))
                self.setKeyBoard(obj)
                return True
            else:
                return False
        else:
            return False

    """
    @detail 设置可以键盘弹出的组件
    @detail 槽函数
    @param obj: 键盘弹出的组件
    """
    def setKeyBoard(self, obj):
        self.keyboardtext = KeyBoard()
        self.keyboardtext.text_msg.connect(self.getKeyBoardText)
        obj_name = obj.objectName()
        obj_text = obj.text()
        self.keyboardtext.textInput.setText(obj_text)
        if obj_name == "pwdLine":
            self.keyboardtext.nameLabel.setText("密码")
        self.keyboardtext.showWindow()

    """
    @detail 获取键盘的文本信息
    @detail 槽函数
    @param msg: 信号，键盘文本信息
    """
    def getKeyBoardText(self, msg):
        self.focusWidget().setText(msg)
        self.focusWidget().clearFocus()

    """
    @detail 设置wifi选择框
    """
    def setWifiName(self):
        mywifi = wifisearch
        self.wifiName = mywifi.getwifiname()
        self.ui.wifiCb.addItems(self.wifiName)

    """
    @detail 确认按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnConfirm_clicked(self):
        try:
            flag = -100
            self.wifiPwd = self.ui.pwdLine.text()
            self.wifiSSID = self.ui.wifiCb.currentText()
            if self.wifiPwd != '':
                cmd_wifi = 'echo %s | sudo nmcli dev wifi connect %s password %s' % (
                'orangepi', self.wifiSSID, self.wifiPwd)
            else:
                cmd_wifi = 'echo %s | sudo nmcli dev wifi connect %s' % ('orangepi', self.wifiSSID)
            result = os.popen(cmd_wifi)
            info = 'Error'
            for i in result:
                flag = i.find(info)
                if flag != -1:
                    break
            if flag == -1:
                m_title = "确认"
                m_title = ""
                m_info = "wifi连接成功！"
                infoMessage(m_info, m_title, 280)
                cmd_date = 'echo %s | sudo ntpdate cn.pool.ntp.org' % ('orangepi')
                os.system(cmd_date)
            else:
                m_title = "确认"
                m_title = ""
                m_info = "wifi连接失败！"
                infoMessage(m_info, m_title, 280)

            time.sleep(1)
        except Exception as e:
            m_title = "确认"
            m_title = ""
            m_info = "wifi连接失败！"
            infoMessage(m_info, m_title, 280)

    """
    @detail 返回按钮操作
    @detail 槽函数
    """
    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'sysPage'
        self.next_page.emit(page_msg)

