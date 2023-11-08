from gui.wifi import *
from keyboard.keyboard import KeyBoard
from utils.wifi import wifisearch


class wifiPage(Ui_Form, QWidget):
    next_page = Signal(str)
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.InitUI()

    def InitUI(self):
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFocusWidget()
        self.installEvent()

    def installEvent(self):
        for item in self.focuswidget:
            item.installEventFilter(self)

    def setFocusWidget(self):
        self.focuswidget = [self.ui.pwdLine]
        for item in self.focuswidget:
            item.setFocusPolicy(Qt.ClickFocus)

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

    def setKeyBoard(self, obj):
        self.keyboardtext = KeyBoard()
        self.keyboardtext.text_msg.connect(self.getKeyBoardText)
        obj_name = obj.objectName()
        obj_text = obj.text()
        self.keyboardtext.textInput.setText(obj_text)
        if obj_name == "pwdLine":
            self.keyboardtext.nameLabel.setText("密码")
        self.keyboardtext.showWindow()

    def getKeyBoardText(self, msg):
        self.focusWidget().setText(msg)
        self.focusWidget().clearFocus()

    # 设置wifi选择框
    def setWifiName(self):
        self.wifiName = wifisearch.getwifiname()
        self.ui.wifiCb.addItems(self.wifiName)

    @Slot()
    def on_btnConfirm_clicked(self):
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
            self.infoMessageBox(m_info, m_title)
            cmd_date = 'echo %s | sudo ntpdate cn.pool.ntp.org' % ('orangepi')
            os.system(cmd_date)
        else:
            m_title = "确认"
            m_title = ""
            m_info = "wifi连接失败！"
            self.infoMessageBox(m_info, m_title)

        time.sleep(1)

    @Slot()
    def on_btnReturn_clicked(self):
        page_msg = 'sysPage'
        self.next_page.emit(page_msg)

